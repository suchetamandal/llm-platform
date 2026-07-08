package clients

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"net/textproto"
	"time"
)

type DocumentUploadResponse struct {
	DocumentID  string `json:"document_id"`
	Filename    string `json:"filename"`
	ContentType string `json:"content_type"`
	Status      string `json:"status"`
}

type RAGDocumentClient struct {
	baseURL    string
	httpClient *http.Client
}

func NewRAGDocumentClient(baseURL string) *RAGDocumentClient {
	return &RAGDocumentClient{
		baseURL: baseURL,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

func (c *RAGDocumentClient) UploadDocument(
	ctx context.Context,
	file multipart.File,
	fileHeader *multipart.FileHeader,
	requestID string,
) (*DocumentUploadResponse, int, error) {
	var body bytes.Buffer

	writer := multipart.NewWriter(&body)

	contentType := fileHeader.Header.Get("Content-Type")
	if contentType == "" {
		contentType = "application/octet-stream"
	}

	header := make(textproto.MIMEHeader)
	header.Set(
		"Content-Disposition",
		fmt.Sprintf(`form-data; name="file"; filename="%s"`, fileHeader.Filename),
	)
	header.Set("Content-Type", contentType)

	part, err := writer.CreatePart(header)
	
	if err != nil {
		return nil, http.StatusInternalServerError, err
	}

	if _, err := io.Copy(part, file); err != nil {
		return nil, http.StatusInternalServerError, err
	}

	if err := writer.Close(); err != nil {
		return nil, http.StatusInternalServerError, err
	}

	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		c.baseURL+"/v1/documents",
		&body,
	)
	if err != nil {
		return nil, http.StatusInternalServerError, err
	}

	req.Header.Set("Content-Type", writer.FormDataContentType())

	if requestID != "" {
		req.Header.Set("X-Request-ID", requestID)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, http.StatusBadGateway, err
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, http.StatusBadGateway, err
	}

	if resp.StatusCode >= 400 {
		return nil, resp.StatusCode, fmt.Errorf("rag service error: %s", string(respBody))
	}

	var uploadResp DocumentUploadResponse
	if err := json.Unmarshal(respBody, &uploadResp); err != nil {
		return nil, http.StatusBadGateway, err
	}

	return &uploadResp, resp.StatusCode, nil
}