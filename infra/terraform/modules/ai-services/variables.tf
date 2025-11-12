variable "core_api_url" {
  type = string
}

variable "otlp_endpoint" {
  type = string
}

variable "semantic_cache_capacity" {
  type        = number
  description = "Max in-memory semantic cache entries exposed to the service"
}
