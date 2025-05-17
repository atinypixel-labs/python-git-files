# Python Git Files Tracker

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![uv](https://img.shields.io/badge/uv-0.7.5-orange.svg)](https://github.com/astral-sh/uv)

A Python script that tracks and logs files modified in a GitHub repository within a specified date range. This tool is particularly useful for:
- Tracking file changes across multiple commits
- Generating reports of modified files
- Analyzing repository activity
- Maintaining a history of file modifications

## Features

- 🔍 Tracks files modified in GitHub commits
- 📅 Filters commits by date range
- 📝 Generates daily log files
- 🔄 Handles GitHub API rate limits
- ⚡ Implements retry logic for failed requests
- 📊 Provides detailed logging

## Prerequisites

- Python >=3.13
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- A GitHub account
- A GitHub Personal Access Token

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd python-git-files
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Create and activate a virtual environment using uv:
```bash (optional)
uv venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

## Configuration

1. Copy the environment sample file:
```bash
cp .env.sample .env
```

2. Update the `.env` file with your GitHub credentials:
```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=your_repository_name
GITHUB_REPO_OWNER=your_github_username
GITHUB_REPO_BRANCH=main  # or your default branch
```

3. To create a GitHub Personal Access Token:
   - Go to GitHub Settings > Developer Settings > Personal Access Tokens
   - Generate a new token with `repo` scope
   - Copy the token and paste it in your `.env` file

## Usage

1. Run the script:
```bash
uv run main.py
```

2. The script will:
   - Fetch commits within the specified date range
   - Track modified files in each commit
   - Generate a log file in the `git-files` directory
   - Create detailed logs in the `logs` directory

## Output

The script generates two types of outputs:

1. **Git Files Log** (`git-files/YYYY-MM-DD.txt`):
   - Contains a list of all modified files
   - One file per line
   - Sorted alphabetically
   - Excludes binary files and old versions

2. **Application Logs** (`logs/`):
   - Detailed execution logs
   - API request information
   - Error messages and warnings
   - Rate limit handling

## Customization

You can modify the following parameters in `main.py`:

- `DATE_RANGE`: Change the date range for commit tracking
- `MAX_RETRIES`: Adjust the number of retry attempts for failed requests
- `RATE_LIMIT_DELAY`: Modify the delay between API calls

## Error Handling

The script includes robust error handling for:
- Network issues
- API rate limits
- Invalid configurations
- File system errors

## Logging

Logs are stored in the `logs` directory with:
- Timestamp
- Log level
- Detailed messages
- Error stack traces (if any)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:
1. Check the logs in the `logs` directory
2. Review the error messages
3. Open an issue in the repository

## Best Practices

- Keep your GitHub token secure
- Regularly update your dependencies
- Monitor your API usage
- Back up your log files
- Review the generated files regularly

## Development

This project uses modern Python tooling:
- Python >=3.13 for enhanced performance and features
- `uv` for fast dependency management
- `.env.sample` for environment variable documentation
- Type hints for better code maintainability

---
**Topics**: `python` `github` `git` `api` `logging` `file-tracking` `automation` `uv` `python3.13` `github-api` `file-management` `commit-history` `repository-tools`
