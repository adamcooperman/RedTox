"""
Flask routes for the RedTox application.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app, session, g
from app.reddit_client import get_thread_data, extract_thread_id
from app.toxicity_detector import ToxicityDetector

# Create Blueprint
main = Blueprint('main', __name__)

# We'll use Flask's g object to store the detector instance
def get_toxicity_detector():
    """Get or create a toxicity detector instance."""
    if 'toxicity_detector' not in g:
        g.toxicity_detector = ToxicityDetector()
    return g.toxicity_detector

@main.before_request
def before_request():
    """Initialize resources before each request."""
    # Make the toxicity detector available
    get_toxicity_detector()

@main.route('/', methods=['GET'])
def index():
    """Render the home page with the URL input form."""
    return render_template('index.html')

@main.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Analyze a Reddit thread for toxicity."""
    # Get thread_url from either form or query parameters
    thread_url = request.form.get('thread_url') if request.method == 'POST' else request.args.get('thread_url')
    threshold = request.args.get('threshold')
    
    if not thread_url:
        flash('Please enter a Reddit thread URL.')
        return redirect(url_for('main.index'))
    
    current_app.logger.info(f"Analyzing thread URL: {thread_url}")
    
    try:
        # Extract thread ID
        thread_id = extract_thread_id(thread_url)
        if not thread_id:
            flash('Invalid Reddit URL. Please enter a URL to a Reddit thread.')
            return redirect(url_for('main.index'))
        
        current_app.logger.info(f"Extracted thread ID: {thread_id}")
        
        # Get thread data
        thread_data = get_thread_data(thread_id=thread_id)
        thread_metadata = thread_data['metadata']
        comments = thread_data['comments']
        
        current_app.logger.info(f"Retrieved {len(comments)} comments from thread: {thread_metadata['title']}")
        
        # Adjust toxicity threshold if specified
        toxicity_detector = get_toxicity_detector()
        if threshold:
            try:
                threshold = float(threshold)
                if 0 <= threshold <= 1:
                    toxicity_detector.threshold = threshold
                    current_app.logger.info(f"Adjusted toxicity threshold to {threshold}")
            except ValueError:
                pass
        
        # Analyze comments for toxicity
        analyzed_comments, toxicity_stats = toxicity_detector.analyze_comments(comments)
        
        current_app.logger.info(f"Analysis complete. Overall toxicity: {toxicity_stats['avg_toxicity']:.2f}")
        
        # Store data in session for the view page
        session['thread_id'] = thread_id
        session['toxicity_stats'] = toxicity_stats
        
        # Pass data directly to template
        return render_template(
            'results.html', 
            stats=toxicity_stats,
            thread_url=thread_url,
            threshold=toxicity_detector.threshold
        )
    
    except Exception as e:
        flash(f'Error analyzing thread: {str(e)}')
        current_app.logger.error(f"Error analyzing thread: {str(e)}")
        return redirect(url_for('main.index'))

@main.route('/thread', methods=['GET'])
def thread_view():
    """Display the thread with toxicity analysis."""
    thread_url = request.args.get('thread_url')
    threshold = request.args.get('threshold')
    toxicity_detector = get_toxicity_detector()
    
    if not thread_url:
        flash('Thread URL is required.')
        return redirect(url_for('main.index'))
    
    current_app.logger.info(f"Viewing thread: {thread_url}")
    
    # Adjust toxicity threshold if specified
    if threshold:
        try:
            threshold = float(threshold)
            if 0 <= threshold <= 1:
                toxicity_detector.threshold = threshold
                current_app.logger.info(f"Adjusted toxicity threshold to {threshold}")
        except ValueError:
            pass
    
    try:
        # Extract thread ID
        thread_id = extract_thread_id(thread_url)
        if not thread_id:
            flash('Invalid Reddit URL. Please enter a URL to a Reddit thread.')
            return redirect(url_for('main.index'))
        
        # Get thread data
        thread_data = get_thread_data(thread_id=thread_id)
        thread_metadata = thread_data['metadata']
        comments = thread_data['comments']
        
        current_app.logger.info(f"Retrieved {len(comments)} comments for viewing thread: {thread_metadata['title']}")
        
        # Analyze comments for toxicity
        analyzed_comments, toxicity_stats = toxicity_detector.analyze_comments(comments)
        
        current_app.logger.info(f"Thread view analysis complete. Detected {toxicity_stats['toxic_count']} toxic comments")
        
        # Prepare thread data for rendering
        thread_view_data = {
            'metadata': thread_metadata,
            'comments': analyzed_comments,
            'stats': toxicity_stats,
            'threshold': toxicity_detector.threshold
        }
        
        return render_template('thread.html', thread=thread_view_data)
    
    except Exception as e:
        flash(f'Error loading thread: {str(e)}')
        current_app.logger.error(f"Error loading thread: {str(e)}")
        return redirect(url_for('main.index'))

# Keep the old route for backward compatibility
@main.route('/view/<thread_id>', methods=['GET'])
def view_thread(thread_id):
    """Redirect to the new thread view with appropriate parameters."""
    threshold = request.args.get('threshold')
    url = url_for('main.thread_view', thread_url=f"https://reddit.com/comments/{thread_id}")
    if threshold:
        url = f"{url}&threshold={threshold}"
    return redirect(url)

@main.route('/about', methods=['GET'])
def about():
    """Display information about the RedTox application."""
    return render_template('about.html') 