package plugins

// Plugin defines the interface that all command plugins must implement
type Plugin interface {
	// Name returns the name of the plugin (used as the command name)
	Name() string

	// Description returns a short description of what the plugin does
	Description() string

	// Execute runs the plugin with the given arguments and output format
	Execute(args []string, outputFormat string) error
}
