package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/suchetamandal/llm-platform/gateway/internal/clients"
)

type RAGHandler struct {
	ragClient *clients.RAGClient
}

func NewRAGHandler(ragClient *clients.RAGClient) *RAGHandler {
	return &RAGHandler{
		ragClient: ragClient,
	}
}

func (h *RAGHandler) Ask(c *gin.Context) {
	var req clients.RAGRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "invalid request body",
		})
		return
	}

	if req.Query == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "query is required",
		})
		return
	}

	if req.TopK <= 0 {
		req.TopK = 3
	}

	requestID := c.GetHeader("X-Request-ID")

	resp, err := h.ragClient.Ask(c.Request.Context(), req, requestID)
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{
			"error": "rag service unavailable",
		})
		return
	}

	c.JSON(http.StatusOK, resp)
}