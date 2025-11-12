resource "aws_ecs_cluster" "ai" {
  name = "atlas-ai"
}

resource "aws_ecs_task_definition" "ai" {
  family                   = "atlas-ai-service"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  container_definitions = jsonencode([
    {
      name      = "ai-service"
      image     = "public.ecr.aws/atlas/ai-service:latest"
      essential = true
      environment = [
        { name = "ATLAS_AI_CORE_API_URL", value = var.core_api_url },
        { name = "OTLP_ENDPOINT", value = var.otlp_endpoint },
        {
          name  = "SEMANTIC_CACHE_CAPACITY"
          value = tostring(var.semantic_cache_capacity)
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "ai" {
  name            = "atlas-ai"
  cluster         = aws_ecs_cluster.ai.id
  task_definition = aws_ecs_task_definition.ai.arn
  desired_count   = 1
  launch_type     = "FARGATE"
}
