package llm

import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type OllamaProvider struct {
	baseURL string
	client  *http.Client
}

type ollamaGenerateRequest struct {
	Model  string `json:"model"`
	Prompt string `json:"prompt"`
	Stream bool   `json:"stream"`
}

type ollamaGenerateResponse struct {
	Response string `json:"response"`
	Done     bool   `json:"done"`
}

func NewOllamaProvider() *OllamaProvider {
	baseURL := os.Getenv("OLLAMA_BASE_URL")
	if baseURL == "" {
		baseURL = "http://localhost:11434"
	}

	return &OllamaProvider{
		baseURL: baseURL,
		client:  &http.Client{},
	}
}

func (p *OllamaProvider) Stream(ctx context.Context, prompt string, opts ChatOptions) (<-chan string, error) {
	model := opts.Model
	if model == "" {
		model = "llama3.2"
	}

	body := ollamaGenerateRequest{
		Model:  model,
		Prompt: prompt,
		Stream: true,
	}

	payload, err := json.Marshal(body)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		p.baseURL+"/api/generate",
		bytes.NewReader(payload),
	)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")

	resp, err := p.client.Do(req)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode >= 300 {
		defer resp.Body.Close()
		return nil, fmt.Errorf("ollama request failed with status: %s", resp.Status)
	}

	ch := make(chan string)

	go func() {
		defer close(ch)
		defer resp.Body.Close()

		scanner := bufio.NewScanner(resp.Body)

		for scanner.Scan() {
			line := scanner.Bytes()

			var chunk ollamaGenerateResponse
			if err := json.Unmarshal(line, &chunk); err != nil {
				continue
			}

			if chunk.Response != "" {
				select {
				case <-ctx.Done():
					return
				case ch <- chunk.Response:
				}
			}

			if chunk.Done {
				return
			}
		}
	}()

	return ch, nil
}
