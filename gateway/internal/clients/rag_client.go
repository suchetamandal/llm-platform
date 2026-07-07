package clients

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"
)

type RAGClient struct {
	baseURL    string
	httpClient *http.Client
}

func NewRAGClient(baseURL string, timeout time.Duration) *RAGClient {
	return &RAGClient{
		baseURL: strings.TrimRight(baseURL, "/v1"),
		httpClient: &http.Client{
			Timeout: timeout,
		},
	}
}

type RAGRequest struct {
	Query string `json:"query"`
	TopK  int    `json:"top_k"`
}

type RAGResponse struct {
	Answer  string      `json:"answer"`
	Sources interface{} `json:"sources,omitempty"`
}

func (c *RAGClient) Ask(ctx context.Context, req RAGRequest, requestID string) (*RAGResponse, error) {
	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("marshal rag request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		c.baseURL+"/v1/rag",
		bytes.NewReader(body),
	)
	if err != nil {
		return nil, fmt.Errorf("create rag request: %w", err)
	}

	httpReq.Header.Set("Content-Type", "application/json")

	if requestID != "" {
		httpReq.Header.Set("X-Request-ID", requestID)
	}

	resp, err := c.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("call rag service: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		return nil, fmt.Errorf("rag service returned status %d", resp.StatusCode)
	}

	var ragResp RAGResponse
	if err := json.NewDecoder(resp.Body).Decode(&ragResp); err != nil {
		return nil, fmt.Errorf("decode rag response: %w", err)
	}

	return &ragResp, nil
}