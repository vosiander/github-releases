package get

import (
	"fmt"

	"github.com/vosiander/github-releases/internal/output"
	"github.com/vosiander/github-releases/pkg/github"
)

// GetPlugin implements the get command for fetching a single repository's latest release
type GetPlugin struct {
	client *github.Client
}

// New creates a new get plugin instance
func New(client *github.Client) *GetPlugin {
	return &GetPlugin{
		client: client,
	}
}

// Name returns the plugin name
func (p *GetPlugin) Name() string {
	return "get"
}

// Description returns the plugin description
func (p *GetPlugin) Description() string {
	return "Get the latest release tag for a single repository"
}

// Execute runs the get command
func (p *GetPlugin) Execute(args []string, outputFormat string) error {
	if len(args) != 1 {
		return fmt.Errorf("usage: githubrel get <owner/repo>")
	}

	repository := args[0]
	owner, repo, err := github.ParseRepository(repository)
	if err != nil {
		return err
	}

	release, err := p.client.GetLatestRelease(owner, repo)
	if err != nil {
		return err
	}

	// Format and output the result
	result, err := output.FormatRelease(release, output.OutputFormat(outputFormat))
	if err != nil {
		return fmt.Errorf("failed to format output: %w", err)
	}

	fmt.Println(result)
	return nil
}
