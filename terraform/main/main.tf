# REFERENCE:
# - DevOps Bootcamp: Terraform by Andrei Neagoie and Andrei Dumitrescu
#   Link: https://www.udemy.com/course/devops-bootcamp-terraform-certification/
# - How Can I Reference Terraform Cloud Environment Variables?
#   Link: https://stackoverflow.com/questions/66598788/terraform-how-can-i-reference-terraform-cloud-environmental-variables
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    hcp = {
      source  = "hashicorp/hcp"
      version = "0.63.0"
    }
  }
  cloud {
    organization = "abwromero"
    workspaces {
      name = "dev-test-us-east"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "../modules/vpc"
}

module "source_rds" {
    source = "../modules/rds"
    vpc_id = module.vpc.vpc_id
    rds_subnets_ids = module.vpc.public_subnets_ids
    microservice_name = "car_sales_source"
    vpc_cidr_block = module.vpc.vpc_cidr_block
}