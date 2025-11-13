.PHONY: help install dev test lint format clean docker-build docker-up docker-down migrate init-db

help:
	@echo "MapleCMS Backend - Available Commands"
	@echo "======================================"
	@echo "install      - Install dependencies"
	@echo "dev          - Run development server"
	@echo "test         - Run tests"
	@echo "test-cov     - Run tests with coverage"
	@echo "lint         - Run linters"
	@echo "format       - Format code"
	@echo "clean        - Clean temporary files"
	@echo "docker-build - Build Docker image"
	@echo "docker-up    - Start Docker containers"
	@echo "docker-down  - Stop Docker containers"
	@echo "migrate      - Run database migrations"
	@echo "init-db      - Initialize database with sample data"

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

lint:
	ruff check app/
	mypy app/

format:
	black app/
	ruff check --fix app/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/
	rm -f .coverage
	rm -f test.db

docker-build:
	docker build -t maplecms-backend:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	alembic upgrade head

init-db:
	python scripts/init_db.py
