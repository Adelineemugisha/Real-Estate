# Real Estate Backend API

A modular FastAPI backend for real estate applications, featuring user authentication, property listings, favorites, and inquiries.

## Features

- User registration & JWT authentication
- Property listing CRUD (agents only)
- Location-based property search
- Property image management
- Favorite/wishlist toggling
- Buyer inquiries
- Async SQLAlchemy with PostgreSQL (asyncpg)

## Tech Stack

- FastAPI
- SQLAlchemy (async)
- Pydantic
- PyJWT
- pytest
- SQLite (isolated test DB)

## Project Structure

```
app/
  main.py              # FastAPI app entry point
  models/              # SQLAlchemy ORM models
  schemas/             # Pydantic schemas
  repositories/        # Data access layer
  services/            # Business logic
  routers/             # API endpoints
  tests/               # Test suite
```

## Running Tests Locally

```bash
# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the test suite
pytest -v
```

Tests use an isolated SQLite database (`sqlite:///./test_real_estate.db`) and override the default PostgreSQL `get_db` dependency, so no live database is required.