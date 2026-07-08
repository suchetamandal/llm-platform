package handlers

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/suchetamandal/llm-platform/gateway/internal/clients"
)

func UploadDocumentHandler(c *gin.Context) {
	file, fileHeader, err := c.Request.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "file is required",
		})
		return
	}
	defer file.Close()

	ragServiceURL := os.Getenv("RAG_SERVICE_URL")
	if ragServiceURL == "" {
		ragServiceURL = "http://localhost:8000"
	}

	requestID := c.GetHeader("X-Request-ID")

	client := clients.NewRAGDocumentClient(ragServiceURL)

	resp, statusCode, err := client.UploadDocument(
		c.Request.Context(),
		file,
		fileHeader,
		requestID,
	)
	if err != nil {
		c.JSON(statusCode, gin.H{
			"error": err.Error(),
		})
		return
	}

	c.JSON(statusCode, resp)
}