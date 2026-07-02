package llm

import "context"

var provider Provider = NewOpenAIProvider()

func GenerateStream(ctx context.Context, prompt string) (<-chan string, error) {
	return provider.Stream(ctx, prompt)
}