package llm

import "context"

type ChatOptions struct {
	Model       string
	Provider    string
	Temperature *float64
}

type Provider interface {
	// Stream starts generating a response for the given prompt.
	//
	// It returns:
	//   - A receive-only channel that streams generated text chunks or tokens.
	//   - An error if the streaming session could not be started.
	//
	// The caller should read from the returned channel until it is closed.
	// If the provided context is cancelled or reaches its deadline,
	// the implementation should stop generating output and close the channel.

	Stream(ctx context.Context, prompt string, opts ChatOptions) (<-chan string, error)
}
