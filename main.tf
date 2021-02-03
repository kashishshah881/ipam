provider "aws" {
  region = "us-east-1"
}

# Create new staging DB
resource "aws_db_instance" "default" {
  allocated_storage    = 25
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "ipamdb"
  username             = "admin"
  password             = "qwerty1234"
  parameter_group_name = "default.mysql5.7"
}

# Create a FIFO Queue

resource "aws_sqs_queue" "terraform_queue" {
  name                        = "terraform-example-queue.fifo"
  visibility_timeout_seconds =  3
  fifo_queue                  = true
  content_based_deduplication = true
}
