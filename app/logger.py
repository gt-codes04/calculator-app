# app/logger.py
import logging
import os
from app.calculator_config import Config

def setup_logger():
    """Configures the application logger."""
    log_dir = Config.get_log_dir()
    if not os.path.exists(log_dir):
        os.makedirs(log_dir) # pragma: no cover

    log_file_path = os.path.join(log_dir, 'calculator.log')

    # Prevent duplicate handlers if called multiple times
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler() # Also print to console
        ]
    )
    logging.info("Logger configured.")