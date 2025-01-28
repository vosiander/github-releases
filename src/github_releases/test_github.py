from github_releases.github_api import Tools

def test_get_issue_status():
    # Example issue path
    issue_path = "open-webui/open-webui/issues/6190"
    
    # Initialize Github object without a token for public repositories
    github = Tools.Github()
    
    # Fetch issue status
    issue_status = github.get_issue_status(issue_path)
    
    # Print the results
    if issue_status:
        print("Issue Status:", issue_status["status"])
        print("Issue Name:", issue_status["name"])
        print("Published At:", issue_status["published_at"])
        print("Last Activity:", issue_status["last_activity"])
        print("Last Comment:", issue_status["last_comment"])
    else:
        print("Failed to fetch issue status.")

def test_get_latest_release():
    # Example repository
    owner = "microsoft"
    repo = "vscode"
    
    # Initialize Github object without a token for public repositories
    github = Tools.Github()
    
    # Fetch latest release
    latest_release = github.get_latest_release(owner, repo)
    
    # Print the results
    if latest_release:
        print("Latest Release Tag:", latest_release["tag_name"])
        print("Release Name:", latest_release["name"])
        print("Published At:", latest_release["published_at"])
        print("Release URL:", latest_release["html_url"])
    else:
        print("Failed to fetch latest release.")

if __name__ == "__main__":
    test_get_issue_status()
    test_get_latest_release()
