output "vpc_id" {
  value = module.networking.vpc_id
}

output "private_subnets" {
  value = module.networking.private_subnet_ids
}

output "sqs_queue_url" {
  value = module.storage.sqs_queue_url
}

output "s3_bucket" {
  value = module.storage.s3_bucket
}
