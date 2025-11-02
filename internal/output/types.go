package output

// OutputFormat represents the output format type
type OutputFormat string

const (
	// FormatText outputs in plain text format (default)
	FormatText OutputFormat = "text"
	// FormatJSON outputs in JSON format
	FormatJSON OutputFormat = "json"
)

// BulkResult represents the result of processing a single repository in bulk operations
type BulkResult struct {
	Repository string `json:"repository"`
	Tag        string `json:"tag,omitempty"`
	Error      string `json:"error,omitempty"`
}

// HistoryResult represents the result of comparing historical version with current release
type HistoryResult struct {
	Repository        string `json:"repository"`
	HistoricalVersion string `json:"historical_version"`
	CurrentVersion    string `json:"current_version,omitempty"`
	HasUpdate         bool   `json:"has_update"`
	Error             string `json:"error,omitempty"`
}
