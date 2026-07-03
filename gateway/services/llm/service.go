package llm

import (
	"context"
	"fmt"
)

var providers = map[string]Provider{
	"mock":   NewMockProvider(),
	"openai": NewOpenAIProvider(),
	"ollama": NewOllamaProvider(),
}

func GenerateStream(ctx context.Context, prompt string, opts ChatOptions) (<-chan string, error) {
	providerName := opts.Provider
	if providerName == "" {
		providerName = "mock"
	}

	provider, exists := providers[providerName]
	if !exists {
		return nil, fmt.Errorf("unsupported provider: %s", providerName)
	}

	return provider.Stream(ctx, prompt, opts)
}
