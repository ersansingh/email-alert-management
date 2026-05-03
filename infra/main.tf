module "networking" {
  source         = var.cloud_provider == "aws" ? "./modules/networking/aws" : "./modules/networking/gcp"
  region         = var.region
}

module "compute" {
  source         = var.cloud_provider == "aws" ? "./modules/compute/aws" : "./modules/compute/gcp"
  region         = var.region
  vpc_id         = var.cloud_provider == "aws" ? module.networking.vpc_id : null
  subnet_ids     = var.cloud_provider == "aws" ? module.networking.private_subnet_ids : null
  network_name   = var.cloud_provider == "gcp" ? module.networking.network_name : null
  subnet_name    = var.cloud_provider == "gcp" ? module.networking.subnet_name : null
}

module "storage" {
  source         = var.cloud_provider == "aws" ? "./modules/storage/aws" : "./modules/storage/gcp"
  region         = var.region
}
