resource "google_compute_network" "main" {
  name                    = "ai-sre-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "private" {
  name          = "ai-sre-private-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.main.id
}

output "network_name" {
  value = google_compute_network.main.name
}

output "subnet_name" {
  value = google_compute_subnetwork.private.name
}
