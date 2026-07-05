package apperrors

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type ErrorResponse struct {
	Code      string `json:"code"`
	Message   string `json:"message"`
	RequestID string `json:"request_id"`
}

func Write(c *gin.Context, status int, code string, message string) {
	requestID := c.GetString("request_id")

	c.JSON(status, ErrorResponse{
		Code:      code,
		Message:   message,
		RequestID: requestID,
	})
}

func BadRequest(c *gin.Context, code string, message string) {
	Write(c, http.StatusBadRequest, code, message)
}

func Unauthorized(c *gin.Context, code string, message string) {
	Write(c, http.StatusUnauthorized, code, message)
}

func TooManyRequests(c *gin.Context, code string, message string) {
	Write(c, http.StatusTooManyRequests, code, message)
}

func Internal(c *gin.Context, code string, message string) {
	Write(c, http.StatusInternalServerError, code, message)
}
