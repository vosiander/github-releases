# GitHub Latest Release Fetcher

A Python application that fetches the latest releases from specified GitHub repositories. It provides both a CLI interface and a REST API, allowing you to track repository releases and manage them programmatically.

## Features

- Dual interface: CLI tool and REST API
- Fetch the latest releases from GitHub repositories
- Track and compare release tags with history
- Display releases in a clean, colorful table (CLI mode)
- Fetch and display issue statuses
- RESTful API endpoints for programmatic access
- Supports GitHub Personal Access Token (PAT)

## Requirements

- Python 3.12+
- GitHub Personal Access Token (optional for private repositories)

### Installation

To set up the development environment, use `uv` to manage dependencies:

```bash
uv sync
```

To install the package directly from GitHub, use `pip`:

```bash
pip install git+https://github.com/yourusername/github-releases.git
```

## Usage

The application can be used in two modes: CLI and API server.

### CLI Mode

#### Fetching Releases

1. Create a `.txt` file containing a list of GitHub repositories in the following format:

    ```
    owner/repo
    ```

    Example:
    ```
    microsoft/vscode
    torvalds/linux
    ```

2. Run the command:

    ```bash
    github-releases --token <your_token> --repos <path_to_repos_file> [--history <path_to_history_file>] [--updated-only]
    ```

   Options:
   - `--token`: GitHub Personal Access Token (optional)
   - `--history`: Path to history file for tracking changes
   - `--updated-only`: Show only repositories with new releases

#### Fetching Issue Statuses

1. Create a `.txt` file with GitHub issue URLs:

    ```
    https://github.com/owner/repo/issues/issue_number
    ```

2. Run the command:

    ```bash
    github-releases issues --token <your_token> --issues_file <path_to_issues_file>
    ```

### API Mode

Start the API server with:

```bash
github-releases serve [--host HOST] [--port PORT] [--token TOKEN]
```

Options:
- `--host`: Host to bind the server to (default: 127.0.0.1)
- `--port`: Port to run the server on (default: 8000)
- `--token`: GitHub token for API operations (optional)

#### API Endpoints

1. Add New Repository
   ```http
   POST /api/repositories
   Content-Type: application/json

   {
     "repository": "owner/repo"
   }
   ```

2. Refresh Repository Tags
   ```http
   POST /api/repositories/refresh
   ```
   Updates all repositories and returns their current tags.

3. Get Repository Tag
   ```http
   GET /api/repositories/{owner}/{repo}/tag
   ```
   Returns the latest tag for a specific repository.

4. Get History
   ```http
   GET /api/repositories/history
   ```
   Returns all tracked repositories and their saved tags from the history file.

#### API Documentation

When running in API mode, access the interactive API documentation at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Environment Configuration

Configure the application using environment variables:

```bash
# GitHub API token for authentication
export GITHUB_RELEASES_GITHUB_TOKEN=your_token

# API server settings (optional)
export GITHUB_RELEASES_HOST=127.0.0.1
export GITHUB_RELEASES_PORT=8000
```

### Example Output (CLI Mode)

The CLI displays a formatted table with release information:

```
┌──────────────────────┬─────────┬──────────────┬──────────┬────────────────────────────┐
│ Repository           │ Tag     │ Previous Tag │ Changed? │ URL                        │
├──────────────────────┼─────────┼──────────────┼──────────┼────────────────────────────┤
│ microsoft/vscode     │ v1.2.0  │ v1.1.0       │ X        │ https://github.com/...     │
│ torvalds/linux      │ v6.1    │ v6.0         │ X        │ https://github.com/...     │
└──────────────────────┴─────────┴──────────────┴──────────┴────────────────────────────┘
```

## Notes

- **Rate Limiting**: Unauthenticated requests are limited to 60/hour. Use a token for higher limits.
- **Private Repositories**: Require a GitHub Personal Access Token.
- **API Server**: Runs on localhost by default. Configure host/port via environment variables.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Feel free to open issues, suggest features, or contribute via pull requests. All contributions are welcome!
