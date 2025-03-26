"""
Reddit scraping client for fetching thread and comment data without using the Reddit API.
"""
import re
import json
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import current_app

def get_reddit_headers():
    """Get headers for Reddit requests."""
    return {
        'User-Agent': current_app.config['REDDIT_USER_AGENT'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

def extract_thread_id(url):
    """Extract the thread ID from a Reddit URL."""
    # Match patterns like https://www.reddit.com/r/subreddit/comments/abcdef/...
    pattern = r'reddit\.com\/r\/\w+\/comments\/([a-z0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_thread_data(thread_id=None, thread_url=None):
    """
    Retrieve data for a Reddit thread including comments by scraping Reddit.
    
    Args:
        thread_id: The Reddit thread ID
        thread_url: The full Reddit thread URL
        
    Returns:
        Dict containing thread data and comments
    """
    if thread_url and not thread_id:
        thread_id = extract_thread_id(thread_url)
        if not thread_id:
            raise ValueError("Invalid Reddit URL format")
    
    if not thread_id:
        raise ValueError("Either thread_id or thread_url must be provided")
    
    # Construct the URL with old.reddit.com which is easier to scrape
    url = f"https://old.reddit.com/r/all/comments/{thread_id}/"
    
    # Log the request
    current_app.logger.info(f"Making request to Reddit: {url}")
    
    # Make the request
    try:
        response = requests.get(
            url, 
            headers=get_reddit_headers(),
            timeout=current_app.config['REDDIT_REQUEST_TIMEOUT']
        )
        response.raise_for_status()
        current_app.logger.info(f"Successfully retrieved Reddit thread: {thread_id}")
    except requests.RequestException as e:
        current_app.logger.error(f"Error fetching Reddit thread: {str(e)}")
        raise ValueError(f"Failed to retrieve Reddit thread: {str(e)}")
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Extract thread metadata and comments
    thread_data = {
        'metadata': get_thread_metadata(soup, thread_id),
        'comments': extract_comments_from_html(soup)
    }
    
    return thread_data

def get_thread_metadata(soup, thread_id):
    """Extract metadata from a Reddit thread HTML."""
    try:
        # Find the title
        title_element = soup.select_one('a.title')
        title = title_element.text.strip() if title_element else "[Unknown Title]"
        
        # Find the subreddit
        subreddit_element = soup.select_one('a.subreddit')
        subreddit = subreddit_element.text.strip() if subreddit_element else "[Unknown Subreddit]"
        if subreddit.startswith('r/'):
            subreddit = subreddit[2:]
        
        # Find the author
        author_element = soup.select_one('a.author')
        author = author_element.text.strip() if author_element else "[deleted]"
        
        # Find the score
        score_element = soup.select_one('div.score.unvoted')
        score_text = score_element.get('title', '0') if score_element else '0'
        try:
            score = int(score_text)
        except ValueError:
            score = 0
        
        # Find the number of comments
        num_comments_element = soup.select_one('a.comments')
        num_comments_text = num_comments_element.text.strip() if num_comments_element else "0 comments"
        num_comments = int(re.search(r'(\d+)', num_comments_text).group(1)) if re.search(r'(\d+)', num_comments_text) else 0
        
        # Get timestamp
        time_element = soup.select_one('time')
        created_utc = int(time.time())  # Default to current time
        if time_element and time_element.get('datetime'):
            try:
                datetime_str = time_element.get('datetime')
                created_utc = int(datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S+00:00').timestamp())
            except (ValueError, TypeError):
                pass
        
        # Build permalink
        permalink = f"/r/{subreddit}/comments/{thread_id}/"
        
        return {
            'id': thread_id,
            'title': title,
            'author': author,
            'score': score,
            'created_utc': created_utc,
            'permalink': permalink,
            'num_comments': num_comments,
            'subreddit': subreddit
        }
    except Exception as e:
        current_app.logger.error(f"Error extracting thread metadata: {str(e)}")
        return {
            'id': thread_id,
            'title': "Error loading thread",
            'author': "[unknown]",
            'score': 0,
            'created_utc': int(time.time()),
            'permalink': f"/comments/{thread_id}/",
            'num_comments': 0,
            'subreddit': "unknown"
        }

def extract_comments_from_html(soup, limit=100):
    """
    Extract comments from Reddit thread HTML.
    
    Args:
        soup: BeautifulSoup object of the thread page
        limit: Maximum number of comments to extract
        
    Returns:
        List of comment dictionaries
    """
    comments = []
    counter = 0
    
    # Find all comment divs
    comment_divs = soup.select('div.comment')
    
    for div in comment_divs:
        if counter >= limit:
            break
            
        try:
            # Skip deleted/removed comments
            if 'deleted' in div.get('class', []):
                continue
                
            # Author
            author_element = div.select_one('a.author')
            author = author_element.text.strip() if author_element else "[deleted]"
            
            # Comment body
            body_element = div.select_one('div.md')
            body = body_element.get_text(strip=True) if body_element else ""
            
            # Skip deleted/removed comments
            if not body or body in ['[deleted]', '[removed]']:
                continue
                
            # Comment score
            score_element = div.select_one('span.score')
            score_text = score_element.get_text(strip=True) if score_element else "0 points"
            score = int(re.search(r'(-?\d+)', score_text).group(1)) if re.search(r'(-?\d+)', score_text) else 0
            
            # Comment ID
            id_match = re.search(r'id-t1_([a-z0-9]+)', str(div))
            comment_id = id_match.group(1) if id_match else f"unknown_{counter}"
            
            # Permalink
            permalink_element = div.select_one('a.bylink')
            permalink = permalink_element['href'] if permalink_element and 'href' in permalink_element.attrs else ""
            
            # Created time (approximate if not available)
            created_utc = int(time.time())  # Default to current time
            time_element = div.select_one('time')
            if time_element and time_element.get('datetime'):
                try:
                    datetime_str = time_element.get('datetime')
                    created_utc = int(datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S+00:00').timestamp())
                except (ValueError, TypeError):
                    pass
            
            comments.append({
                'id': comment_id,
                'author': author,
                'body': body,
                'score': score,
                'created_utc': created_utc,
                'permalink': permalink
            })
            
            counter += 1
                
        except Exception as e:
            current_app.logger.error(f"Error extracting comment: {str(e)}")
            continue
    
    return comments 