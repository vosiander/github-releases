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

### Database Setup

The application uses SQLAlchemy with SQLite by default, but supports other databases through configuration.

1. Initialize the database (first time setup):
```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

2. For future database schema changes:
```bash
# After modifying models, create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply the new migration
alembic upgrade head

# To rollback a migration
alembic downgrade -1
```

3. Database Configuration:
   - Default: SQLite database at `github_releases.db`
   - Custom database: Set `GITHUB_RELEASES_DATABASE_URL` environment variable
   
Example database URLs:
```bash
# SQLite (default)
export GITHUB_RELEASES_DATABASE_URL="sqlite:///github_releases.db"

# PostgreSQL
export GITHUB_RELEASES_DATABASE_URL="postgresql://user:password@localhost/dbname"

# MySQL
export GITHUB_RELEASES_DATABASE_URL="mysql://user:password@localhost/dbname"
```

## Usage

The application can be used in two modes: CLI and API server.

### CLI Mode

#### Fetching Releases

Run the command to check releases for tracked repositories:

```bash
github-releases --token <your_token> [--updated-only]
```

Options:
- `--token`: GitHub Personal Access Token (optional)
- `--updated-only`: Show only repositories with new releases

#### Fetching Issue Statuses

Run the command with a list of issue URLs:

```bash
github-releases issues --token <your_token> --issues <issue_urls>
```

Example:
```bash
github-releases issues --token <your_token> --issues "https://github.com/owner/repo/issues/1 https://github.com/owner/repo/issues/2"
```

### API Mode

Start the API server with:

```bash
github-releases serve [OPTIONS]
```

Options:
- `--host`: Host to bind the server to (default: 127.0.0.1)
- `--port`: Port to run the server on (default: 8000)
- `--token`: GitHub token for API operations (optional)

The application uses a database to store repository and tag information. Configure the database connection using the `GITHUB_RELEASES_DATABASE_URL` environment variable.

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
   Returns all tracked repositories and their tags from the database, including previous tags and URLs.

#### API Documentation

When running in API mode, access the interactive API documentation at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Environment Configuration

The application can be configured through environment variables:

```bash
# Server settings
export GITHUB_RELEASES_HOST=127.0.0.1
export GITHUB_RELEASES_PORT=8000
export GITHUB_RELEASES_GITHUB_TOKEN=your_token

# Database settings (optional, defaults to SQLite)
export GITHUB_RELEASES_DATABASE_URL="sqlite:///github_releases.db"
```

CLI options take precedence over environment variables when available.

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
