resource "google_pubsub_topic" "alerts" {
  name = "ai-sre-alerts-topic"
}

resource "google_storage_bucket" "alerts" {
  name     = "ai-sre-alert-archive-${var.region}"
  location = var.region
}
