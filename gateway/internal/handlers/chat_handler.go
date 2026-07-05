package handlers

import (
	"io"
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/suchetamandal/llm-platform/gateway/internal/apperrors"
	"github.com/suchetamandal/llm-platform/gateway/internal/models"
	"github.com/suchetamandal/llm-platform/gateway/internal/service/llm"
)

func ChatHandler(c *gin.Context) {
	var req models.ChatRequest

	//validates request.
	if err := c.ShouldBindJSON(&req); err != nil {
		apperrors.BadRequest(c, "CHAT_001", "message is required")
		return
	}

	// c.Request.Context() allows cancellation if client disconnects.
	//calls the LLM service
	stream, err := llm.GenerateStream(c.Request.Context(), req.Message, llm.ChatOptions{
		Model:       req.Model,
		Provider:    req.Provider,
		Temperature: req.Temperature,
	})

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	//enables SSE streaming.
	c.Writer.Header().Set("Content-Type", "text/event-stream")
	c.Writer.Header().Set("Cache-Control", "no-cache")
	c.Writer.Header().Set("Connection", "keep-alive")

	c.Stream(func(w io.Writer) bool {
		token, ok := <-stream
		if !ok {
			return false
		}

		c.SSEvent("message", token)
		return true
	})
}
