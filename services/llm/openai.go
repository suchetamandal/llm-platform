package llm

import(
	"context"
	"time"
)

// OpenAIProvider is a mock implementation of the Provider interface.
type OpenAIProvider struct{}

// NewOpenAIProvider creates and returns a new OpenAIProvider.
func NewOpenAIProvider() *OpenAIProvider {
	return &OpenAIProvider{}
}

func (p *OpenAIProvider) Stream(ctx context.Context, promt string) (<-chan string, error) {
	// Creates a channel for streaming tokens.
	ch := make(chan string)

	// Launches a goroutine so Stream() returns immediately.
	go func() {
		defer close(ch)

		tokens := []string{
			"Hello",
			" from",
			" your",
			" Go",
			" LLM",
			" Gateway!",
		}

		// Sends one token at a time through the channel.
		// Waits 250ms between tokens to simulate LLM generation.
		// Stops immediately if the context is cancelled.
		for _, token := range tokens {
			select {
			case <- ctx.Done():
				return
			case ch <- token:
				time.Sleep(250 * time.Millisecond)	
			}
		}
	}()

	return ch, nil;
}