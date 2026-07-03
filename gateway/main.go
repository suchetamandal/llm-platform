package main

import (
	"github.com/gin-gonic/gin"

	"github.com/suchetamandal/llm-platform/gateway/handlers"
	"github.com/suchetamandal/llm-platform/gateway/middleware"
)

func main() {
	r := gin.New()

	r.Use(gin.Recovery())
	r.Use(middleware.Logger())

	r.GET("/healthz", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})

	v1 := r.Group("/v1")
	v1.Use(middleware.AuthMiddleware())
	v1.Use(middleware.RateLimiter())

	v1.POST("/chat", handlers.ChatHandler)

	r.Run(":8080")
}
