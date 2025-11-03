# 🏗️ MapleCMS Architecture

MapleCMS is built with a **modular, cloud-native architecture** designed for performance, scalability, and developer simplicity.  
It decouples the **frontend (Next.js)** and **backend (FastAPI)** while using **AWS services** for hosting, storage, and monitoring.

---

## 🧩 High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────┐
│ Frontend (UI Layer)                                    │
│ Next.js + TypeScript + TailwindCSS                     │
│ • Static & Dynamic Rendering                           │
│ • Markdown + API Content Loader                        │
│ • SEO-Optimized Routing & Metadata                     │
└──────────────▲─────────────────────────────────────────┘
               │ REST / GraphQL API Calls
               ▼
┌────────────────────────────────────────────────────────┐
│ Backend (API Layer)                                    │
│ FastAPI (Python 3.11+)                                 │
│ • Async REST API Endpoints                             │
│ • CRUD for Articles, Media, and Users                  │
│ • JWT Authentication & Role-Based Access               │
│ • Validation via Pydantic Models                       │
│ • Integration-Ready for GPT/AI APIs                    │
└──────────────▲─────────────────────────────────────────┘
               │ SQLAlchemy ORM Queries
               ▼
┌────────────────────────────────────────────────────────┐
│ Data & Storage Layer (Persistence)                     │
│ PostgreSQL (RDS) → Structured Data                     │
│ AWS S3 → Media & Static Assets                         │
│ Redis (optional) → Caching Layer                       │
└────────────────────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│ Infrastructure & Deployment Layer                      │
│ Docker → Containerization                              │
│ Terraform → IaC for AWS ECS/ECR                        │
│ GitHub Actions → CI/CD Pipeline                        │
│ CloudFront + Route 53 → CDN + Domain Management        │
│ CloudWatch → Logging & Monitoring                      │
└────────────────────────────────────────────────────────┘
```

---

## ⚙️ Component Overview

### 1️⃣ Frontend — Next.js + TypeScript

- **Rendering:** Server-Side (SSR) and Static (SSG)
- **Framework:** React + TailwindCSS for responsive UI
- **Content Sources:** Markdown files and FastAPI API
- **Routing:** SEO-optimized dynamic routes for pages/articles
- **Build Tool:** Vercel or Node.js build pipeline

### 2️⃣ Backend — FastAPI (Async Python)

- **Architecture:** Lightweight microservice
- **Routing:** `/api/v1/*` REST endpoints
- **ORM:** SQLAlchemy + Alembic migrations
- **Auth:** JWT tokens with role support (Admin, Editor, User)
- **Extensions:** Email, AI, and Plugin modules

### 3️⃣ Database & Storage

| Component | Description |
|-----------|-------------|
| **PostgreSQL (AWS RDS)** | Stores articles, users, settings |
| **AWS S3** | Media assets (images, docs, uploads) |
| **Redis (optional)** | In-memory cache for API responses & sessions |

### 4️⃣ Infrastructure & Deployment

- **Containerization:** Docker + Docker Compose  
- **Provisioning:** Terraform modules for ECS, RDS, S3  
- **CI/CD:** GitHub Actions → ECR → ECS (auto-deploy)  
- **Monitoring:** AWS CloudWatch + Grafana dashboards  

---

## 🔗 Data Flow Overview

1. User opens a page → Next.js requests data from FastAPI  
2. FastAPI fetches from PostgreSQL or Markdown source  
3. FastAPI returns JSON response to Next.js  
4. Next.js renders the page with dynamic data  
5. Optional: Media fetched from S3 via signed URLs  

---

## 🔐 Security Architecture

- JWT authentication tokens  
- HTTPS enforced via CloudFront + ACM certificates  
- IAM roles for S3 & ECR access  
- Environment secrets stored in AWS Secrets Manager  
- CORS control for API routes  

---

## ☁️ Scalability & Resilience

- Stateless services → horizontal scaling via ECS  
- Database replicas via RDS read replicas  
- CDN cache for static assets  
- Load balancing with Application Load Balancer (ALB)  

---

## 🧱 Future Upgrades

- GraphQL endpoint option  
- AI content suggestion microservice  
- Multi-tenant architecture (MapleCloud SaaS)  
- WebSocket real-time content sync  

---

> MapleCMS is engineered to be **developer-first**, **cloud-native**, and **open to innovation** — a lightweight foundation for the next generation of content tools.
