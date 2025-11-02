package github

import (
	"context"
	"fmt"
	"strings"

	"github.com/google/go-github/v58/github"
	"golang.org/x/oauth2"
)

// Client wraps the GitHub API client
type Client struct {
	client *github.Client
	token  string
}

// NewClient creates a new GitHub API client with the provided token
func NewClient(token string) *Client {
	var client *github.Client

	if token != "" {
		ts := oauth2.StaticTokenSource(
			&oauth2.Token{AccessToken: token},
		)
		tc := oauth2.NewClient(context.Background(), ts)
		client = github.NewClient(tc)
	} else {
		client = github.NewClient(nil)
	}

	return &Client{
		client: client,
		token:  token,
	}
}

// GetLatestRelease fetches the latest release for a repository
func (c *Client) GetLatestRelease(owner, repo string) (*Release, error) {
	ctx := context.Background()

	release, resp, err := c.client.Repositories.GetLatestRelease(ctx, owner, repo)
	if err != nil {
		// Check if it's a rate limit error
		if resp != nil && resp.StatusCode == 403 {
			return nil, fmt.Errorf("GitHub API rate limit exceeded. Please set GITHUB_TOKEN environment variable")
		}
		return nil, fmt.Errorf("failed to get latest release: %w", err)
	}

	publishedAt := ""
	if release.PublishedAt != nil {
		publishedAt = release.PublishedAt.Format("2006-01-02T15:04:05Z")
	}

	return &Release{
		Repository:  fmt.Sprintf("%s/%s", owner, repo),
		TagName:     release.GetTagName(),
		Name:        release.GetName(),
		HTMLURL:     release.GetHTMLURL(),
		PublishedAt: publishedAt,
	}, nil
}

// GetReleaseTag fetches just the tag name of the latest release
func (c *Client) GetReleaseTag(owner, repo string) (string, error) {
	release, err := c.GetLatestRelease(owner, repo)
	if err != nil {
		return "", err
	}
	return release.TagName, nil
}

// ParseRepository splits a repository string (owner/repo) into owner and repo
func ParseRepository(repository string) (owner, repo string, err error) {
	parts := strings.Split(strings.TrimSpace(repository), "/")
	if len(parts) != 2 {
		return "", "", fmt.Errorf("invalid repository format: %s (expected format: owner/repo)", repository)
	}

	owner = strings.TrimSpace(parts[0])
	repo = strings.TrimSpace(parts[1])

	if owner == "" || repo == "" {
		return "", "", fmt.Errorf("invalid repository format: %s (owner and repo cannot be empty)", repository)
	}

	return owner, repo, nil
}
