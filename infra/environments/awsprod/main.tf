module "networking" {
  source = "../../modules/networking/aws"
  region = var.region
}

module "compute" {
  source     = "../../modules/compute/aws"
  region     = var.region
  vpc_id     = module.networking.vpc_id
  subnet_ids = module.networking.private_subnet_ids
}

module "storage" {
  source = "../../modules/storage/aws"
  region = var.region
}
