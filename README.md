# GitHub Releases Tracker

A CLI tool to fetch and track GitHub release tags from repositories. Built with Go, featuring a plugin-based architecture for extensibility.

## Features

- **Single Repository**: Fetch the latest release tag for a specific repository
- **Bulk Operations**: Process multiple repositories from a file
- **Flexible Output**: Support for text (default) and JSON formats
- **Plugin Architecture**: Easily extensible with new commands
- **No Database**: Always fetches fresh data from GitHub API
- **Concurrent Processing**: Bulk operations process repositories concurrently

## Installation

### Build from Source

```bash
go build -o githubrel ./cmd/githubrel
```

### Install with Go

```bash
go install github.com/vosiander/github-releases/cmd/githubrel@latest
```

## Usage

### Authentication

Set your GitHub token as an environment variable for higher API rate limits:

```bash
export GITHUB_TOKEN=your_token_here
```

Without a token, you're limited to 60 requests per hour. With authentication, you get 5,000 requests per hour.

### Commands

#### Get Single Repository

Fetch the latest release tag for a single repository:

```bash
# Text output (default)
githubrel get owner/repo

# JSON output
githubrel get owner/repo --output json
```

**Examples:**

```bash
$ githubrel get spf13/cobra
v1.10.1

$ githubrel get spf13/cobra --output json
{
  "repository": "spf13/cobra",
  "tag_name": "v1.10.1",
  "name": "v1.10.1",
  "html_url": "https://github.com/spf13/cobra/releases/tag/v1.10.1",
  "published_at": "2025-09-01T16:32:42Z"
}
```

#### Bulk Get

Process multiple repositories from a file:

```bash
# Text output (default)
githubrel bulk-get repos.txt

# JSON output
githubrel bulk-get repos.txt --output json
```

**File Format:**

Create a text file with one repository per line:

```text
# repos.txt - Comments start with #
owner/repo1
owner/repo2
another-owner/repo3
```

**Examples:**

```bash
$ cat repos.txt
spf13/cobra
google/go-github

$ githubrel bulk-get repos.txt
spf13/cobra: v1.10.1
google/go-github: v76.0.0

$ githubrel bulk-get repos.txt --output json
[
  {
    "repository": "spf13/cobra",
    "tag": "v1.10.1"
  },
  {
    "repository": "google/go-github",
    "tag": "v76.0.0"
  }
]
```

#### Other Commands

```bash
# Show version
githubrel version

# Show help
githubrel --help
githubrel get --help
githubrel bulk-get --help
```

## Architecture

### Plugin System

The tool uses a plugin-based architecture where each command is implemented as a plugin. This makes it easy to add new commands without modifying the core CLI framework.

**Plugin Interface:**

```go
type Plugin interface {
    Name() string
    Description() string
    Execute(args []string, outputFormat string) error
}
```

**Available Plugins:**
- `get`: Fetch latest release for a single repository
- `bulk-get`: Process multiple repositories from a file

### Project Structure

```
githubrel/
├── cmd/githubrel/         # CLI entry point
│   └── main.go
├── pkg/github/            # GitHub API client
│   ├── client.go
│   ├── types.go
│   └── client_test.go
├── plugins/               # Plugin system
│   ├── plugin.go          # Plugin interface
│   ├── registry.go        # Plugin registry
│   ├── get/              # Get plugin
│   │   └── get.go
│   └── bulk/             # Bulk-get plugin
│       └── bulk.go
├── internal/output/       # Output formatting
│   ├── formatter.go
│   ├── types.go
│   └── formatter_test.go
└── testdata/             # Test data
    └── repos.txt
```

## Development

### Prerequisites

- Go 1.21 or later
- GitHub personal access token (optional, for higher rate limits)

### Dependencies

- `github.com/google/go-github/v58` - GitHub API client
- `github.com/spf13/cobra` - CLI framework
- `golang.org/x/oauth2` - OAuth2 authentication

### Testing

```bash
# Run all tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Run tests with race detection
go test -race ./...
```

### Building

```bash
# Build for current platform
go build -o githubrel ./cmd/githubrel

# Build for specific platforms
GOOS=linux GOARCH=amd64 go build -o githubrel-linux-amd64 ./cmd/githubrel
GOOS=darwin GOARCH=arm64 go build -o githubrel-darwin-arm64 ./cmd/githubrel
GOOS=windows GOARCH=amd64 go build -o githubrel-windows-amd64.exe ./cmd/githubrel
```

## Error Handling

The tool provides clear error messages for common scenarios:

- **Invalid repository format**: Repository must be in `owner/repo` format
- **Repository not found**: HTTP 404 errors from GitHub API
- **Rate limit exceeded**: Suggests setting `GITHUB_TOKEN` environment variable
- **File not found**: Clear message when bulk-get file doesn't exist
- **No releases**: Repositories without releases show appropriate error

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! To add a new plugin:

1. Create a new package under `plugins/`
2. Implement the `Plugin` interface
3. Register the plugin in `cmd/githubrel/main.go`
4. Add tests for the new functionality

## Releases

### Creating a Release

To create a new release with pre-built binaries:

1. Create and push a git tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. GitHub Actions will automatically:
   - Build binaries for multiple platforms (Linux, macOS, Windows)
   - Support multiple architectures (amd64, arm64, arm)
   - Generate SHA256 checksums for each binary
   - Create a GitHub release with all artifacts
   - Include auto-generated release notes

### Available Binaries

The release workflow builds the following binaries:
- `githubrel-linux-amd64`
- `githubrel-linux-arm64`
- `githubrel-linux-armv7`
- `githubrel-darwin-amd64` (Intel Mac)
- `githubrel-darwin-arm64` (Apple Silicon)
- `githubrel-windows-amd64.exe`
- `githubrel-windows-arm64.exe`

Each binary includes a `.sha256` file for integrity verification.

## Changelog

### Version 1.0.0

- Complete rewrite from Python to Go
- Plugin-based architecture
- Concurrent bulk processing
- JSON and text output formats
- No database dependencies
- Comprehensive error handling
- Automated release builds for multiple platforms
