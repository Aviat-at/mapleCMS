# 🌲 MapleCMS Terraform Guide

This guide explains how to provision **AWS infrastructure** for MapleCMS using **Terraform**. It covers module layout, remote state, environments, variables, and deployment commands.

---

## 🧭 Architecture (Infra Scope)
- **VPC** (private subnets + NAT + public subnets for ALB)
- **ECS Fargate** (frontend and backend services)
- **ECR** (Docker image registry)
- **RDS PostgreSQL** (managed database)
- **S3** (media bucket + Terraform state)
- **CloudFront** (CDN for frontend)
- **ACM** (TLS certificates)
- **Route 53** (optional custom domain)
- **CloudWatch** (logs + alarms)

---

## 📁 Repository Layout
```
infra/
├── modules/
│   ├── vpc/
│   ├── ecr/
│   ├── ecs-service/
│   ├── rds-postgres/
│   ├── s3-bucket/
│   ├── cloudfront/
│   ├── acm/
│   └── iam/
├── envs/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── backend.tf
└── README.md
```

---

## 🗂️ Remote State & Locking
Use **S3** for state and **DynamoDB** for state locking.

**`backend.tf` (per environment):**
```hcl
terraform {
  backend "s3" {
    bucket         = "maplecms-tf-state"
    key            = "envs/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "maplecms-tf-locks"
    encrypt        = true
  }
}
```

Create the state bucket and lock table once (bootstrap script or manual):
```bash
aws s3api create-bucket --bucket maplecms-tf-state --region us-east-1 \
  --create-bucket-configuration LocationConstraint=us-east-1
aws dynamodb create-table --table-name maplecms-tf-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

---

## 🔧 Providers & Versions
**`providers.tf`**
```hcl
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.6"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

---

## 🧮 Variables
**`variables.tf` (common)**
```hcl
variable "project" { type = string }
variable "environment" { type = string }           # dev|prod
variable "aws_region" { type = string  default = "us-east-1" }
variable "domain_name" { type = string  default = null }  # optional Route53 domain
variable "frontend_image" { type = string }        # ECR URI:tag
variable "backend_image"  { type = string }
variable "db_username" { type = string }
variable "db_password" { type = string  sensitive = true }
variable "db_instance_class" { type = string  default = "db.t4g.micro" }
variable "desired_count_backend" { type = number default = 1 }
variable "desired_count_frontend" { type = number default = 1 }
```

**`terraform.tfvars.example`**
```hcl
project     = "maplecms"
environment = "dev"
aws_region  = "us-east-1"
frontend_image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/maplecms-frontend:main"
backend_image  = "123456789012.dkr.ecr.us-east-1.amazonaws.com/maplecms-backend:main"
db_username = "maple"
db_password = "CHANGEME"
```

---

## 🏗️ Main Stack (envs/dev/main.tf)
```hcl
module "vpc" {
  source = "../modules/vpc"
  project = var.project
  environment = var.environment
}

module "ecr" {
  source = "../modules/ecr"
  project = var.project
  repos = ["maplecms-frontend", "maplecms-backend"]
}

module "rds" {
  source              = "../modules/rds-postgres"
  project             = var.project
  environment         = var.environment
  db_username         = var.db_username
  db_password         = var.db_password
  vpc_id              = module.vpc.id
  private_subnet_ids  = module.vpc.private_subnets
}

module "media_bucket" {
  source  = "../modules/s3-bucket"
  name    = "${var.project}-${var.environment}-media"
  acl     = "private"
  version = true
}

module "acm" {
  source      = "../modules/acm"
  domain_name = var.domain_name
  create      = var.domain_name != null
}

module "ecs_backend" {
  source             = "../modules/ecs-service"
  name               = "${var.project}-api"
  image              = var.backend_image
  port               = 8000
  vpc_id             = module.vpc.id
  private_subnets    = module.vpc.private_subnets
  public_subnets     = module.vpc.public_subnets
  desired_count      = var.desired_count_backend
  env = {
    DATABASE_URL = module.rds.database_url
    S3_BUCKET    = module.media_bucket.name
  }
}

module "ecs_frontend" {
  source             = "../modules/ecs-service"
  name               = "${var.project}-web"
  image              = var.frontend_image
  port               = 3000
  vpc_id             = module.vpc.id
  private_subnets    = module.vpc.private_subnets
  public_subnets     = module.vpc.public_subnets
  desired_count      = var.desired_count_frontend
}

module "cdn" {
  source         = "../modules/cloudfront"
  origin_domain  = module.ecs_frontend.alb_dns
  acm_cert_arn   = module.acm.cert_arn
  create         = var.domain_name != null
}
```

---

## 🧰 Commands
```bash
# authenticate to AWS
aws configure

# initialize terraform (per env)
cd infra/envs/dev
terraform init

# see the plan
terraform plan -var-file=terraform.tfvars

# apply the changes
terraform apply -var-file=terraform.tfvars

# destroy (be careful!)
terraform destroy -var-file=terraform.tfvars
```

### Workspaces (optional)
```bash
terraform workspace new dev
terraform workspace select dev
```

---

## 🔐 Secrets Management
- Pass DB password and JWT secrets via **Terraform variables** sourced from **AWS Secrets Manager** or **SSM Parameter Store**.
- Never commit secrets to Git. Use `sensitive = true` on secret variables.

---

## 📈 Autoscaling & Sizing
- Start with **Fargate** `0.25 vCPU / 512 MB` per task for frontend & backend.
- Enable **ECS Service Autoscaling** on CPU ≥ 60% or latency alarms.
- RDS: `db.t4g.micro` (dev) → `db.t4g.small/medium` (prod).

---

## 📦 CI/CD Integration
Your CI (GitHub Actions) should:
1. Build images and push to **ECR**.
2. Run `terraform plan` on PRs.
3. On main merges, run `terraform apply` (with manual approval for prod).

**Example deploy step (pseudocode):**
```yaml
- name: Terraform Apply (dev)
  run: |
    cd infra/envs/dev
    terraform init -input=false
    terraform apply -auto-approve -var-file=terraform.tfvars
```

---

## 🛡️ Security Checklist
- Private subnets for ECS tasks; ALB in public subnets only.
- SG rules: allow 80/443 to ALB; ALB → ECS on app ports; ECS → RDS on 5432.
- S3 buckets: block public access; enable server-side encryption.
- CloudFront + ACM for TLS; redirect HTTP → HTTPS.
- Least-privilege IAM roles for tasks (S3, CloudWatch only).

---

## 💸 Cost Notes (rough, us-east-1)
- ECS Fargate (2 small tasks): ~$20–40/mo
- RDS t4g.micro (dev): ~$15–20/mo (storage extra)
- S3 (low usage): ~$1–5/mo
- CloudFront: pay-as-you-go (low for dev sites)
> Use **budgets + alarms** in AWS to avoid surprises.

---

## 🧯 Troubleshooting
- **ECS service not healthy** → check target group health checks & container port mapping.
- **Images not updating** → verify ECR tag and task definition revision.
- **RDS connection errors** → confirm SG rules and `DATABASE_URL`.
- **ACM not issued** → DNS validation must be completed in Route 53.

---

## 🧭 Summary
This Terraform setup gives MapleCMS a **repeatable, secure, and scalable** AWS baseline. Start minimal, scale with autoscaling and larger DB classes, and keep all changes tracked in code.
