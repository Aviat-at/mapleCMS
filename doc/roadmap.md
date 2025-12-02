# 🗺️ MapleCMS Product Roadmap

This roadmap outlines the **phased development plan** for MapleCMS — from its lightweight MVP to a scalable, cloud-ready open-source platform. Each phase builds on the previous one, ensuring incremental improvements while maintaining speed and simplicity.

---

## 🌱 Phase 1 — MVP (Core CMS)
**Goal:** Build the foundation of a fast, open-source CMS that’s easy to install and deploy.

**Deliverables:**
- ✅ FastAPI backend with CRUD for Articles, Users, Categories, Tags
- ✅ PostgreSQL database with Alembic migrations
- ✅ Next.js + TypeScript frontend for content display
- ✅ JWT-based authentication
- ✅ File uploads via AWS S3
- ✅ Docker Compose setup (local)
- ✅ Terraform templates for AWS ECS deployment
- ✅ GitHub Actions CI/CD pipeline

**Target Users:** Developers & early adopters building content-driven websites.

**Release:** `v1.0.0`

---

## 🧩 Phase 2 — Developer Experience & Extensibility
**Goal:** Improve the contributor experience and open the system to extensions.

**Deliverables:**
- 🔹 Plugin & theme system (hot-reload capable)
- 🔹 Role-based permissions (Admin, Editor, Author, Viewer)
- 🔹 Frontend admin dashboard (content editor, settings, analytics)
- 🔹 REST + GraphQL API dual support
- 🔹 Markdown + WYSIWYG dual editor
- 🔹 API documentation (Swagger + ReDoc)

**Target Users:** Developers integrating MapleCMS into client projects.

**Release:** `v2.0.0`

---

## 🤖 Phase 3 — AI & Automation
**Goal:** Introduce intelligent tools for content creation and optimization.

**Deliverables:**
- 🧠 AI-assisted content writing using GPT APIs
- 🧩 Auto image tagging, captioning, and metadata generation
- 🔍 SEO automation (keyword suggestions, readability analysis)
- 🪶 Content summarization and translation tools
- 🔔 Smart notifications (Slack/email integrations)
- 📊 Analytics dashboard for engagement insights

**Target Users:** Content creators, marketing teams, and AI enthusiasts.

**Release:** `v3.0.0`

---

## ☁️ Phase 4 — MapleCloud (SaaS Platform)
**Goal:** Evolve MapleCMS into a hosted multi-tenant SaaS platform.

**Deliverables:**
- 🌐 Multi-tenant architecture (orgs, teams, projects)
- 💳 Billing & subscription management (Stripe)
- 🔑 OAuth login (Google, GitHub, etc.)
- 🧱 Dedicated tenant storage (DB schema per client)
- 🚀 Auto-scaling AWS infrastructure (ECS, RDS, CloudFront)
- 🧾 Admin & audit logs, usage analytics
- 🧩 Template marketplace (themes, plugins)

**Target Users:** Startups, content agencies, and educational organizations.

**Release:** `v4.0.0`

---

## 🧭 Phase 5 — Ecosystem & Community
**Goal:** Establish MapleCMS as a community-driven open-source ecosystem.

**Deliverables:**
- 🌿 Official website & documentation portal (maplecms.dev)
- 🧰 CLI tool for project scaffolding (`maple create mysite`)
- 🤝 Open-source contributor program
- 📦 Package registry for community plugins & templates
- 🎓 Developer tutorials, webinars, and GitHub discussions

**Target Users:** Global developer and open-source community.

**Release:** Continuous (post `v4.0.0`)

---

## 📊 Feature Matrix Summary
| Feature | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|----------|----------|----------|----------|----------|----------|
| CRUD + Auth | ✅ | ✅ | ✅ | ✅ | ✅ |
| Plugin System | ❌ | ✅ | ✅ | ✅ | ✅ |
| GraphQL API | ❌ | ✅ | ✅ | ✅ | ✅ |
| AI Writing | ❌ | ❌ | ✅ | ✅ | ✅ |
| Multi-Tenancy | ❌ | ❌ | ❌ | ✅ | ✅ |
| Marketplace | ❌ | ❌ | ❌ | ✅ | ✅ |
| Community Tools | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 🧾 Long-Term Vision
> MapleCMS will evolve from a lightweight developer tool into a complete **AI-powered content ecosystem** — where open-source collaboration meets modern cloud architecture.

**Strategic Goals:**
1. Maintain **lightweight architecture** (sub-100MB container images)
2. Ensure **99.9% uptime** via AWS-native scaling
3. Integrate **AI assistants** for editorial support
4. Build **developer marketplace** for plugins and templates
5. Become the **default CMS choice** for small teams and educational creators

---

## 🕓 Timeline Overview
| Year | Focus | Version |
|------|--------|----------|
| 2025 | Core + Developer Experience | `v1.0` → `v2.0` |
| 2026 | AI + Automation | `v3.0` |
| 2027 | Cloud SaaS Platform | `v4.0` |
| 2028+ | Community Ecosystem | Ongoing |

---

> MapleCMS Roadmap is iterative — community contributions and user feedback directly shape its future.
