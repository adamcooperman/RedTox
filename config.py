import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    DEBUG = FLASK_DEBUG
    
    # Reddit scraping settings
    REDDIT_USER_AGENT = os.environ.get('REDDIT_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    REDDIT_REQUEST_TIMEOUT = int(os.environ.get('REDDIT_REQUEST_TIMEOUT', 10))
    
    # Toxicity detection (Friendly_Text_Moderation API)
    TOXICITY_THRESHOLD = float(os.environ.get('TOXICITY_THRESHOLD', 0.7))
    SAFER_VALUE = float(os.environ.get('SAFER_VALUE', 0.02))
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Cache settings
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

# Set configuration based on environment
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Return the appropriate configuration object based on the environment."""
    config_name = os.environ.get('FLASK_APP_ENV', 'default')
    return config.get(config_name, config['default']) 