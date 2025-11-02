package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/vosiander/github-releases/pkg/github"
	"github.com/vosiander/github-releases/plugins"
	"github.com/vosiander/github-releases/plugins/bulk"
	"github.com/vosiander/github-releases/plugins/get"
)

// version is set via ldflags during build
var version = "dev"

var (
	outputFormat string
)

func main() {
	if err := run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func run() error {
	// Get GitHub token from environment
	token := os.Getenv("GITHUB_TOKEN")

	// Create GitHub client
	client := github.NewClient(token)

	// Create plugin registry
	registry := plugins.NewRegistry()

	// Register plugins
	if err := registry.Register(get.New(client)); err != nil {
		return fmt.Errorf("failed to register get plugin: %w", err)
	}
	if err := registry.Register(bulk.New(client)); err != nil {
		return fmt.Errorf("failed to register bulk plugin: %w", err)
	}

	// Initialize root command
	rootCmd := initRootCmd()

	// Register plugins as subcommands
	registerPlugins(rootCmd, registry)

	// Execute command
	return rootCmd.Execute()
}

func initRootCmd() *cobra.Command {
	rootCmd := &cobra.Command{
		Use:   "githubrel",
		Short: "GitHub releases tracker CLI",
		Long:  "A CLI tool to fetch and track GitHub release tags from repositories",
		Run: func(cmd *cobra.Command, args []string) {
			cmd.Help()
		},
	}

	// Add global flags
	rootCmd.PersistentFlags().StringVarP(&outputFormat, "output", "o", "text", "Output format (text or json)")

	// Add version command
	rootCmd.AddCommand(&cobra.Command{
		Use:   "version",
		Short: "Print the version number",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Printf("githubrel version %s\n", version)
		},
	})

	return rootCmd
}

func registerPlugins(cmd *cobra.Command, registry *plugins.Registry) {
	for _, plugin := range registry.All() {
		p := plugin // Capture plugin in closure
		subCmd := &cobra.Command{
			Use:   p.Name(),
			Short: p.Description(),
			RunE: func(cmd *cobra.Command, args []string) error {
				return p.Execute(args, outputFormat)
			},
		}
		cmd.AddCommand(subCmd)
	}
}
