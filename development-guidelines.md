# 🧑‍💻 MapleCMS Development Guidelines

These guidelines define the coding standards, branching strategy, and contribution workflow for the **MapleCMS** project. All contributors are expected to follow them to ensure clean, maintainable, and scalable code.

---

## 🧱 1. Repository Structure
```
maplecms/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/          # Route controllers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── core/         # Config, security, utilities
│   │   └── main.py       # FastAPI entry point
│   └── tests/            # Backend unit tests
│
├── frontend/             # Next.js + TypeScript app
│   ├── components/
│   ├── pages/
│   ├── lib/
│   ├── styles/
│   └── tests/
│
├── infra/                # Docker, Terraform, CI/CD configs
├── docs/                 # Project documentation
├── .github/workflows/    # GitHub Actions pipeline YAMLs
└── README.md
```

---

## 🧠 2. Code Style

### Backend (Python / FastAPI)
- Follow **PEP 8** and **PEP 257**.
- Use **type hints** everywhere.
- Use **black** for formatting, **isort** for imports.
- Apply **flake8** or **ruff** for linting.
- Prefer async functions (`async def`) for all I/O-bound operations.
- All database queries via SQLAlchemy ORM or async sessions.

**Example:**
```python
from fastapi import APIRouter, Depends
from app.schemas.article import ArticleOut
from app.services.article import get_articles

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/", response_model=list[ArticleOut])
async def list_articles():
    return await get_articles()
```

### Frontend (Next.js / TypeScript)
- Use **ESLint** + **Prettier** for linting and formatting.
- Use **functional components** and **React Hooks**.
- Use **TypeScript** types/interfaces consistently.
- Keep components small, reusable, and descriptive.
- CSS via **Tailwind** or **CSS Modules**, no inline styles.

**Example:**
```tsx
import { FC } from "react";
import Link from "next/link";

type ArticleCardProps = {
  title: string;
  slug: string;
};

const ArticleCard: FC<ArticleCardProps> = ({ title, slug }) => (
  <Link href={`/articles/${slug}`} className="block p-4 hover:bg-gray-100 rounded-lg">
    <h2 className="text-xl font-semibold">{title}</h2>
  </Link>
);

export default ArticleCard;
```

---

## 🌿 3. Commit Conventions

Follow the **Conventional Commits** standard:
```
<type>(scope): <short summary>
```

### Common Types
| Type | Purpose |
|------|----------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation-only changes |
| `style` | Code style changes (no logic impact) |
| `refactor` | Code restructure without functional change |
| `test` | Add or fix tests |
| `chore` | Maintenance tasks (build, CI, deps) |

**Example:**
```
feat(api): add endpoint for listing all articles
fix(frontend): correct missing tag rendering
```

---

## 🌳 4. Branching Strategy

We follow the **GitHub Flow** with lightweight feature branches:

```
main      → production releases
│
dev       → integration branch for staging
│
feature/* → individual feature or fix branches
```

### Rules
- Always branch from `dev`.
- Name branches descriptively: `feature/article-search`, `fix/image-upload`.
- Use pull requests (PRs) to merge into `dev`.
- Merge into `main` only after QA/staging approval.

---

## 🧪 5. Testing Standards
- Use **pytest** for backend testing.
- Use **Jest** + **React Testing Library** for frontend.
- All new features require at least minimal test coverage.
- Keep test files alongside components/services they test.

**Example:** `backend/app/tests/test_article.py`
```python
from httpx import AsyncClient

async def test_article_list(async_client: AsyncClient):
    response = await async_client.get("/api/v1/articles/")
    assert response.status_code == 200
```

---

## 🧩 6. Environment Variables
All secrets are stored in `.env` (local) or AWS Secrets Manager (prod).

### Example `.env.example`
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/maplecms
SECRET_KEY=your-secret-key
S3_BUCKET=maplecms-assets
AWS_REGION=us-east-1
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## ⚙️ 7. Code Review Checklist
✅ Code compiles without errors
✅ No console logs or unused imports
✅ Variables and functions have meaningful names
✅ Functions are small and testable
✅ API endpoints validated and documented
✅ Security-sensitive code reviewed (auth, file upload)

---

## 🧭 8. Version Control Best Practices
- Commit often; push once work is tested.
- Keep commits atomic and descriptive.
- Avoid committing `.env`, secrets, or node_modules.
- Rebase (`git pull --rebase`) instead of merge when syncing.
- Use GitHub issues to track bugs and enhancements.

---

## 🧾 9. Pre-Commit Hooks
Use **pre-commit** or **Husky** to enforce formatting and linting:
```bash
black backend/
isort backend/
flake8 backend/
npm run lint
```

---

## 💬 10. Documentation Contributions
- Update Markdown files in `/docs/` when adding new features.
- For every API change, update `api-reference.md`.
- Include screenshots or diagrams where possible.

---

> Following these conventions keeps MapleCMS maintainable, scalable, and professional — ensuring a clean experience for every contributor.
