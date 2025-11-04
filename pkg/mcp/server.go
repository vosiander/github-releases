package mcp

import (
	"context"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	"github.com/sirupsen/logrus"
	"github.com/vosiander/github-releases/pkg/github"
)

// CreateMCPServer creates and configures an MCP server with all tools registered
func CreateMCPServer(client *github.Client) *mcp.Server {
	l := logrus.WithField("component", "mcp-server")
	// Create server with implementation info
	l.Infof("creating mcp server")
	server := mcp.NewServer(&mcp.Implementation{
		Name:    "github-releases",
		Version: "1.0.0",
	}, nil)

	// Register get_release tool
	l.Info("Adding mcp tool: get_release")
	mcp.AddTool(server, &mcp.Tool{
		Name:        "get_release",
		Description: "Get the latest release information for a single GitHub repository",
	}, func(ctx context.Context, req *mcp.CallToolRequest, input GetReleaseInput) (*mcp.CallToolResult, *ReleaseOutput, error) {
		output, err := HandleGetRelease(ctx, client, input)
		if err != nil {
			return nil, nil, err
		}
		return nil, output, nil
	})

	// Register bulk_releases tool
	l.Info("Adding mcp tool: bulk_releases")
	mcp.AddTool(server, &mcp.Tool{
		Name:        "bulk_releases",
		Description: "Get the latest release tags for multiple GitHub repositories concurrently",
	}, func(ctx context.Context, req *mcp.CallToolRequest, input BulkReleasesInput) (*mcp.CallToolResult, *BulkReleaseResult, error) {
		output, err := HandleBulkReleases(ctx, client, input)
		if err != nil {
			return nil, nil, err
		}
		return nil, output, nil
	})

	// Register compare_history tool
	l.Info("Adding mcp tool: compare_history")
	mcp.AddTool(server, &mcp.Tool{
		Name:        "compare_history",
		Description: "Compare historical versions with current releases for multiple repositories to detect updates",
	}, func(ctx context.Context, req *mcp.CallToolRequest, input CompareHistoryInput) (*mcp.CallToolResult, *HistoryComparisonResult, error) {
		output, err := HandleCompareHistory(ctx, client, input)
		if err != nil {
			return nil, nil, err
		}
		return nil, output, nil
	})

	return server
}
