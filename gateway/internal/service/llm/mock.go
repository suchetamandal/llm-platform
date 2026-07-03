package llm

import (
	"context"
	"time"
)

type MockProvider struct{}

func NewMockProvider() *MockProvider {
	return &MockProvider{}
}

func (p *MockProvider) Stream(ctx context.Context, prompt string, opts ChatOptions) (<-chan string, error) {
	ch := make(chan string)

	go func() {
		defer close(ch)

		tokens := []string{
			"Mock",
			" response",
			" from",
			" Go",
			" LLM",
			" Gateway.",
		}

		for _, token := range tokens {
			select {
			case <-ctx.Done():
				return
			case ch <- token:
				time.Sleep(250 * time.Millisecond)
			}
		}
	}()

	return ch, nil
}
