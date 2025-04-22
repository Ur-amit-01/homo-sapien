import logging
from logging.handlers import RotatingFileHandler
import time

# Custom time converter for IST
IST = time.timezone == -19800  # 5 hours 30 minutes offset
def ist_time(*args):
    return time.localtime(time.time() + 19800)  # 19800 seconds = 5.5 hours

def setup_logger(name, log_file='bot_launcher.log', level=logging.INFO):
    """Set up a configured logger instance"""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    formatter.converter = ist_time  # Set formatter to use IST

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_logger(name):
    """Get an already configured logger instance"""
    return logging.getLogger(name)
    
