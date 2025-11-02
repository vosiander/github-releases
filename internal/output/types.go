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
