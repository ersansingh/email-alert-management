resource "google_pubsub_topic" "alerts" {
  name = "ai-sre-alerts-topic"
}

resource "google_storage_bucket" "alerts" {
  name     = "ai-sre-alert-archive-${var.region}"
  location = var.region
  uniform_bucket_level_access = true
}

resource "google_artifact_registry_repository" "ai_sre_repo" {
  location      = var.region
  repository_id = "ai-sre-repo"
  description   = "Docker repository for AI SRE application"
  format        = "DOCKER"
}

resource "google_artifact_registry_repository" "ai_sre_repo" {
  location      = var.region
  repository_id = "ai-sre-repo"
  description   = "Docker repository for AI SRE application"
  format        = "DOCKER"
}
