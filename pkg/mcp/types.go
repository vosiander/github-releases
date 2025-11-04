package mcp

// GetReleaseInput represents input for the get_release tool
type GetReleaseInput struct {
	Repository string `json:"repository" jsonschema:"GitHub repository in owner repo format"`
}

// BulkReleasesInput represents input for the bulk_releases tool
type BulkReleasesInput struct {
	Repositories []string `json:"repositories" jsonschema:"Array of GitHub repositories in owner-repo format"`
}

// HistoryEntry represents a single repository with its historical version
type HistoryEntry struct {
	Repository string `json:"repository" jsonschema:"GitHub repository in owner-repo format"`
	Version    string `json:"version" jsonschema:"Historical version tag to compare against"`
}

// CompareHistoryInput represents input for the compare_history tool
type CompareHistoryInput struct {
	Entries []HistoryEntry `json:"entries" jsonschema:"Array of repositories with their historical versions"`
}

// ReleaseOutput represents the output of a single release query
type ReleaseOutput struct {
	Repository  string `json:"repository"`
	TagName     string `json:"tag_name"`
	Name        string `json:"name"`
	HTMLURL     string `json:"html_url"`
	PublishedAt string `json:"published_at"`
}

type BulkReleaseResult struct {
	BulkReleases []BulkReleaseResultEntry `json:"bulk_releases"`
}

// BulkReleaseResultEntry represents a single result in bulk operations
type BulkReleaseResultEntry struct {
	Repository string `json:"repository"`
	Tag        string `json:"tag,omitempty"`
	Error      string `json:"error,omitempty"`
}

// HistoryComparisonResult
type HistoryComparisonResult struct {
	HistoryComparisonResultEntry []HistoryComparisonResultEntry `json:"history_comparisons"`
}

// HistoryComparisonResultEntryrepresents a single comparison result
type HistoryComparisonResultEntry struct {
	Repository        string `json:"repository"`
	HistoricalVersion string `json:"historical_version"`
	CurrentVersion    string `json:"current_version,omitempty"`
	HasUpdate         bool   `json:"has_update"`
	Error             string `json:"error,omitempty"`
}
