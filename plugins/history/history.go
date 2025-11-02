package history

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"sync"

	"github.com/vosiander/github-releases/internal/output"
	"github.com/vosiander/github-releases/pkg/github"
)

// HistoryPlugin implements the history command for comparing historical versions
type HistoryPlugin struct {
	client *github.Client
}

// New creates a new history plugin instance
func New(client *github.Client) *HistoryPlugin {
	return &HistoryPlugin{
		client: client,
	}
}

// Name returns the plugin name
func (p *HistoryPlugin) Name() string {
	return "history"
}

// Description returns the plugin description
func (p *HistoryPlugin) Description() string {
	return "Compare historical versions with current releases from a history file"
}

// HistoryEntry represents a repository with its historical version
type HistoryEntry struct {
	Repository        string
	HistoricalVersion string
}

// Execute runs the history command
func (p *HistoryPlugin) Execute(args []string, outputFormat string) error {
	if len(args) != 1 {
		return fmt.Errorf("usage: githubrel history <file>")
	}

	filePath := args[0]
	entries, err := p.readHistoryFile(filePath)
	if err != nil {
		return err
	}

	if len(entries) == 0 {
		return fmt.Errorf("no entries found in file: %s", filePath)
	}

	// Process entries concurrently
	results := p.processHistoryEntries(entries)

	// Format and output the results
	result, err := output.FormatHistoryResults(results, output.OutputFormat(outputFormat))
	if err != nil {
		return fmt.Errorf("failed to format output: %w", err)
	}

	fmt.Println(result)
	return nil
}

// readHistoryFile reads history entries from a file (repo:version format)
func (p *HistoryPlugin) readHistoryFile(filePath string) ([]HistoryEntry, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	var entries []HistoryEntry
	scanner := bufio.NewScanner(file)
	lineNum := 0

	for scanner.Scan() {
		lineNum++
		line := strings.TrimSpace(scanner.Text())

		// Skip empty lines and comments
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}

		// Parse repo:version format
		parts := strings.SplitN(line, ":", 2)
		if len(parts) != 2 {
			return nil, fmt.Errorf("invalid format at line %d: expected 'repo:version', got '%s'", lineNum, line)
		}

		repository := strings.TrimSpace(parts[0])
		version := strings.TrimSpace(parts[1])

		if repository == "" || version == "" {
			return nil, fmt.Errorf("invalid entry at line %d: repository and version cannot be empty", lineNum)
		}

		entries = append(entries, HistoryEntry{
			Repository:        repository,
			HistoricalVersion: version,
		})
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("error reading file: %w", err)
	}

	return entries, nil
}

// processHistoryEntries processes multiple history entries concurrently
func (p *HistoryPlugin) processHistoryEntries(entries []HistoryEntry) []output.HistoryResult {
	var wg sync.WaitGroup
	results := make([]output.HistoryResult, len(entries))

	for i, entry := range entries {
		wg.Add(1)
		go func(index int, e HistoryEntry) {
			defer wg.Done()
			results[index] = p.processHistoryEntry(e)
		}(i, entry)
	}

	wg.Wait()
	return results
}

// processHistoryEntry processes a single history entry
func (p *HistoryPlugin) processHistoryEntry(entry HistoryEntry) output.HistoryResult {
	owner, repo, err := github.ParseRepository(entry.Repository)
	if err != nil {
		return output.HistoryResult{
			Repository:        entry.Repository,
			HistoricalVersion: entry.HistoricalVersion,
			Error:             err.Error(),
		}
	}

	currentTag, err := p.client.GetReleaseTag(owner, repo)
	if err != nil {
		return output.HistoryResult{
			Repository:        entry.Repository,
			HistoricalVersion: entry.HistoricalVersion,
			Error:             err.Error(),
		}
	}

	// Determine if there's an update
	hasUpdate := currentTag != entry.HistoricalVersion

	return output.HistoryResult{
		Repository:        entry.Repository,
		HistoricalVersion: entry.HistoricalVersion,
		CurrentVersion:    currentTag,
		HasUpdate:         hasUpdate,
	}
}
