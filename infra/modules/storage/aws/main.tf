resource "aws_sqs_queue" "alerts" {
  name = "ai-sre-alerts-queue"
}

resource "aws_s3_bucket" "alerts" {
  bucket = "ai-sre-alert-archive-${var.region}"
}
