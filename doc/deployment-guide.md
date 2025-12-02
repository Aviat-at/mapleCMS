# 🚀 MapleCMS Deployment Guide

This guide explains how to deploy **MapleCMS** in production. It includes a full **AWS reference deployment** (ECS + RDS + S3 + CloudFront) and **lighter alternatives** (Docker Compose on a VM, Vercel/Netlify for the frontend).

---

## 🧭 Deployment Options

| Option | Best For | Stack |
|-------|----------|------|
| **AWS Reference (recommended)** | Production, autoscaling, reliability | ECS Fargate, ECR, RDS (Postgres), S3, CloudFront, ACM |
| **Docker Compose on VM** | Small self-hosted installs, demos | Docker Engine, Nginx reverse proxy, local Postgres |
| **Vercel/Netlify + Managed Backend** | Static-first sites | Frontend on Vercel/Netlify, backend on ECS/Fly/Render |

---

## ✅ Prerequisites
- Docker & Docker Compose
- AWS account with admin access (or delegated IaC role)
- AWS CLI configured (`aws configure`)
- Terraform ≥ 1.6
- GitHub repository for CI/CD

---

## ☁️ Part A — AWS Reference Deployment

### A1) Build & Push Images to ECR
Create ECR repos (once) and push images on each release.

```bash
# Backend
aws ecr create-repository --repository-name maplecms-backend || true
# Frontend
aws ecr create-repository --repository-name maplecms-frontend || true

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=us-east-1

aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build
docker build -t maplecms-backend:main ./backend
docker build -t maplecms-frontend:main ./frontend

# Tag & push
for IMG in backend frontend; do 
  docker tag maplecms-$IMG:main $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/maplecms-$IMG:main
  docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/maplecms-$IMG:main
done
```

> CI/CD (GitHub Actions) should perform these steps automatically on merges to `main`.

---

### A2) Provision AWS with Terraform
Reference: `docs/terraform-guide.md`

```bash
cd infra/envs/prod
cp terraform.tfvars.example terraform.tfvars
# Edit images, domain, DB creds, counts
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

**Creates:** VPC, ECS (frontend/backend), ALB, RDS Postgres, S3 buckets, ECR, CloudFront (if domain), ACM TLS, CloudWatch.

---

### A3) Secrets & Env Vars
Store secrets in **AWS Secrets Manager** or **SSM Parameter Store**.

Required variables (examples):
```
# Backend (FastAPI)
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/maplecms
SECRET_KEY=super-secret
S3_BUCKET=maplecms-prod-media
AWS_REGION=us-east-1
CORS_ORIGINS=["https://maplecms.com"]

# Frontend (Next.js)
NEXT_PUBLIC_API_URL=https://api.maplecms.com/api/v1
```

Inject these into ECS task definitions via Terraform module vars.

---

### A4) Domain & TLS
- Create a `maplecms.com` (example) hosted zone in Route 53.
- Provision ACM certificate in **us-east-1** for CloudFront.
- Terraform module sets CloudFront + DNS records if `domain_name` is provided.

---

### A5) Blue/Green & Zero‑Downtime
**Default (rolling):** ECS updates tasks in-place behind ALB.

**Blue/Green (optional):**
- Use **CodeDeploy for ECS** with two target groups (blue & green).
- Shift traffic after health checks pass; auto-rollback on failure.

**Minimalist Blue/Green:**
- Maintain two tags (`:blue`, `:green`) and flip the service task definition.

---

### A6) Post‑Deploy Verification
- `GET https://api.maplecms.com/api/v1/health` → `{ "status": "ok" }`
- Visit frontend domain → confirm article list renders
- Check CloudWatch log groups for 5xx errors
- Run a smoke test:
```bash
curl -sSf https://api.maplecms.com/api/v1/articles/ > /dev/null
```

---

### A7) Rollback Strategy
- Revert to previous **task definition revision** in ECS
- Pin to previous **ECR image tag** (e.g., `:build-123`)
- `terraform apply` with prior image variables (kept in version control)

---

## 🐳 Part B — Docker Compose on a VM

> Suitable for small teams and quick demos. Not HA.

**`docker-compose.yml` (example):**
```yaml
version: "3.9"
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: maplecms
      POSTGRES_USER: maple
      POSTGRES_PASSWORD: changeme
    volumes:
      - dbdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql+asyncpg://maple:changeme@db:5432/maplecms
      SECRET_KEY: super-secret
      S3_BUCKET: local-dev
    depends_on:
      - db
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
    ports:
      - "3000:3000"

volumes:
  dbdata:
```

**Run:**
```bash
docker compose up -d --build
```

**Reverse Proxy (optional):** Use Nginx/Caddy for TLS on the VM.

---

## 🌐 Part C — Vercel/Netlify Frontend + Managed Backend

**Frontend (Vercel/Netlify):**
- Set `NEXT_PUBLIC_API_URL` to the backend URL
- Configure build: `npm ci && npm run build`
- Output: Next.js (static or SSR)

**Backend (choose one):**
- **AWS ECS (recommended)** — use the same Terraform stack
- **Fly.io / Render** — deploy FastAPI Docker image, attach managed Postgres

**Notes:** Ensure CORS allows your frontend domain.

---

## 🔐 Security Checklist
- Enforce **HTTPS** everywhere (ALB/CloudFront/Proxy)
- Restrict ECS tasks to **private subnets**
- Apply **least-privilege IAM** for S3/ECR/CloudWatch
- Rotate secrets; never commit `.env` to Git
- Enable **automatic minor upgrades** for RDS

---

## 🧯 Troubleshooting
- **502/504 at ALB:** container port mismatch, failing health checks
- **ECS task crash:** wrong env vars, DB connectivity, out-of-memory
- **Images not updating:** confirm new task definition revision is active
- **CORS errors:** update `CORS_ORIGINS` on backend
- **Slow TTFB:** add Redis caching / increase task CPU

---

## 🧭 Summary
- Use **AWS reference deploy** for production-grade hosting
- Use **Docker Compose** for small projects or demos
- Use **Vercel/Netlify** to offload frontend hosting when backend is elsewhere

> MapleCMS ships with a deployment path for every stage — from a single VM to a fully managed AWS footprint with autoscaling and blue/green releases.
