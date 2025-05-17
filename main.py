# --- Imports

import requests
import os
import time
from typing import List, Tuple
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
from logger import logger

# --- Configs

@dataclass
class Config:
	GITHUB_TOKEN: str
	GITHUB_REPO: str
	GITHUB_REPO_OWNER: str
	GITHUB_REPO_BRANCH: str
	GITHUB_API_URL: str
	DATE_RANGE: Tuple[datetime, datetime]
	MAX_RETRIES: int = 3
	RETRY_DELAY: int = 2
	RATE_LIMIT_DELAY: int = 1

def load_config() -> Config:
	load_dotenv()

	return Config(
		GITHUB_TOKEN=os.getenv('GITHUB_TOKEN'),
		GITHUB_REPO=os.getenv('GITHUB_REPO'),
		GITHUB_REPO_OWNER=os.getenv('GITHUB_REPO_OWNER'),
		GITHUB_REPO_BRANCH=os.getenv('GITHUB_REPO_BRANCH'),
		GITHUB_API_URL=f'https://api.github.com/repos/{os.getenv("GITHUB_REPO_OWNER")}/{os.getenv("GITHUB_REPO")}/commits',
		DATE_RANGE=(datetime(2024, 3, 12), datetime.today())  # Updated to current year
	)

# --- Utils

def handle_rate_limit(response: requests.Response) -> None:
	"""Handle GitHub API rate limiting"""
	if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
		reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
		wait_time = max(reset_time - time.time(), 0)
		if wait_time > 0:
			logger.warning(f'Rate limit reached. Waiting {wait_time:.0f} seconds...')
			time.sleep(wait_time)

def make_request(url: str, headers: dict, params: dict = None, max_retries: int = 3) -> requests.Response:
	"""Make HTTP request with retry logic"""
	for attempt in range(max_retries):
		try:
			response = requests.get(url, headers=headers, params=params)
			handle_rate_limit(response)
			response.raise_for_status()
			return response
		except requests.exceptions.RequestException as e:
			if attempt == max_retries - 1:
				raise
			logger.warning(f'Request failed (attempt {attempt + 1}/{max_retries}): {str(e)}')
			time.sleep(2 ** attempt)  # Exponential backoff

# --- Scripts

def get_commit_urls(config: Config) -> List[str]:
	"""Get commit URLs within date range"""
	logger.info('Getting commit urls...')
	headers = {'Authorization': f'Bearer {config.GITHUB_TOKEN}'}
	params = {
		'since': config.DATE_RANGE[0].strftime('%Y-%m-%d'),
		'until': config.DATE_RANGE[1].strftime('%Y-%m-%d'),
		'per_page': 100,
	}

	urls = []
	page = 1

	while True:
		logger.info(f'>> Fetching data for page {page}')
		params['page'] = page
		response = make_request(config.GITHUB_API_URL, headers, params)
		data = response.json()

		if not data:
			break

		urls.extend([
			commit['url'] for commit in data
			if commit['author']['login'] == config.GITHUB_REPO_OWNER
		])
		page += 1
		time.sleep(config.RATE_LIMIT_DELAY)  # Respect rate limits

	logger.info(f'Fetched commit urls. Total: {len(urls)}')
	return urls

def get_commit_files(url: str, config: Config) -> List[str]:
	"""Get files modified in a commit"""
	logger.info(f'>> Fetching files for commit {url}')
	headers = {'Authorization': f'Bearer {config.GITHUB_TOKEN}'}

	response = make_request(url, headers)
	files = response.json()['files']

	filenames = []
	for file in files:
		filename = file['filename']
		if any(filename.endswith(ext) for ext in ['.pyc', '.pyo', '.pdf']) or 'old' in filename:
			continue
		if filename not in filenames:
			filenames.append(filename)

	logger.info(f'Fetched files for commit -> Total: {len(filenames)}')
	return filenames

def get_commits_files(urls: List[str], config: Config) -> List[str]:
	"""Get all files modified in commits"""
	logger.info('========================================')
	logger.info('Fetching files for commits')

	files = set()  # Use set for automatic deduplication
	for url in urls:
		files.update(get_commit_files(url, config))
		time.sleep(config.RATE_LIMIT_DELAY)  # Respect rate limits

	logger.info(f'Fetched files for commits. Total: {len(files)}')
	return sorted(list(files))  # Return sorted list for consistent output

def write_files_to_file(files: List[str]) -> None:
	"""Write files to output file"""
	logger.info('========================================')
	logger.info('Writing files to file')

	os.makedirs('git-files', exist_ok=True)
	filename = f'{datetime.now().strftime("%Y-%m-%d")}.txt'

	with open(os.path.join('git-files', filename), 'w') as f:
		f.write('\n'.join(files))

	logger.info(f'Files written to file -> {filename}')

def main():
	"""Main execution function"""
	try:
		config = load_config()

		# Validate required environment variables
		if not all([config.GITHUB_TOKEN, config.GITHUB_REPO, config.GITHUB_REPO_OWNER]):
			raise ValueError("Missing required environment variables")

		commit_urls = get_commit_urls(config)
		commit_files = get_commits_files(commit_urls, config)
		write_files_to_file(commit_files)

		logger.info('Script completed successfully')

	except Exception as e:
		logger.error(f'Script failed: {str(e)}')
		raise

if __name__ == '__main__':
	main()
