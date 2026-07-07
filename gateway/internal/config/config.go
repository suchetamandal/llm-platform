package config

import "os"

type Config struct {
	Port           string
	RequestTimeout string
	OpenAIAPIKey   string
	JWTSecret      string
	RedisAddr      string
	RAGServiceURL  string
}

func Load() Config {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	timeout := os.Getenv("REQUEST_TIMEOUT")
	if timeout == "" {
		timeout = "30s"
	}

	jwtSecret := os.Getenv("JWT_SECRET")
	if jwtSecret == "" {
		jwtSecret = "dev-secret"
	}

	ragServiceURL := os.Getenv("RAG_SERVICE_URL")
	if ragServiceURL == "" {
		ragServiceURL = "http://localhost:8000"
	}

	redisAddr := os.Getenv("REDIS_ADDR")
	if redisAddr == "" {
		redisAddr = "localhost:6379"
	}

	return Config{
		Port:           port,
		RequestTimeout: timeout,
		OpenAIAPIKey:	os.Getenv("OPENAI_API_KEY"),
		JWTSecret:      jwtSecret,
		RedisAddr:		redisAddr,
		RAGServiceURL:  ragServiceURL,
	}
}