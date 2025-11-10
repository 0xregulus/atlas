terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

module "network" {
  source = "./modules/network"
}

module "observability" {
  source = "./modules/observability"
  grafana_workspace = var.grafana_workspace
}

module "ai_services" {
  source                   = "./modules/ai-services"
  core_api_url             = var.core_api_url
  otlp_endpoint            = var.otlp_endpoint
  semantic_cache_capacity  = 10000
}
