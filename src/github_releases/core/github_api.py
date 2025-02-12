"""
title: GitHub API Tools
author: open-webui
date: 2024-05-30
version: 1.0
license: MIT
description: A set of tools for interacting with the GitHub API, including fetching release and issue information.
requirements: requests, loguru
"""

import os
import requests
from datetime import datetime
from loguru import logger

class Tools:
    def __init__(self):
        pass

    class Github:
        def __init__(self, token=None):
            """
            Initialize the Github object. An optional token can be provided for authenticated requests.

            :param token: Github Personal Access Token (optional)
            """
            logger.trace(
                "Initializing Github object with token: {}",
                "provided" if token else "not provided",
            )
            self.base_url = "https://api.github.com"
            self.headers = {
                "Authorization": f"token {token}" if token else None,
                "Accept": "application/vnd.github.v3+json",
            }

        def get_latest_release(self, owner, repo):
            """
            Fetches the latest release from a Github repository.

            :param owner: The owner of the repository.
            :param repo: The name of the repository.
            :return: A dictionary containing release details, or None if the request fails.
            """
            url = f"{self.base_url}/repos/{owner}/{repo}/releases/latest"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                latest_release = response.json()
                return {
                    "tag_name": latest_release["tag_name"],
                    "name": latest_release["name"],
                    "published_at": latest_release["published_at"],
                    "html_url": latest_release["html_url"],
                    "body": latest_release["body"],
                }
            else:
                return None

        def get_issue_status(self, issue_path):
            """
            Fetches the status of a specific issue from a Github repository.

            :param issue_path: A string in the format 'owner/repo/issues/issue_number'.
            :return: A dictionary containing issue status, name, published date, and last activity or comment.
            """
            try:
                owner, repo, _, issue_number = issue_path.split('/')
                url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
                response = requests.get(url, headers=self.headers)

                if response.status_code == 200:
                    issue = response.json()
                    comments_url = issue["comments_url"]
                    comments_response = requests.get(comments_url, headers=self.headers)
                    comments = comments_response.json() if comments_response.status_code == 200 else []

                    return {
                        "status": issue["state"],
                        "name": issue["title"],
                        "published_at": issue["created_at"],
                        "last_activity": issue["updated_at"],
                        "last_comment": comments[-1]["body"] if comments else "No comments"
                    }
                else:
                    logger.warning(f"Failed to fetch issue details for {issue_path}. Status code: {response.status_code}")
                    return None
            except Exception as e:
                logger.error(f"Error fetching issue status: {e}")
                return None
