module "networking" {
  source = "../../modules/networking/aws"
  region = var.region
}

module "storage" {
  source = "../../modules/storage/aws"
  region = var.region
}
