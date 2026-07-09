package clients

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"net/http"
)

type RAGStreamClient struct {
	baseURL    string
	httpClient *http.Client
}

func NewRAGStreamClient(baseURL string) *RAGStreamClient {
	return &RAGStreamClient{
		baseURL: baseURL,
		httpClient: &http.Client{
			Timeout: 0,
		},
	}
}

func (c *RAGStreamClient) StreamRAG(
	ctx context.Context,
	body []byte,
	requestID string,
) (*http.Response, error) {
	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		c.baseURL+"/v1/rag/stream",
		bytes.NewReader(body),
	)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")

	if requestID != "" {
		req.Header.Set("X-Request-ID", requestID)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode >= 400 {
		defer resp.Body.Close()

		respBody, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("rag service error: %s", string(respBody))
	}

	return resp, nil
}