output "vpc_id" {
  value = aws_vpc.main.id
}

output "private_subnets" {
  value = [
    aws_subnet.private_1.id,
    aws_subnet.private_2.id
  ]
}

output "eks_cluster_name" {
  value = aws_eks_cluster.main.name
}

output "sqs_queue_url" {
  value = aws_sqs_queue.alerts.id
}

output "s3_bucket" {
  value = aws_s3_bucket.alerts.bucket
}