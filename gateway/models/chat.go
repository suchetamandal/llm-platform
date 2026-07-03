package models

type ChatRequest struct {
	Message     string   `json:"message" binding:"required"`
	Model       string   `json:"model"`
	Provider    string   `json:"provider"`
	Temperature *float64 `json:"temperature"`
}

type ChatChunk struct {
	Type      string `json:"type"`
	Content   string `json:"content"`
	RequestID string `json:"request_id"`
}
