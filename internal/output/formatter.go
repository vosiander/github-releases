package output

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/vosiander/github-releases/pkg/github"
)

// FormatRelease formats a single release based on the output format
func FormatRelease(release *github.Release, format OutputFormat) (string, error) {
	switch format {
	case FormatJSON:
		return formatJSON(release)
	case FormatText:
		return formatReleaseText(release), nil
	default:
		return "", fmt.Errorf("unsupported output format: %s", format)
	}
}

// FormatBulkResults formats bulk results based on the output format
func FormatBulkResults(results []BulkResult, format OutputFormat) (string, error) {
	switch format {
	case FormatJSON:
		return formatJSON(results)
	case FormatText:
		return formatBulkText(results), nil
	default:
		return "", fmt.Errorf("unsupported output format: %s", format)
	}
}

// formatReleaseText formats a single release as plain text (just the tag)
func formatReleaseText(release *github.Release) string {
	return release.TagName
}

// formatBulkText formats bulk results as plain text
func formatBulkText(results []BulkResult) string {
	var lines []string
	for _, result := range results {
		if result.Error != "" {
			lines = append(lines, fmt.Sprintf("%s: ERROR - %s", result.Repository, result.Error))
		} else {
			lines = append(lines, fmt.Sprintf("%s: %s", result.Repository, result.Tag))
		}
	}
	return strings.Join(lines, "\n")
}

// formatJSON formats data as JSON
func formatJSON(data interface{}) (string, error) {
	jsonBytes, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return "", fmt.Errorf("failed to marshal JSON: %w", err)
	}
	return string(jsonBytes), nil
}
