package llm

import (
	"context"
	"fmt"
	"os"

	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"
	"github.com/sirupsen/logrus"
)

// OpenAIProvider is a mock implementation of the Provider interface.
type OpenAIProvider struct {
	client openai.Client
}

// NewOpenAIProvider creates and returns a new OpenAIProvider.
func NewOpenAIProvider() *OpenAIProvider {
	apiKey := os.Getenv("OPENAI_API_KEY")

	client := openai.NewClient(
		option.WithAPIKey(apiKey),
	)

	return &OpenAIProvider{
		client: client,
	}
}

func (p *OpenAIProvider) Stream(ctx context.Context, prompt string, opts ChatOptions) (<-chan string, error) {

	if os.Getenv("OPENAI_API_KEY") == "" {
		return nil, fmt.Errorf("OPENAI_API_KEY is not set")
	}

	// Creates a channel for streaming tokens.
	ch := make(chan string)

	model := opts.Model
	if model == "" {
		model = "gpt-4o-mini"
	}

	// Launches a goroutine so Stream() returns immediately.
	go func() {
		defer close(ch)

		stream := p.client.Chat.Completions.NewStreaming(ctx, openai.ChatCompletionNewParams{
			Model: model,
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.UserMessage(prompt),
			},
		})

		// Sends one token at a time through the channel.
		// Waits 250ms between tokens to simulate LLM generation.
		// Stops immediately if the context is cancelled.
		for stream.Next() {
			chunk := stream.Current()

			if len(chunk.Choices) == 0 {
				continue
			}

			content := chunk.Choices[0].Delta.Content
			if content == "" {
				continue
			}

			select {
			case <-ctx.Done():
				return
			case ch <- content:
			}
		}

		if err := stream.Err(); err != nil {
			logrus.WithError(err).Error("openai stream failed")
		}

	}()

	return ch, nil
}
