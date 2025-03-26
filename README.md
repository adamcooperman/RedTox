# RedTox: Reddit Proxy with Toxicity Detection

RedTox is a Python web application that acts as a proxy for Reddit, helping users avoid potentially toxic content by analyzing and filtering comments.

## Features

- **Toxicity Analysis**: Analyze Reddit thread comments for toxic content
- **Toxicity Metrics**: Get statistics on the toxicity level of a thread
- **Content Filtering**: View Reddit threads with toxic comments hidden behind warnings
- **Adjustable Threshold**: Customize the sensitivity of the toxicity detection
- **No API Credentials Required**: 
  - Uses web scraping to access Reddit content without API credentials
  - Uses Hugging Face Spaces API for toxicity detection

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/redtox.git
   cd redtox
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following content:
   ```
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   
   # Reddit scraping settings
   REDDIT_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
   REDDIT_REQUEST_TIMEOUT=10
   
   # Toxicity detection settings
   TOXICITY_THRESHOLD=0.7
   SAFER_VALUE=0.02  # Higher value is less safe (allows more content through)
   ```

## Running the Application

1. Start the development server:
   ```
   python run.py
   ```

2. Open your browser and visit `http://localhost:5000`

## How It Works

RedTox works by:

1. **Reddit Content Access**: Scrapes Reddit content directly from old.reddit.com (which has a simpler HTML structure)
2. **Toxicity Detection**: Uses the [Friendly_Text_Moderation](https://huggingface.co/spaces/duchaba/Friendly_Text_Moderation) API from Hugging Face Spaces to analyze comments
3. **Content Filtering**: Provides a modified version of the thread with toxic comments hidden behind warnings

### Toxicity Detection

The application uses Duc Haba's Friendly_Text_Moderation API to detect toxic content in comments. This API analyzes text and provides toxicity scores across several categories:

- General toxicity
- Identity attacks
- Insults
- Obscenity
- Severe toxicity
- Sexual explicit content
- Threats

You can adjust the "safer" value to control the sensitivity of the toxicity detection. A higher value means less strict filtering (more content will be shown).

## Limitations

Since this application relies on web scraping rather than the official API:

1. It may break if Reddit changes their HTML structure
2. It may not work well with very large threads
3. It could potentially be blocked by Reddit if used extensively

This application is intended for educational purposes and personal use only.

## Credits

- [Friendly_Text_Moderation](https://huggingface.co/spaces/duchaba/Friendly_Text_Moderation) by Duc Haba for toxicity detection

## License

This project is licensed under the MIT License - see the LICENSE file for details. 