resource "google_container_cluster" "primary" {
  name     = "ai-sre-cluster"
  location = "${var.region}-a" # Use a specific zone instead of a region to stay within quota
  network  = var.network_name
  subnetwork = var.subnet_name

  remove_default_node_pool = true
  initial_node_count       = 1
  deletion_protection      = false
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "ai-sre-node-pool"
  location   = "${var.region}-a" # Match cluster zone
  cluster    = google_container_cluster.primary.name
  node_count = 1 # Reduce node count to save disk space

  node_config {
    preemptible  = true
    machine_type = "e2-medium"
    disk_size_gb = 50 # Reduce disk size from 100GB to 50GB
    disk_type    = "pd-standard" # Use standard disks instead of SSD (pd-balanced) if needed, but reducing size is better

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
