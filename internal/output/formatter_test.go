package output

import (
	"encoding/json"
	"strings"
	"testing"

	"github.com/vosiander/github-releases/pkg/github"
)

func TestFormatRelease(t *testing.T) {
	release := &github.Release{
		Repository:  "owner/repo",
		TagName:     "v1.2.3",
		Name:        "Release 1.2.3",
		HTMLURL:     "https://github.com/owner/repo/releases/tag/v1.2.3",
		PublishedAt: "2023-01-01T12:00:00Z",
	}

	t.Run("text format", func(t *testing.T) {
		result, err := FormatRelease(release, FormatText)
		if err != nil {
			t.Fatalf("FormatRelease() error = %v", err)
		}
		if result != "v1.2.3" {
			t.Errorf("FormatRelease() = %v, want v1.2.3", result)
		}
	})

	t.Run("json format", func(t *testing.T) {
		result, err := FormatRelease(release, FormatJSON)
		if err != nil {
			t.Fatalf("FormatRelease() error = %v", err)
		}

		var decoded github.Release
		if err := json.Unmarshal([]byte(result), &decoded); err != nil {
			t.Fatalf("Failed to parse JSON: %v", err)
		}

		if decoded.TagName != "v1.2.3" {
			t.Errorf("JSON tag_name = %v, want v1.2.3", decoded.TagName)
		}
	})

	t.Run("invalid format", func(t *testing.T) {
		_, err := FormatRelease(release, "invalid")
		if err == nil {
			t.Error("FormatRelease() expected error for invalid format")
		}
	})
}

func TestFormatBulkResults(t *testing.T) {
	results := []BulkResult{
		{Repository: "owner/repo1", Tag: "v1.0.0"},
		{Repository: "owner/repo2", Tag: "v2.0.0"},
		{Repository: "owner/repo3", Error: "not found"},
	}

	t.Run("text format", func(t *testing.T) {
		result, err := FormatBulkResults(results, FormatText)
		if err != nil {
			t.Fatalf("FormatBulkResults() error = %v", err)
		}

		lines := strings.Split(result, "\n")
		if len(lines) != 3 {
			t.Errorf("FormatBulkResults() got %d lines, want 3", len(lines))
		}

		if !strings.Contains(lines[0], "owner/repo1: v1.0.0") {
			t.Errorf("Line 0 = %v, want to contain 'owner/repo1: v1.0.0'", lines[0])
		}
		if !strings.Contains(lines[2], "ERROR") {
			t.Errorf("Line 2 = %v, want to contain 'ERROR'", lines[2])
		}
	})

	t.Run("json format", func(t *testing.T) {
		result, err := FormatBulkResults(results, FormatJSON)
		if err != nil {
			t.Fatalf("FormatBulkResults() error = %v", err)
		}

		var decoded []BulkResult
		if err := json.Unmarshal([]byte(result), &decoded); err != nil {
			t.Fatalf("Failed to parse JSON: %v", err)
		}

		if len(decoded) != 3 {
			t.Errorf("JSON array length = %d, want 3", len(decoded))
		}
	})
}
