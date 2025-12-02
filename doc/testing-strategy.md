# ✅ MapleCMS Testing Strategy

A comprehensive testing approach ensures MapleCMS remains **lightweight, reliable, and safe to change**. This guide covers unit, integration, end‑to‑end, performance, and security testing for both **FastAPI** and **Next.js**.

---

## 🧭 Testing Pyramid
```
E2E (Playwright)
Integration (API + DB + S3 mocks)
Unit (services, utils, components)
Static/Type checks (mypy, ruff, ESLint, TypeScript)
```

---

## 🐍 Backend (FastAPI) — Python

### Tools
- **pytest** – test runner
- **httpx** – async HTTP client
- **pytest-asyncio** – async tests
- **pytest-cov** – coverage
- **mypy** – type checking

### Example Project Layout
```
backend/app/
  api/        # routers
  services/   # business logic
  models/     # SQLAlchemy
  schemas/    # Pydantic
backend/tests/
  unit/
  integration/
```

### Unit Test Example (service)
```python
# backend/tests/unit/test_slug.py
from app.services.slugs import to_slug

def test_to_slug_basic():
    assert to_slug("Hello World!") == "hello-world"
```

### API Integration Test (with DB)
```python
# backend/tests/integration/test_articles_api.py
import pytest
from httpx import AsyncClient
from app.main import create_app

@pytest.mark.asyncio
async def test_list_articles(empty_db_session):
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/api/v1/articles/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
```

### Test DB & Fixtures
- Use **SQLite in-memory** or **Postgres test container**.
- Create `empty_db_session` and `authorized_client` fixtures.

### Coverage Targets
- **Unit:** ≥ 90%
- **Overall backend:** ≥ 80%

**Run:**
```bash
pytest -q --maxfail=1 --disable-warnings \
  --cov=app --cov-report=term-missing
```

---

## ⚛️ Frontend (Next.js + TypeScript)

### Tools
- **Jest** – unit tests
- **React Testing Library (RTL)** – component tests
- **@testing-library/jest-dom** – DOM matchers
- **ts-jest** – TS support

### Component Test Example
```tsx
// frontend/tests/components/ArticleCard.test.tsx
import { render, screen } from "@testing-library/react";
import ArticleCard from "@/components/ArticleCard";

test("renders title and link", () => {
  render(<ArticleCard title="Hello" slug="hello" />);
  expect(screen.getByText("Hello")).toBeInTheDocument();
});
```

### Coverage Targets
- **Components:** ≥ 85%
- **Overall frontend:** ≥ 80%

**Run:**
```bash
npm run test -- --coverage
```

---

## 🧪 Contract Tests (API Schema)
- Validate responses against **OpenAPI** to prevent breaking changes.
- Use FastAPI’s built‑in schema at `/openapi.json`.

```python
def test_openapi_has_articles_schema():
    from app.main import app
    schema = app.openapi()
    assert "ArticleOut" in str(schema)
```

---

## 🔗 Integration Tests (Full Stack)
Run API + DB locally with Docker Compose and execute tests against real endpoints.

```bash
docker compose -f docker-compose.test.yml up -d
pytest backend/tests/integration -q
```

Mock external services (S3, email) using:
- **moto** (AWS mocks) or **localstack**
- **pytest-mailhog** for email flows

---

## 🎭 End‑to‑End (E2E) Tests — Playwright
Use **Playwright** to simulate user journeys across the browser.

### Install & Init
```bash
npm i -D @playwright/test
npx playwright install
```

### Example E2E Test
```ts
// e2e/article.spec.ts
import { test, expect } from '@playwright/test';

test('view article list', async ({ page }) => {
  await page.goto(process.env.WEB_URL!);
  await expect(page.getByRole('heading', { name: /latest articles/i })).toBeVisible();
});
```

Run E2E nightly or on PRs with a small smoke suite.

---

## 📈 Performance & Load Testing
- **k6** (JS-based) or **Locust** (Python) for load tests.

### k6 Example
```js
// load/k6-smoke.js
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = { vus: 10, duration: '1m' };

export default function () {
  const res = http.get(`${__ENV.API_URL}/articles/`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

Run against staging after deploy; fail if p95 latency exceeds target (e.g., **< 300ms** for list endpoints).

---

## ♿ Accessibility & Visual Regressions
- **axe-core** via `jest-axe` for a11y checks in component tests.
- Optional **Playwright visual snapshots** for critical pages.

```tsx
import { axe } from 'jest-axe';
```

---

## 🔐 Security Scans
- **Bandit** for Python static security analysis.
- **pip-audit** & **npm audit** for dependency CVEs.
- Container image scans via **Trivy** in CI.

```bash
trivy image $ECR_IMAGE
```

---

## 🤖 CI Gates (GitHub Actions)

### Example Workflow (combined)
```yaml
name: Test & Lint
on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r backend/requirements-dev.txt
      - run: pytest backend -q --cov=app --cov-fail-under=80

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint && npm test -- --coverage --watch=false

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Trivy scan
        uses: aquasecurity/trivy-action@0.20.0
        with:
          scan-type: fs
          ignore-unfixed: true
          format: table
```

---

## 🧰 Test Data & Factories
- Use **factory_boy** / **faker** for backend objects.
- Provide seed scripts for local dev data.

```python
from factory import Factory, Faker
class ArticleFactory(Factory):
    class Meta: model = Article
    title = Faker('sentence')
    slug = Faker('slug')
```

---

## 🎛️ Configuration Tips
- Separate `pytest.ini`, `mypy.ini`, `.flake8`, `.eslintrc`.
- Use **.env.test** for test‑only configuration.
- Keep tests fast and deterministic; avoid sleeps, prefer time mocking.

---

## 🧭 Summary
- Unit + integration + E2E ensure correctness end‑to‑end.
- Performance, accessibility, and security are part of CI, not afterthoughts.
- Clear coverage targets and CI gates keep MapleCMS stable as it grows.
