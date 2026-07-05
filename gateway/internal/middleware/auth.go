package middleware

import (
	"github.com/gin-gonic/gin"
	"strings"

	"github.com/golang-jwt/jwt/v5"
	"github.com/suchetamandal/llm-platform/gateway/internal/apperrors"
)

const UserIDKey = "user_id"

type AuthClaims struct {
	UserID string `json:"user_id"`
	jwt.RegisteredClaims
}

func AuthMiddleware(secret string) gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")

		if authHeader == "" {
			apperrors.Unauthorized(c, "AUTH_001", "missing authorization header")
			c.Abort()
			return
		}

		if !strings.HasPrefix(authHeader, "Bearer ") {
			apperrors.Unauthorized(c, "AUTH_001", "missing authorization header")
			c.Abort()
			return
		}

		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		claims := &AuthClaims{}

		token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
			return []byte(secret), nil
		})

		if err != nil || !token.Valid {
			apperrors.Unauthorized(c, "AUTH_002", "invalid token")
			c.Abort()
			return
		}

		if claims.UserID == "" {
			apperrors.Unauthorized(c, "AUTH_003", "missing user_id claim")
			c.Abort()
			return
		}

		c.Set(UserIDKey, claims.UserID)

		c.Next()
	}
}
