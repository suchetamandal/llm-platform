package llm

import (
	"context"
	"fmt"
	"time"
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

	model := opts.Model
	if model == "" {
		model = "default"
	}

	provider, exists := providers[providerName]
	if !exists {
		LLMRequestsTotal.WithLabelValues(providerName, model, "unsupported").Inc()
		return nil, fmt.Errorf("unsupported provider: %s", providerName)
	}

	start := time.Now()

	stream, err := provider.Stream(ctx, prompt, opts)
	if err != nil {
		LLMRequestsTotal.WithLabelValues(providerName, model, "error").Inc()
		return nil, err
	}

	out := make(chan string)

	go func() {
		defer close(out)
		defer LLMStreamDuration.WithLabelValues(providerName, model).Observe(time.Since(start).Seconds())
		defer LLMRequestsTotal.WithLabelValues(providerName, model, "success").Inc()

		for token := range stream {
			select {
			case <-ctx.Done():
				LLMRequestsTotal.WithLabelValues(providerName, model, "cancelled").Inc()
				return
			case out <- token:
			}
		}
	}()

	return out, nil
}
