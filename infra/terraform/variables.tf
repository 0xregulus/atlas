variable "region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "grafana_workspace" {
  type        = string
  description = "Grafana workspace id"
}

variable "core_api_url" {
  type        = string
  description = "URL of Atlas core API"
}

variable "otlp_endpoint" {
  type        = string
  description = "Observability endpoint"
}
