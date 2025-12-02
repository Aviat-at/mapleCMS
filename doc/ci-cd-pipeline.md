# ⚙️ MapleCMS CI/CD Pipeline Guide

MapleCMS uses a **fully automated CI/CD pipeline** to deploy both its **Next.js frontend** and **FastAPI backend** to AWS. This document explains the entire flow — from local commits to production deployment.

---

## 🧠 Overview

MapleCMS follows a modern DevOps pipeline using **GitHub Actions**, **Docker**, **Terraform**, and **AWS ECS/ECR**.

### CI/CD Flow Summary
```
   Developer → GitHub Push → CI (Build + Test) → Docker Build → ECR → ECS Deploy → Live Site
```

Each step is automated to ensure reliable, repeatable, and zero-downtime deployments.

---

## 🧩 1. Continuous Integration (CI)

### Trigger
- Triggered on every `push` or `pull_request` to `main` or `dev` branch.

### Steps
1. **Checkout Repository** – Pull latest code.
2. **Set up Environments** – Configure Python, Node.js, AWS credentials.
3. **Install Dependencies** – `npm install` and `pip install -r requirements.txt`.
4. **Run Tests** – Unit & integration tests for both frontend and backend.
5. **Build Docker Images** – Create container images for `frontend` and `backend`.
6. **Push to AWS ECR** – Tag & upload images to Elastic Container Registry.

Example GitHub Actions job:
```yaml
name: CI Build
on:
  push:
    branches: [main, dev]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd frontend && npm ci
          cd ../backend && pip install -r requirements.txt

      - name: Run tests
        run: |
          cd backend && pytest
          cd ../frontend && npm run test

      - name: Build Docker images
        run: |
          docker build -t maplecms-frontend:latest ./frontend
          docker build -t maplecms-backend:latest ./backend
```

---

## ☁️ 2. Continuous Deployment (CD)

### AWS Infrastructure Components
| Component | Service | Purpose |
|------------|----------|----------|
| **Compute** | ECS (Elastic Container Service) | Runs containers in Fargate mode |
| **Registry** | ECR (Elastic Container Registry) | Stores Docker images |
| **Storage** | S3 | Media uploads + static assets |
| **Database** | RDS (PostgreSQL) | Content + user data |
| **Networking** | CloudFront + ALB | CDN and load balancing |

### Steps in CD
1. **Terraform Apply** – Provisions ECS, RDS, and networking infrastructure.
2. **ECS Service Update** – Pulls the latest Docker image from ECR.
3. **Smoke Tests** – Confirms deployment health.
4. **Notifications** – Sends deployment status to Slack/Email.

---

## 🧱 3. Infrastructure as Code (Terraform)

Terraform manages all AWS resources declaratively.

**Modules:**
- `ecs/` → Cluster + Services
- `rds/` → PostgreSQL instance
- `s3/` → Buckets for media and static assets
- `cloudfront/` → CDN + SSL
- `iam/` → Role & policy management

**Commands:**
```bash
terraform init
terraform plan
terraform apply -auto-approve
```

---

## 🔒 4. Secrets & Security

- Secrets managed via **AWS Secrets Manager**.
- GitHub secrets for CI/CD credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`).
- HTTPS enforced by **AWS ACM** certificates.
- Principle of least privilege applied for all IAM roles.

---

## 🚀 5. Deployment Environments

| Environment | Branch | Infrastructure | Notes |
|--------------|---------|----------------|-------|
| **Dev** | `dev` | Staging ECS + RDS | Auto-deployed on merge |
| **Prod** | `main` | Production ECS + RDS | Manual approval required |

Manual promotion between environments ensures stable releases.

---

## 🧩 6. Rollback & Monitoring

### Rollback Procedure
- Use `terraform destroy -target=aws_ecs_service.maplecms_backend` (to redeploy previous version)
- Previous Docker images are versioned in ECR.

### Monitoring
- AWS CloudWatch for logs, CPU, and latency.
- Optional Prometheus + Grafana for visualization.
- Alert notifications through AWS SNS.

---

## 🧭 Summary
- **GitHub Actions** for CI/CD automation.
- **Terraform** for infrastructure as code.
- **AWS ECS + ECR** for scalable, containerized hosting.
- **Secure secrets** and **zero-downtime** deploys.

> MapleCMS CI/CD ensures reliability, speed, and simplicity — empowering developers to deploy confidently with every commit.
