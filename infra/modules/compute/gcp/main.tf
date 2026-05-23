resource "google_container_cluster" "primary" {
  name     = "ai-sre-cluster"
  location = var.region
  network  = var.network_name
  subnetwork = var.subnet_name

  deletion_protection = false
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "ai-sre-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = 2

  node_config {
    preemptible  = true
    machine_type = "e2-medium"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
