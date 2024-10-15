# GitHub Latest Release Fetcher

A Python script that fetches the latest releases from specified GitHub repositories. It uses the GitHub API and provides the ability to display the results in a well-formatted table using the `rich` library. The script allows you to specify a list of repositories and fetch the latest release details for each one.

## Features

- Fetch the latest releases from GitHub repositories.
- Display the releases in a clean, colorful table using `rich`.
- Supports GitHub Personal Access Token (PAT) for authenticated requests.
- Handles multiple repositories from a text file input.
- Provides progress tracking while fetching release data.
- Fetch and display issue statuses from GitHub repositories.

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

### Fetching Releases

1. Create a `.txt` file containing a list of GitHub repositories in the following format:

    ```
    owner/repo
    ```

    Example:

    ```
    microsoft/vscode
    torvalds/linux
    ```

2. Run the script using the command line, specifying the token (if needed) and the text file containing repositories:

    ```bash
    github-releases --token <your_token> --repos <path_to_repos_file>
    ```

   If no GitHub token is provided, the script will make unauthenticated requests, which have lower rate limits.

### Fetching Issue Statuses

1. Create a `.txt` file containing a list of GitHub issue URLs in the following format:

    ```
    https://github.com/owner/repo/issues/issue_number
    ```

    Example:

    ```
    https://github.com/microsoft/vscode/issues/12345
    https://github.com/torvalds/linux/issues/67890
    ```

2. Run the script using the command line, specifying the token (if needed) and the text file containing issue URLs:

    ```bash
    github-releases issues --token <your_token> --issues_file <path_to_issues_file>
    ```

   If no GitHub token is provided, the script will make unauthenticated requests, which have lower rate limits.

### Example

```bash
github-releases issues --token your_token --issues_file issues.txt
```

### Output

The script will print a formatted table with issue details like this:

```
┌──────────────────────────────────────────────┬──────────────┬─────────────────────────────────────────────┐
│ Issue URL                                    │ Status       │ Name                                        │
├──────────────────────────────────────────────┼──────────────┼─────────────────────────────────────────────┤
│ https://github.com/microsoft/vscode/issues/1 │ open         │ Issue Title                                 │
│ https://github.com/torvalds/linux/issues/2   │ closed       │ Another Issue Title                         │
└──────────────────────────────────────────────┴──────────────┴─────────────────────────────────────────────┘
```

If the issue status cannot be fetched, an error message will be printed.

## Notes

- **Rate Limiting**: Unauthenticated requests to the GitHub API are limited to 60 requests per hour. If you need to make more requests, use a GitHub Personal Access Token.
- **Private Repositories**: A token is required to access private repositories.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions

Feel free to open issues, suggest features, or contribute to this project via pull requests. All contributions are welcome!
