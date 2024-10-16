provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      Project = "myapp-api-py"
      Environment = "${terraform.workspace}"
    }
  }
}

terraform {
  required_version = "~> 1.8.5"
}