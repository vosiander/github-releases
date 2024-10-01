# GitHub Latest Release Fetcher

A Python script that fetches the latest releases from specified GitHub repositories. It uses the GitHub API and provides the ability to display the results in a well-formatted table using the `rich` library. The script allows you to specify a list of repositories and fetch the latest release details for each one.

## Features

- Fetch the latest releases from GitHub repositories.
- Display the releases in a clean, colorful table using `rich`.
- Supports GitHub Personal Access Token (PAT) for authenticated requests.
- Handles multiple repositories from a text file input.
- Provides progress tracking while fetching release data.

## Requirements

- Python 3.7+
- GitHub Personal Access Token (optional for private repositories)

### Dependencies

The script uses the following Python packages:

- `argparse` - For argument parsing.
- `rich` - For creating beautifully formatted tables.
- `colorama` - For color output in terminal.
- `loguru` - For logging (optional, can be enhanced for detailed logs).
- `requests` - For making HTTP requests to the GitHub API.

Install the required dependencies via `pip`:

```bash
pip install argparse rich colorama loguru requests
```

## Usage

1. Create a `.txt` file containing a list of GitHub repositories in the following format:

    ```
    owner/repo
    ```

    Example:

    ```
    microsoft/vscode
    torvalds/linux
    ```

2. Run the script, specifying the token (if needed) and the text file containing repositories:

    ```bash
    python github_release_fetcher.py --token <your_token> --repos <path_to_repos_file>
    ```

   If no GitHub token is provided, the script will make unauthenticated requests, which have lower rate limits.

### Example

```bash
python github_release_fetcher.py --token your_token --repos repos.txt
```

### Output

The script will print a formatted table like this:

```
┌─────────────────────────┬──────────────┬─────────────────────────────────────────────────────────────┐
│ Repository              │ Tag          │ URL                                                         │
├─────────────────────────┼──────────────┼─────────────────────────────────────────────────────────────┤
│ microsoft/vscode        │ v1.59.1      │ https://github.com/microsoft/vscode/releases/tag/v1.59.1     │
│ torvalds/linux          │ v5.14        │ https://github.com/torvalds/linux/releases/tag/v5.14         │
└─────────────────────────┴──────────────┴─────────────────────────────────────────────────────────────┘
```

If the latest release cannot be fetched, an error message will be printed.

## Notes

- **Rate Limiting**: Unauthenticated requests to the GitHub API are limited to 60 requests per hour. If you need to make more requests, use a GitHub Personal Access Token.
- **Private Repositories**: A token is required to access private repositories.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions

Feel free to open issues, suggest features, or contribute to this project via pull requests. All contributions are welcome!