package bulk

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"sync"

	"github.com/vosiander/github-releases/internal/output"
	"github.com/vosiander/github-releases/pkg/github"
)

// BulkPlugin implements the bulk-get command for fetching multiple repositories
type BulkPlugin struct {
	client *github.Client
}

// New creates a new bulk-get plugin instance
func New(client *github.Client) *BulkPlugin {
	return &BulkPlugin{
		client: client,
	}
}

// Name returns the plugin name
func (p *BulkPlugin) Name() string {
	return "bulk-get"
}

// Description returns the plugin description
func (p *BulkPlugin) Description() string {
	return "Get latest release tags for multiple repositories from a file"
}

// Execute runs the bulk-get command
func (p *BulkPlugin) Execute(args []string, outputFormat string) error {
	if len(args) != 1 {
		return fmt.Errorf("usage: githubrel bulk-get <file>")
	}

	filePath := args[0]
	repositories, err := p.readRepositoriesFromFile(filePath)
	if err != nil {
		return err
	}

	if len(repositories) == 0 {
		return fmt.Errorf("no repositories found in file: %s", filePath)
	}

	// Process repositories concurrently
	results := p.processRepositories(repositories)

	// Format and output the results
	result, err := output.FormatBulkResults(results, output.OutputFormat(outputFormat))
	if err != nil {
		return fmt.Errorf("failed to format output: %w", err)
	}

	fmt.Println(result)
	return nil
}

// readRepositoriesFromFile reads repository names from a file (one per line)
func (p *BulkPlugin) readRepositoriesFromFile(filePath string) ([]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	var repositories []string
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		// Skip empty lines and comments
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		repositories = append(repositories, line)
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("error reading file: %w", err)
	}

	return repositories, nil
}

// processRepositories processes multiple repositories concurrently
func (p *BulkPlugin) processRepositories(repositories []string) []output.BulkResult {
	var wg sync.WaitGroup
	results := make([]output.BulkResult, len(repositories))

	for i, repo := range repositories {
		wg.Add(1)
		go func(index int, repository string) {
			defer wg.Done()
			results[index] = p.processRepository(repository)
		}(i, repo)
	}

	wg.Wait()
	return results
}

// processRepository processes a single repository and returns the result
func (p *BulkPlugin) processRepository(repository string) output.BulkResult {
	owner, repo, err := github.ParseRepository(repository)
	if err != nil {
		return output.BulkResult{
			Repository: repository,
			Error:      err.Error(),
		}
	}

	tag, err := p.client.GetReleaseTag(owner, repo)
	if err != nil {
		return output.BulkResult{
			Repository: repository,
			Error:      err.Error(),
		}
	}

	return output.BulkResult{
		Repository: repository,
		Tag:        tag,
	}
}
