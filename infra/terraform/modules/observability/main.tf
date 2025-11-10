locals {
  prometheus_endpoint = var.enable_prometheus ? try(aws_prometheus_workspace.this[0].prometheus_endpoint, "") : var.prometheus_remote_write_endpoint
  otel_config        = templatefile("${path.module}/templates/otel-config.tpl", {
    prometheus_remote_write = local.prometheus_endpoint
  })
  collector_command = "echo $OTEL_CONFIG | base64 -d > /etc/otelcol/config.yaml && /otelcol --config=/etc/otelcol/config.yaml"
  grafana_workspace_id = var.grafana_workspace != "" ? var.grafana_workspace : try(aws_grafana_workspace.this[0].id, "")
}

resource "aws_prometheus_workspace" "this" {
  count = var.enable_prometheus ? 1 : 0
  alias = "atlas"
}

resource "aws_grafana_workspace" "this" {
  count = var.grafana_workspace == "" ? 1 : 0
  name                 = "atlas-grafana"
  account_access_type  = "CURRENT_ACCOUNT"
  authentication_providers = ["AWS_SSO"]
  permission_type = "SERVICE_MANAGED"
}

resource "aws_ecs_cluster" "collector" {
  count = var.enable_collector ? 1 : 0
  name  = "atlas-otel"
}

resource "aws_cloudwatch_log_group" "collector" {
  count             = var.enable_collector ? 1 : 0
  name              = "/aws/ecs/atlas-otel"
  retention_in_days = 7
}

resource "aws_iam_role" "collector_task" {
  count = var.enable_collector ? 1 : 0
  name  = "atlas-otel-task"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "collector_exec" {
  count      = var.enable_collector ? 1 : 0
  role       = aws_iam_role.collector_task[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "collector" {
  count                    = var.enable_collector ? 1 : 0
  family                   = "atlas-otel"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.collector_cpu
  memory                   = var.collector_memory
  execution_role_arn       = aws_iam_role.collector_task[0].arn

  container_definitions = jsonencode([
    {
      name      = "otel-collector"
      image     = var.collector_image
      essential = true
      entryPoint = [
        "sh",
        "-c"
      ]
      command = [local.collector_command]
      environment = [
        {
          name  = "OTEL_CONFIG"
          value = base64encode(local.otel_config)
        },
        {
          name  = "PROM_REMOTE_WRITE"
          value = local.prometheus_endpoint
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.collector[0].name
          awslogs-region        = data.aws_region.current.name
          awslogs-stream-prefix = "otel"
        }
      }
      portMappings = [
        {
          containerPort = 4318
          hostPort      = 4318
          protocol      = "tcp"
        }
      ]
    }
  ])
}

data "aws_region" "current" {}

resource "aws_ecs_service" "collector" {
  count           = var.enable_collector && length(var.subnet_ids) > 0 && length(var.security_group_ids) > 0 ? 1 : 0
  name            = "atlas-otel"
  cluster         = aws_ecs_cluster.collector[0].id
  task_definition = aws_ecs_task_definition.collector[0].arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = var.security_group_ids
    assign_public_ip = true
  }
}

output "prometheus_endpoint" {
  value       = local.prometheus_endpoint
  description = "Prometheus remote write endpoint"
}

output "collector_service_name" {
  value       = var.enable_collector ? "atlas-otel" : ""
  description = "Name of the ECS service running the collector"
}

output "grafana_workspace_id" {
  value       = local.grafana_workspace_id
  description = "Grafana workspace used for dashboards"
}
