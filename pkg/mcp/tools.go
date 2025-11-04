package mcp

import (
	"context"
	"fmt"
	"sync"

	"github.com/vosiander/github-releases/pkg/github"
)

// HandleGetRelease handles the get_release tool request
func HandleGetRelease(ctx context.Context, client *github.Client, input GetReleaseInput) (*ReleaseOutput, error) {
	// Validate repository format
	owner, repo, err := github.ParseRepository(input.Repository)
	if err != nil {
		return nil, fmt.Errorf("invalid repository format: %w", err)
	}

	// Get the latest release
	release, err := client.GetLatestRelease(owner, repo)
	if err != nil {
		return nil, fmt.Errorf("failed to get latest release for %s: %w", input.Repository, err)
	}

	// Transform to output format
	output := &ReleaseOutput{
		Repository:  release.Repository,
		TagName:     release.TagName,
		Name:        release.Name,
		HTMLURL:     release.HTMLURL,
		PublishedAt: release.PublishedAt,
	}

	return output, nil
}

// HandleBulkReleases handles the bulk_releases tool request
func HandleBulkReleases(ctx context.Context, client *github.Client, input BulkReleasesInput) (*BulkReleaseResult, error) {
	if len(input.Repositories) == 0 {
		return nil, fmt.Errorf("no repositories provided")
	}

	// Process repositories concurrently
	var wg sync.WaitGroup
	results := make([]BulkReleaseResultEntry, len(input.Repositories))

	for i, repository := range input.Repositories {
		wg.Add(1)
		go func(index int, repo string) {
			defer wg.Done()
			results[index] = processBulkRepository(client, repo)
		}(i, repository)
	}

	wg.Wait()
	return &BulkReleaseResult{BulkReleases: results}, nil
}

// processBulkRepository processes a single repository for bulk operations
func processBulkRepository(client *github.Client, repository string) BulkReleaseResultEntry {
	owner, repo, err := github.ParseRepository(repository)
	if err != nil {
		return BulkReleaseResultEntry{}
	}

	tag, err := client.GetReleaseTag(owner, repo)
	if err != nil {
		return BulkReleaseResultEntry{
			Repository: repository,
			Error:      err.Error(),
		}
	}

	return BulkReleaseResultEntry{
		Repository: repository,
		Tag:        tag,
	}
}

// HandleCompareHistory handles the compare_history tool request
func HandleCompareHistory(ctx context.Context, client *github.Client, input CompareHistoryInput) (*HistoryComparisonResult, error) {
	if len(input.Entries) == 0 {
		return nil, fmt.Errorf("no entries provided")
	}

	// Process entries concurrently
	var wg sync.WaitGroup
	results := make([]HistoryComparisonResultEntry, len(input.Entries))

	for i, entry := range input.Entries {
		wg.Add(1)
		go func(index int, e HistoryEntry) {
			defer wg.Done()
			results[index] = processHistoryEntry(client, e)
		}(i, entry)
	}

	wg.Wait()
	return &HistoryComparisonResult{HistoryComparisonResultEntry: results}, nil
}

// processHistoryEntry processes a single history entry
func processHistoryEntry(client *github.Client, entry HistoryEntry) HistoryComparisonResultEntry {
	owner, repo, err := github.ParseRepository(entry.Repository)
	if err != nil {
		return HistoryComparisonResultEntry{
			Repository:        entry.Repository,
			HistoricalVersion: entry.Version,
			HasUpdate:         false,
			Error:             err.Error(),
		}
	}

	currentTag, err := client.GetReleaseTag(owner, repo)
	if err != nil {
		return HistoryComparisonResultEntry{
			Repository:        entry.Repository,
			HistoricalVersion: entry.Version,
			HasUpdate:         false,
			Error:             err.Error(),
		}
	}

	// Determine if there's an update
	hasUpdate := currentTag != entry.Version

	return HistoryComparisonResultEntry{
		Repository:        entry.Repository,
		HistoricalVersion: entry.Version,
		CurrentVersion:    currentTag,
		HasUpdate:         hasUpdate,
	}
}
