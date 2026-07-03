package llm

import "github.com/prometheus/client_golang/prometheus"

var (
	LLMRequestsTotal = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "gateway_llm_requests_total",
			Help: "Total number of LLM provider requests.",
		},
		[]string{"provider", "model", "status"},
	)

	LLMStreamDuration = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "gateway_llm_stream_duration_seconds",
			Help:    "Duration of LLM streaming responses.",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"provider", "model"},
	)
)

func init() {
	prometheus.MustRegister(LLMRequestsTotal)
	prometheus.MustRegister(LLMStreamDuration)
}
