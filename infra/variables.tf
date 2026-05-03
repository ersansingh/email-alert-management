variable "region" {
  default = "us-east-1"
}

variable "cloud_provider" {
  description = "The cloud provider to deploy to (aws or gcp)"
  type        = string
  default     = "aws"
}
