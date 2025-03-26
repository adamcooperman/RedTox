"""
RedTox application initialization
"""
from flask import Flask
import logging
import sys

def create_app(config_object=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load config
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_pyfile('../config.py')
    
    # Configure logging - always set up regardless of debug mode
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    
    # Configure root logger
    root_logger = logging.getLogger()
    # Clear existing handlers to avoid duplicate messages
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set up console handler for direct output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Use different format based on debug mode
    if app.config.get('DEBUG', False):
        console_format = logging.Formatter('API DEBUG: %(levelname)s: %(message)s')
    else:
        console_format = logging.Formatter('API INFO: %(levelname)s: %(message)s')
    
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(log_level)
    
    # Set Flask logger level
    app.logger.setLevel(log_level)
    
    # Only reduce werkzeug noise in production
    if not app.config.get('DEBUG', False):
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        
    app.logger.info(f"Application initialized with DEBUG={app.config.get('DEBUG', False)}")
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app 