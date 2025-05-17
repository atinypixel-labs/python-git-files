import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

def setup_logger(name='app'):
	"""
	Set up and return a logger with both file and console handlers.
	Log files are created in the logs directory with date-based names.
	"""
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)

	# Create formatters
	file_formatter = logging.Formatter(
		'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	)
	console_formatter = logging.Formatter(
		'%(asctime)s - %(levelname)s - %(message)s'
	)

	# File handler - creates new file daily
	log_file = os.path.join('logs', f'{name}.log')
	file_handler = TimedRotatingFileHandler(
		log_file,
		when='midnight',
		interval=1,
		backupCount=30,  # Keep logs for 30 days
		encoding='utf-8'
	)
	file_handler.setFormatter(file_formatter)
	file_handler.setLevel(logging.INFO)

	# Console handler
	console_handler = logging.StreamHandler()
	console_handler.setFormatter(console_formatter)
	console_handler.setLevel(logging.INFO)

	# Add handlers to logger
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)

	return logger

# Create default logger instance
logger = setup_logger(datetime.now().strftime('%Y-%m-%d'))

if __name__ == '__main__':
	# Example usage
	logger.info('Logger initialized')
	logger.warning('This is a warning message')
	logger.error('This is an error message')
