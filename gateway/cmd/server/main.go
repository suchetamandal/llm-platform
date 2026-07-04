package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	"github.com/suchetamandal/llm-platform/gateway/internal/config"
	"github.com/suchetamandal/llm-platform/gateway/internal/handlers"
	"github.com/suchetamandal/llm-platform/gateway/internal/middleware"
)

func main() {

	cfg := config.Load()

	requestTimeout, err := time.ParseDuration(cfg.RequestTimeout)
	if err != nil {
		log.Fatalf("invalid REQUEST_TIMEOUT: %v", err)
	}

	r := gin.New()

	r.Use(gin.Recovery())
	r.Use(middleware.Logger())
	r.Use(middleware.Timeout(requestTimeout))
	r.Use(middleware.Metrics())

	r.GET("/healthz", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})

	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	v1 := r.Group("/v1")
	v1.Use(middleware.AuthMiddleware(cfg.JWTSecret))
	v1.Use(middleware.RedisRateLimiter()) // previously it was RateLimiter
	v1.POST("/chat", handlers.ChatHandler)

	server := &http.Server{
		Addr:    ":" + cfg.Port,
		Handler: r,
	}

	go func() {
		log.Printf("gateway listening on port %s", cfg.Port)

		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("server failed: %v", err)
		}
	}()

	quit := make(chan os.Signal, 1)

	signal.Notify(
		quit,
		syscall.SIGINT,
		syscall.SIGTERM,
	)

	<-quit
	log.Println("shutdown signal received")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("server forced to shutdown: %v", err)
	}

	log.Println("server exited cleanly")

}
