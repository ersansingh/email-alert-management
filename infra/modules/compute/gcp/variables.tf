variable "region" {
  type = string
}

variable "vpc_id" {
  type = string
  default = null
}

variable "subnet_ids" {
  type = list(string)
  default = null
}

variable "network_name" {
  type = string
  default = null
}

variable "subnet_name" {
  type = string
  default = null
}

variable "project_id" {
  type = string
  default = "ai-learning-495017"
}
