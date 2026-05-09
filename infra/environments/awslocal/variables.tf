variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "localstack_endpoint" {
  description = "Endpoint for LocalStack"
  type        = string
  default     = "http://host.docker.internal:4566"
}
