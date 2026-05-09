resource "aws_sqs_queue" "alerts" {
  name = "ai-sre-alerts-queue"
}

resource "aws_s3_bucket" "alerts" {
  bucket = "ai-sre-alert-archive-${var.region}"
}

output "sqs_queue_url" {
  value = aws_sqs_queue.alerts.id
}

output "s3_bucket" {
  value = aws_s3_bucket.alerts.bucket
}