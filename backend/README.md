# MapleCMS Backend

FastAPI-based backend for MapleCMS - a lightweight, modern content management system.

## Features

- ⚡ **Fast & Async** - Built with FastAPI and async SQLAlchemy
- 🔒 **Secure** - JWT authentication with bcrypt password hashing
- 📝 **RESTful API** - Clean, well-documented API endpoints
- 🗃️ **PostgreSQL** - Robust database with SQLAlchemy ORM
- 🧪 **Tested** - pytest-based test suite

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/          # API route handlers
│   ├── core/         # Core configuration and utilities
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic services
│   ├── tests/        # Test files
│   └── main.py       # FastAPI application entry point
├── requirements.txt  # Python dependencies
└── pytest.ini        # pytest configuration
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Articles
- `GET /api/v1/articles/` - List all articles
- `GET /api/v1/articles/{id}` - Get article by ID
- `POST /api/v1/articles/` - Create article (auth required)
- `PUT /api/v1/articles/{id}` - Update article (auth required)
- `DELETE /api/v1/articles/{id}` - Delete article (auth required)

### Categories
- `GET /api/v1/categories/` - List all categories
- `POST /api/v1/categories/` - Create category (auth required)

### Users
- `GET /api/v1/users/me` - Get current user profile (auth required)
- `GET /api/v1/users/` - List all users (auth required)

### System
- `GET /api/v1/health` - Health check
- `GET /api/v1/version` - API version info

## Testing

Run tests with pytest:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Development

### Code Quality

Format code with black:
```bash
black app/
```

Sort imports with isort:
```bash
isort app/
```

Lint with flake8:
```bash
flake8 app/
```

## License

MIT License - see the main repository LICENSE file for details.
