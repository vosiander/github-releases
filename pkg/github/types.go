package github

// Release represents a GitHub release
type Release struct {
	Repository  string `json:"repository"`
	TagName     string `json:"tag_name"`
	Name        string `json:"name"`
	HTMLURL     string `json:"html_url"`
	PublishedAt string `json:"published_at"`
}
