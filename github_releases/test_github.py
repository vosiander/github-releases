from github_releases.main import Github

def test_get_issue_status():
    # Example issue path
    issue_path = "open-webui/open-webui/issues/6190"
    
    # Initialize Github object without a token for public repositories
    github = Github()
    
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

if __name__ == "__main__":
    test_get_issue_status()
