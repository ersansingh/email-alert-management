module "networking" {
  source = "../../modules/networking/gcp"
  region = var.region
}

module "compute" {
  source       = "../../modules/compute/gcp"
  region       = var.region
  network_name = module.networking.network_name
  subnet_name  = module.networking.subnet_name
}

module "storage" {
  source = "../../modules/storage/gcp"
  region = var.region
}
