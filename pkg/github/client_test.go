package github

import (
	"testing"
)

func TestParseRepository(t *testing.T) {
	tests := []struct {
		name      string
		input     string
		wantOwner string
		wantRepo  string
		wantErr   bool
	}{
		{
			name:      "valid repository",
			input:     "owner/repo",
			wantOwner: "owner",
			wantRepo:  "repo",
			wantErr:   false,
		},
		{
			name:      "valid repository with spaces",
			input:     "  owner/repo  ",
			wantOwner: "owner",
			wantRepo:  "repo",
			wantErr:   false,
		},
		{
			name:    "invalid format - no slash",
			input:   "ownerrepo",
			wantErr: true,
		},
		{
			name:    "invalid format - empty owner",
			input:   "/repo",
			wantErr: true,
		},
		{
			name:    "invalid format - empty repo",
			input:   "owner/",
			wantErr: true,
		},
		{
			name:    "invalid format - too many parts",
			input:   "owner/repo/extra",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			owner, repo, err := ParseRepository(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("ParseRepository() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if owner != tt.wantOwner {
					t.Errorf("ParseRepository() owner = %v, want %v", owner, tt.wantOwner)
				}
				if repo != tt.wantRepo {
					t.Errorf("ParseRepository() repo = %v, want %v", repo, tt.wantRepo)
				}
			}
		})
	}
}

func TestNewClient(t *testing.T) {
	// Test creating client without token
	client := NewClient("")
	if client == nil {
		t.Error("NewClient() returned nil")
	}
	if client.token != "" {
		t.Errorf("NewClient() token = %v, want empty string", client.token)
	}

	// Test creating client with token
	token := "test-token"
	client = NewClient(token)
	if client == nil {
		t.Error("NewClient() returned nil")
	}
	if client.token != token {
		t.Errorf("NewClient() token = %v, want %v", client.token, token)
	}
}
