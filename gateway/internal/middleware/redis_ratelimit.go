package middleware

import (
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
)

var redisClient = redis.NewClient(&redis.Options{
	Addr: getRedisAddr(),
})

func getRedisAddr() string {
	addr := os.Getenv("REDIS_ADDR")
	if addr == "" {
		addr = "localhost:6379"
	}
	return addr
}

func RedisRateLimiter() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx := c.Request.Context()

		key := "rate_limit:" + c.ClientIP()
		limit := int64(20)
		window := time.Minute

		count, err := redisClient.Incr(ctx, key).Result()
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "rate limiter unavailable"})
			c.Abort()
			return
		}

		if count == 1 {
			redisClient.Expire(ctx, key, window)
		}

		if count > limit {
			c.JSON(http.StatusTooManyRequests, gin.H{"error": "rate limit exceeded"})
			c.Abort()
			return
		}

		c.Next()
	}
}
