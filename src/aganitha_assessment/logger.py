# aganitha_assessment/logger.py
import logging
import re

def setup_logging(debug: bool, query: str) -> logging.Logger:
    """Set up logging configuration for a specific query.

    Args:
        debug (bool): If True, enable debug logging to console in addition to file logging.
        query (str): The query string, used to name the log file.

    Returns:
        logging.Logger: Configured logger instance specific to the query.
    """
    # Sanitize the query to create a safe file name by replacing non-alphanumeric characters with underscores
    safe_query = re.sub(r'\W+', '_', query)
    
    # Create a unique logger for this query to avoid conflicts across different queries
    logger = logging.getLogger(f"aganitha_assessment.{query}")
    
    # Configure the logger only if it doesn't already have handlers
    if not logger.handlers:
        # Set logger level: DEBUG if debug is True, INFO otherwise
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        
        # Define the log message format
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        
        # Always set up a file handler to log to a file named after the sanitized query
        file_handler = logging.FileHandler(f"{safe_query}.log", mode='a')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Add a console handler only if debug is True
        if debug:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
    
    return logger