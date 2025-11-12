variable "grafana_workspace" {
  type        = string
  description = "Existing Grafana workspace ID (optional)"
  default     = ""
}

variable "enable_prometheus" {
  type        = bool
  description = "Whether to create an AMP workspace"
  default     = true
}

variable "prometheus_remote_write_endpoint" {
  type        = string
  description = "External remote write endpoint (if not creating AMP)"
  default     = ""
}

variable "collector_image" {
  type    = string
  default = "otel/opentelemetry-collector:0.96.0"
}

variable "enable_collector" {
  type    = bool
  default = true
}

variable "subnet_ids" {
  type    = list(string)
  default = []
}

variable "security_group_ids" {
  type    = list(string)
  default = []
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "collector_cpu" {
  type    = number
  default = 256
}

variable "collector_memory" {
  type    = number
  default = 512
}
