# 🔧 MapleCMS Plugin System

MapleCMS supports a **Hybrid Plugin Architecture** that enables developers to extend both the backend (FastAPI) and frontend (Next.js) with modular functionality.  
This design provides maximum flexibility — allowing MapleCMS to grow into a full ecosystem of custom integrations, themes, and automation tools.

---

## 🧩 Overview

The **Hybrid Plugin System** combines:
- **Backend Plugins (FastAPI extensions):** Add APIs, jobs, or logic.
- **Frontend Plugins (Next.js extensions):** Add UI components, widgets, or pages.

Each plugin is self-contained with metadata, routes, and optional frontend components.

```
/plugins/
 ├── analytics/
 │   ├── backend/
 │   │   ├── routes.py
 │   │   ├── models.py
 │   │   └── services.py
 │   ├── frontend/
 │   │   ├── components/AnalyticsCard.tsx
 │   │   └── pages/analytics.tsx
 │   ├── plugin.json
 │   └── README.md
 └── seo/
     ├── backend/
     └── frontend/
```

---

## ⚙️ 1. Plugin Registration (Backend)

Backend plugins register themselves with the FastAPI app at startup.  
Each plugin exports a router or a setup function that the core system auto-loads.

### Example — `plugins/analytics/backend/routes.py`
```python
from fastapi import APIRouter

router = APIRouter(prefix="/plugins/analytics", tags=["Analytics"])

@router.get("/stats")
async def get_site_stats():
    return {"visits": 1024, "unique_users": 289}
```

### Auto-Registration Example
```python
# core/plugin_loader.py
from importlib import import_module
from pathlib import Path

from fastapi import FastAPI

def register_plugins(app: FastAPI):
    plugin_dirs = Path("plugins").glob("*/backend/routes.py")
    for path in plugin_dirs:
        module_path = str(path).replace("/", ".").replace(".py", "")
        module = import_module(module_path)
        app.include_router(module.router)
```

On startup, FastAPI dynamically discovers and mounts all available plugin routers.

---

## 🧱 2. Plugin Metadata

Each plugin must include a `plugin.json` manifest:
```json
{
  "name": "Analytics",
  "id": "maplecms.analytics",
  "version": "1.0.0",
  "author": "MapleCMS Team",
  "description": "Adds analytics dashboards and visitor tracking.",
  "backend": true,
  "frontend": true,
  "entry": {
    "backend": "backend.routes",
    "frontend": "frontend.components.AnalyticsCard"
  }
}
```

This allows the system to:
- Load plugins conditionally (only backend/frontend)
- Display plugin info in the admin dashboard
- Register API routes or components automatically

---

## 🖥️ 3. Frontend Plugin Loading (Next.js)

Frontend plugins extend the admin dashboard and UI with widgets or new routes.

### Example — `frontend/components/AnalyticsCard.tsx`
```tsx
import { FC, useEffect, useState } from "react";

const AnalyticsCard: FC = () => {
  const [stats, setStats] = useState({ visits: 0, users: 0 });

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/plugins/analytics/stats`)
      .then((res) => res.json())
      .then(setStats);
  }, []);

  return (
    <div className="p-4 bg-white shadow rounded-xl">
      <h2 className="text-lg font-semibold">Site Analytics</h2>
      <p>Total Visits: {stats.visits}</p>
      <p>Unique Users: {stats.unique_users}</p>
    </div>
  );
};

export default AnalyticsCard;
```

### Dynamic Component Import (Plugin Loader)
```tsx
// frontend/lib/pluginLoader.ts
export async function loadPluginComponent(id: string) {
  const manifest = await import(`../../plugins/${id}/plugin.json`);
  const comp = await import(`../../plugins/${id}/${manifest.entry.frontend}`);
  return comp.default;
}
```

---

## 🧠 4. Plugin Types

| Type | Description | Example |
|------|--------------|----------|
| **Core Extension** | Adds backend logic or routes | SEO Analyzer, Sitemap Generator |
| **UI Plugin** | Adds frontend widgets or themes | Analytics Dashboard, Comment Box |
| **Integration Plugin** | Connects external APIs | Slack Alerts, Google Drive Sync |
| **Automation Plugin** | Runs background jobs or AI tools | Auto Tagging, AI Writer |

---

## 🪣 5. Security & Isolation

- Each plugin runs **sandboxed** in its namespace.
- Plugin routes use the prefix `/plugins/<id>`.
- Frontend imports are scoped within `plugins/`.
- API validation and role checks apply globally.
- Only verified plugins (signed manifests) can be loaded in production.

---

## 🔄 6. Plugin Lifecycle

| Stage | Description |
|--------|--------------|
| **Install** | Copy plugin folder or install via CLI | `maple install plugin analytics` |
| **Load** | Detected by loader on startup/build |
| **Activate** | Enabled in admin dashboard |
| **Update** | Version bump in manifest |
| **Remove** | Uninstall from plugin registry |

---

## ☁️ 7. Marketplace Integration (Future)

MapleCMS will support an official **Plugin Marketplace** for open-source and commercial add-ons.

**Planned features:**
- 🧩 Install plugins via CLI or admin dashboard
- 🧠 Auto-discovery of community plugins from `registry.maplecms.dev`
- 🧰 Developer publishing workflow (`maple publish`)
- 🔐 Plugin signing and version verification

---

## 🧾 8. Example Plugin Ideas
- `@maplecms/seo` → SEO analyzer + sitemap generator
- `@maplecms/comments` → Commenting system with moderation
- `@maplecms/analytics` → Dashboard stats plugin
- `@maplecms/ai-writer` → GPT-powered content suggestions

---

## 🧭 Summary

- **Hybrid architecture** supports both backend and frontend extensibility.
- **FastAPI auto-discovery** mounts plugin routes dynamically.
- **Next.js integration** enables UI extensions and dashboards.
- Future **Marketplace** will enable distribution and collaboration.

> The MapleCMS plugin system is built for developers — powerful, modular, and open to innovation.
