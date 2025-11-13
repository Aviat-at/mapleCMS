# MapleCMS Backend

FastAPI-based backend for MapleCMS - The World's Lightest Open-Source CMS.

## Features

- ⚡ **FastAPI** - Modern, fast async Python web framework
- 🗃️ **PostgreSQL** - Robust relational database with async support
- 🔐 **JWT Authentication** - Secure token-based authentication
- 📝 **CRUD Operations** - Complete API for articles, users, categories, tags
- 🔒 **Role-Based Access Control** - Admin, Editor, Author, Viewer roles
- 📤 **File Uploads** - Media management with S3 support
- 🧪 **Testing** - Comprehensive test suite with pytest
- 🐳 **Docker** - Containerized deployment ready

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- pip or poetry

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/maplecms.git
cd maplecms/backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/api/v1/docs`

## Project Structure

```
backend/
├── app/
│   ├── api/              # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── users.py      # User management
│   │   ├── articles.py   # Article CRUD
│   │   ├── categories.py # Category management
│   │   ├── tags.py       # Tag management
│   │   └── media.py      # File upload
│   ├── core/             # Core functionality
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Database setup
│   │   ├── security.py   # Auth utilities
│   │   └── deps.py       # Dependencies
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
├── tests/                # Test suite
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout and revoke token

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/` - List all users (admin)
- `GET /api/v1/users/{id}` - Get user by ID (admin)
- `PUT /api/v1/users/{id}` - Update user (admin)
- `DELETE /api/v1/users/{id}` - Delete user (admin)

### Articles
- `GET /api/v1/articles/` - List articles
- `GET /api/v1/articles/{id}` - Get article by ID
- `GET /api/v1/articles/slug/{slug}` - Get article by slug
- `POST /api/v1/articles/` - Create article
- `PUT /api/v1/articles/{id}` - Update article
- `DELETE /api/v1/articles/{id}` - Delete article

### Categories
- `GET /api/v1/categories/` - List categories
- `GET /api/v1/categories/{id}` - Get category
- `POST /api/v1/categories/` - Create category
- `PUT /api/v1/categories/{id}` - Update category
- `DELETE /api/v1/categories/{id}` - Delete category

### Tags
- `GET /api/v1/tags/` - List tags
- `GET /api/v1/tags/{id}` - Get tag
- `POST /api/v1/tags/` - Create tag
- `PUT /api/v1/tags/{id}` - Update tag
- `DELETE /api/v1/tags/{id}` - Delete tag

### Media
- `POST /api/v1/media/upload` - Upload file
- `GET /api/v1/media/` - List media files
- `GET /api/v1/media/{id}` - Get media file
- `DELETE /api/v1/media/{id}` - Delete media file

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Docker

Build image:
```bash
docker build -t maplecms-backend .
```

Run container:
```bash
docker run -p 8000:8000 --env-file .env maplecms-backend
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `CORS_ORIGINS` - Allowed CORS origins
- `AWS_ACCESS_KEY_ID` - AWS credentials for S3
- `S3_BUCKET` - S3 bucket name

## License

MIT License - see LICENSE file for details
