# 🌿 MapleCMS — The World's Lightest Open-Source CMS

MapleCMS is a **modern, ultra-light, open-source Content Management System** built with **FastAPI**, **Next.js**, and **AWS-native infrastructure**.  
It's designed for developers who want speed, simplicity, and full control — without the bloat of traditional CMS platforms.

---

## ✨ Key Features

- ⚡ **Blazing Fast** — Async FastAPI backend + Next.js frontend
- 🧩 **Modular Architecture** — Frontend and backend decoupled
- ☁️ **Cloud-Native** — Deploy easily to AWS with ready Terraform templates
- 🧠 **Developer-First** — Markdown or API-driven content
- 🔒 **Secure by Default** — JWT auth, HTTPS, and IAM-based storage
- 🤖 **AI-Ready** — Integrate GPT-powered assistants for content creation
- 🧱 **Extensible** — Plugin & theme system for blogs, docs, or learning portals

---

## 🚀 Quick Start

### Prerequisites

- Node.js ≥ 18
- Python ≥ 3.11
- Docker & Docker Compose
- AWS CLI (optional for cloud deploy)

### Clone & Run Locally

```bash
git clone https://github.com/Aviat-at/mapleCMS
cd maplecms

# Run backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Run frontend (Next.js)
cd frontend
npm install
npm run dev
```

Then visit 👉 http://localhost:3000

---

## 🧭 Project Structure

```
maplecms/
├── backend/              # FastAPI app
├── frontend/             # Next.js app
├── infra/                # Docker, Terraform, CI/CD
├── docs/                 # Documentation folder
├── tests/                # Unit & integration tests
└── README.md
```

---

## 🧰 Tech Stack

| Layer | Technology | Description |
|-------|------------|-------------|
| Frontend | Next.js + TypeScript | Fast, SEO-friendly UI |
| Backend | FastAPI | Async REST API |
| Database | PostgreSQL | Structured data store |
| Storage | AWS S3 | Media files |
| Infra | Terraform + Docker | IaC and containerization |
| CI/CD | GitHub Actions | Automated deploys |

---

## 🧑‍💻 Contributing

We welcome contributors of all skill levels!

Please read the `CONTRIBUTING.md` file before submitting PRs.

**To contribute:**

1. Fork the repo
2. Create a branch (`feature/your-feature`)
3. Commit changes
4. Open a Pull Request 🚀

---

## 🗺 Roadmap

- ✅ **Phase 1** – Core CMS (FastAPI + Next.js)
- 🔜 **Phase 2** – Plugin system & themes
- 🔮 **Phase 3** – AI-assisted authoring
- 🌐 **Phase 4** – Multi-tenant SaaS (MapleCloud)

See `docs/roadmap.md` for full details.

---

## 🛡 License

Released under the **MIT License** — free for personal and commercial use.

See `LICENSE` for details.

---

## 🌍 Community

Join discussions, contribute ideas, and help shape the future of MapleCMS.

Follow us on **GitHub Issues** and share your feedback!

---

*Built with ❤️ in Waterloo, Canada — for developers everywhere.*
