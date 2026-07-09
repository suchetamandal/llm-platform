package handlers

import (
	"io"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/suchetamandal/llm-platform/gateway/internal/clients"
)

func RAGStreamHandler(c *gin.Context) {
	requestBody, err := io.ReadAll(c.Request.Body)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "failed to read request body",
		})
		return
	}

	ragServiceURL := os.Getenv("RAG_SERVICE_URL")
	if ragServiceURL == "" {
		ragServiceURL = "http://localhost:8000"
	}

	requestID := c.GetHeader("X-Request-ID")

	client := clients.NewRAGStreamClient(ragServiceURL)

	resp, err := client.StreamRAG(
		c.Request.Context(),
		requestBody,
		requestID,
	)
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{
			"error": err.Error(),
		})
		return
	}
	defer resp.Body.Close()

	c.Header("Content-Type", "text/event-stream")
	c.Header("Cache-Control", "no-cache")
	c.Header("Connection", "keep-alive")

	c.Status(http.StatusOK)

	flusher, ok := c.Writer.(http.Flusher)
	if !ok {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "streaming unsupported",
		})
		return
	}

	buffer := make([]byte, 1024)

	for {
		n, err := resp.Body.Read(buffer)
		if n > 0 {
			if _, writeErr := c.Writer.Write(buffer[:n]); writeErr != nil {
				return
			}
			flusher.Flush()
		}

		if err != nil {
			if err == io.EOF {
				return
			}
			return
		}
	}
}