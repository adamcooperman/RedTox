"""
Toxicity detection component using Friendly_Text_Moderation API.
"""
import json
import logging
import sys
from flask import current_app, has_app_context
from gradio_client import Client

# Simple console logger for when no app context is available
console_logger = logging.getLogger('toxicity_detector')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('TOXICITY-DETECTOR: %(message)s'))
console_logger.addHandler(console_handler)
console_logger.setLevel(logging.INFO)

class ToxicityDetector:
    def __init__(self, threshold=None):
        """
        Initialize the toxicity detector.
        
        Args:
            threshold: Toxicity threshold (0-1), defaults to config value if None
        """
        self._threshold = None
        self.threshold = threshold
        self._client = None
        self._log("======== ToxicityDetector initialized ========")
        
    def _log(self, message, level='info'):
        """Log messages safely with or without app context."""
        if has_app_context():
            logger = current_app.logger
            log_method = getattr(logger, level)
            log_method(message)
        else:
            log_method = getattr(console_logger, level)
            log_method(message)
    
    @property
    def threshold(self):
        """Get the current toxicity threshold."""
        if self._threshold is not None:
            return self._threshold
        
        if has_app_context():
            return current_app.config.get('TOXICITY_THRESHOLD', 0.7)
        return 0.7
        
    @threshold.setter
    def threshold(self, value):
        """Set the toxicity threshold."""
        self._threshold = value
    
    @property
    def client(self):
        """Lazy-load and cache the Friendly_Text_Moderation client."""
        if self._client is None:
            self._log("======== INITIALIZING API CLIENT ========")
            self._client = Client("duchaba/Friendly_Text_Moderation")
            self._log("Client initialization complete")
        return self._client
        
    def analyze_text(self, text):
        """
        Analyze a text string for toxicity using Friendly_Text_Moderation API.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Dictionary containing:
                - score (float): Toxicity score (0-1)
                - is_toxic (bool): Whether the text is classified as toxic
                - categories (dict): Breakdown of toxicity categories
        """
        if not text or len(text.strip()) == 0:
            return {'score': 0, 'is_toxic': False, 'categories': {}}
        
        safer_value = 0.02
        if has_app_context():
            safer_value = current_app.config.get('SAFER_VALUE', 0.02)
        
        # Log API request details
        self._log("\n======== API REQUEST ========")
        self._log(f"Text: {text[:50]}...")
        self._log(f"Safer value: {safer_value}")
        self._log(f"API endpoint: /fetch_toxicity_level")
        
        try:
            # Call the API using positional arguments
            self._log("Calling API with positional arguments")
            _, json_result = self.client.predict(
                text,
                safer_value,
                api_name="/fetch_toxicity_level"
            )
            
            self._log("Response received from API")
            self._log(f"Response (first 100 chars): {json_result[:100]}...")
            
            # Parse the JSON string result
            result_dict = json.loads(json_result)
            
            # Extract the overall toxicity score - use sum_value as the overall score
            toxicity_score = result_dict.get('sum_value', 0)
            
            # Determine if the text is toxic based on the is_flagged or is_safer_flagged fields
            is_toxic = result_dict.get('is_flagged', False) or result_dict.get('is_safer_flagged', False)
            
            # Extract individual toxicity categories
            categories = {
                'harassment': result_dict.get('harassment', 0),
                'harassment_threatening': result_dict.get('harassment_threatening', 0),
                'hate': result_dict.get('hate', 0),
                'hate_threatening': result_dict.get('hate_threatening', 0),
                'self_harm': result_dict.get('self_harm', 0),
                'self_harm_instructions': result_dict.get('self_harm_instructions', 0),
                'self_harm_intent': result_dict.get('self_harm_intent', 0),
                'sexual': result_dict.get('sexual', 0),
                'sexual_minors': result_dict.get('sexual_minors', 0),
                'violence': result_dict.get('violence', 0),
                'violence_graphic': result_dict.get('violence_graphic', 0)
            }
            
            # Log the max category
            max_key = result_dict.get('max_key', 'none')
            max_value = result_dict.get('max_value', 0)
            self._log(f"Highest toxicity category: {max_key} ({max_value:.4f})")
            
            self._log(f"Toxicity analysis complete: score={toxicity_score}, is_toxic={is_toxic}")
            self._log("======== END API REQUEST ========\n")
            
            return {
                'score': toxicity_score,
                'is_toxic': is_toxic,
                'categories': categories,
                'max_category': max_key,
                'max_value': max_value
            }
            
        except Exception as e:
            error_msg = str(e)
            self._log(f"\n======== API ERROR ========", 'error')
            self._log(f"Error: {error_msg}", 'error')
            self._log(f"API call details:", 'error')
            self._log(f"  - Endpoint: /fetch_toxicity_level", 'error')
            self._log(f"  - Text: {text[:50]}...", 'error')
            self._log(f"  - Safer value: {safer_value}", 'error')
            
            import traceback
            self._log(f"Stack trace: {traceback.format_exc()}", 'error')
            self._log(f"======== END API ERROR ========\n", 'error')
            
            # Return a safe default value in case of error
            return {'score': 0, 'is_toxic': False, 'categories': {}}
        
    def analyze_comments(self, comments):
        """
        Analyze a list of comment dictionaries.
        
        Args:
            comments (list): List of comment dictionaries with 'body' field
            
        Returns:
            tuple: (augmented_comments, toxicity_stats)
                - augmented_comments adds 'toxicity' field to each comment
                - toxicity_stats contains overall statistics
        """
        total_comments = len(comments)
        if total_comments == 0:
            return [], {'toxic_count': 0, 'toxic_percentage': 0, 'avg_toxicity': 0, 'total_comments': 0}
        
        self._log(f"\n======== ANALYZING {total_comments} COMMENTS ========")
            
        for comment in comments:
            comment['toxicity'] = self.analyze_text(comment['body'])
            
        # Calculate statistics
        toxic_comments = [c for c in comments if c['toxicity']['is_toxic']]
        toxic_count = len(toxic_comments)
        toxic_percentage = (toxic_count / total_comments) * 100 if total_comments else 0
        
        scores = [c['toxicity']['score'] for c in comments]
        avg_toxicity = sum(scores) / total_comments if total_comments else 0
        
        # Track the max category across all comments
        top_category = None
        top_category_value = 0
        
        # For API results, gather category stats if available
        categories = {}
        for comment in comments:
            if 'categories' in comment['toxicity']:
                # Check if this comment has the highest category value so far
                if 'max_category' in comment['toxicity'] and 'max_value' in comment['toxicity']:
                    max_cat = comment['toxicity']['max_category']
                    max_val = comment['toxicity']['max_value']
                    if max_val > top_category_value:
                        top_category = max_cat
                        top_category_value = max_val
                
                for category, score in comment['toxicity']['categories'].items():
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(score)
        
        category_averages = {
            category: sum(scores) / len(scores) 
            for category, scores in categories.items()
        }
        
        stats = {
            'toxic_count': toxic_count,
            'toxic_percentage': toxic_percentage,
            'avg_toxicity': avg_toxicity,
            'total_comments': total_comments
        }
        
        if category_averages:
            stats['category_averages'] = category_averages
            
        # Add the top category information if available
        if top_category:
            stats['top_category'] = top_category
            stats['top_category_value'] = top_category_value
        
        self._log(f"Comment analysis complete:")
        self._log(f"  - Total comments: {total_comments}")
        self._log(f"  - Toxic comments: {toxic_count} ({toxic_percentage:.1f}%)")
        self._log(f"  - Average toxicity score: {avg_toxicity:.3f}")
        if top_category:
            self._log(f"  - Most severe category: {top_category} ({top_category_value:.4f})")
        self._log(f"======== ANALYSIS COMPLETE ========\n")
            
        return comments, stats 