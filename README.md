# BlogFastAPI

A robust REST API for a simple blogging platform with user authentication, role-based access control, and post management.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Authentication](#authentication)
- [Database](#database)
- [Docker](#docker)
- [Security and Vulnerability Scanning](#security-and-vulnerability-scanning)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

BlogFastAPI is a minimalist blogging platform backend service that provides:

- User authentication and authorization with JWT tokens
- Role-based access control (SUPER, EDITOR, USER)
- Blog post creation, management, and publishing
- Asynchronous database operations
- RESTful API design with Pydantic validation
- Comprehensive API documentation

This backend service handles user management, authentication, and blog content operations through a clean REST API.

## Features

Current features include:

- User registration and authentication with JWT
- Role-based access control with three tiers (SUPER, EDITOR, USER)
- Blog post CRUD operations with draft/published states
- Asynchronous database operations with SQLAlchemy
- Automatic database table creation on startup
- Initial superuser setup for development
- Comprehensive request/response validation
- Interactive API documentation (Swagger UI and ReDoc)
- Health check endpoint
- Docker containerization

## Tech Stack

### Backend

- **Python 3.12** - Programming language
- **FastAPI 0.135.1** - Web framework
- **SQLAlchemy 2.0.35** - ORM with async support
- **Pydantic 2.9.1** - Data validation
- **asyncpg 0.29.0** - PostgreSQL async driver
- **python-jose 3.3.0** - JWT token handling
- **passlib 1.7.4** - Password hashing

### Database

- **PostgreSQL 16** - Relational database

### DevOps

- **Docker** - Container technology
- **Docker Compose** - Multi-container orchestration

## Quick Start

### Prerequisites

Ensure you have installed:

- Python 3.12 or higher
- Docker - https://docs.docker.com/engine/install/
- Docker Compose - Bundled with Docker Desktop
- Git

### Running the Application

1. Clone the repository:

```bash
git clone https://github.com/Caio-GBrayner/BlogFastAPI.git
cd BlogFastAPI
```

2. Start the application with Docker Compose:

```bash
docker-compose up --build
```

3. Access the API:

```
http://localhost:8000/
```

4. Check health status:

```bash
curl http://localhost:8000/health
```

The application will be ready once PostgreSQL is healthy and the FastAPI server starts.

## Installation

### Setup Environment Variables

Create a `.env` file in the project root or Or just rename the .env.example file to .env. :

```bash
# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=blog_db
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/blog_db

# JWT Configuration
JWT_SECRET=your-secret-key-here-minimum-32-characters-required
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# API Configuration
API_V1_STR=/api/v1

# Initial Superuser
FIRST_SUPERUSER_EMAIL=admin@blog.local
FIRST_SUPERUSER_PASSWORD=admin123
FIRST_SUPERUSER_USERNAME=admin
```

### Local Development (without Docker)

1. Create a Python virtual environment:

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Export environment variables (or use .env file with python-dotenv):

```bash
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/blog_db"
export JWT_SECRET="your-secret-key-here"
```

4. Run the application:

```bash
uvicorn app.main:app --reload
```

## Project Structure

```
BlogFastAPI/
├── app/
│   ├── main.py                          # Application entry point
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── api.py                   # API router
│   │   │   └── endpoints/
│   │   │       ├── auth.py              # Authentication endpoints
│   │   │       ├── users.py             # User endpoints
│   │   │       └── posts.py             # Blog post endpoints
│   │   │
│   │   └── deps.py                      # Dependency injection
│   │
│   ├── core/
│   │   ├── config.py                    # Application configuration
│   │   └── security.py                  # JWT and password utilities
│   │
│   ├── models/
│   │   ├── user.py                      # User SQLAlchemy model
│   │   └── post.py                      # Post SQLAlchemy model
│   │
│   ├── schemas/
│   │   ├── user.py                      # User Pydantic schemas
│   │   ├── token.py                     # Token Pydantic schemas
│   │   └── post.py                      # Post Pydantic schemas
│   │
│   ├── services/
│   │   ├── auth_service.py              # Authentication business logic
│   │   ├── user_service.py              # User business logic
│   │   └── post_service.py              # Post business logic
│   │
│   └── db/
│       ├── session.py                   # Database session management
│       ├── base.py                      # SQLAlchemy declarative base
│       └── init_db.py                   # Database initialization
│
├── tests/                               # Test files
│   └── test_health.py                   # Health check tests
│
├── .env.example                         # Environment variables template
├── docker-compose.yml                   # Docker Compose configuration
├── Dockerfile                           # Docker image definition
├── requirements.txt                     # Python dependencies
├── .gitignore                           # Git ignore rules
├── README.md                            # This file
└── LICENSE

```

## API Endpoints

### Authentication

```
POST   /api/v1/auth/login                Login with credentials
```

### Users

```
POST   /api/v1/users/register            Register new user
GET    /api/v1/users/me                  Get authenticated user profile
```

### Blog Posts

```
GET    /api/v1/posts/                    List all published posts
GET    /api/v1/posts/{post_id}           Get post by ID
POST   /api/v1/posts/                    Create new post (EDITOR/SUPER)
PUT    /api/v1/posts/{post_id}           Update post (EDITOR/SUPER)
DELETE /api/v1/posts/{post_id}           Delete post (SUPER only)
```

### Health

```
GET    /health                           Health check endpoint
```

## Testing the API

All endpoints can be tested interactively through the built-in API documentation interfaces. Once the application is running, access:

### Swagger UI

Interactive API documentation with full testing capabilities:

```
http://localhost:8000/docs
```

The Swagger UI allows you to:
- View all available endpoints
- See request and response schemas
- Test endpoints directly with different parameters
- Authenticate with bearer tokens
- View status codes and error responses

### ReDoc

Alternative API documentation (read-only):

```
http://localhost:8000/redoc
```

### Using Swagger UI to Test Endpoints

1. Open http://localhost:8000/docs
2. Click "Authorize" and enter your JWT token (obtained from login endpoint)
3. Click on any endpoint to expand its details
4. Click "Try it out"
5. Fill in required parameters
6. Click "Execute" to send the request
7. View the response in real-time

### Example: Test Post Creation in Swagger

1. POST /api/v1/auth/login - Authorize button, enter username and password
2. Copy the access_token from response
3. Click "Authorize" and paste the token
4. POST /api/v1/posts/ - Try it out, enter post details
5. Click Execute to create a post

The API uses JWT (JSON Web Tokens) for stateless authentication.

### Request Header

Include the JWT token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Login Flow

1. User sends credentials to POST /api/v1/auth/login
2. Backend validates and returns JWT token
3. Client stores token in localStorage or session
4. Include token in all subsequent requests
5. Token expires after configured duration (default: 60 minutes)

### Example: Authenticate and Create Post

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}

# 2. Create post with token
curl -X POST http://localhost:8000/api/v1/posts/ \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my blog post",
    "excerpt": "A brief summary"
  }'
```

## Database

The application uses PostgreSQL 16 as the primary database.

### Database Initialization

Database tables are automatically created on application startup through SQLAlchemy. The initial superuser is also created during startup if it does not exist.

### Key Tables

- users - User accounts and authentication data
- posts - Blog post content and metadata

### Role Hierarchy

- SUPER - Administrator with all permissions
- EDITOR - Can create and edit own posts
- USER - Read-only access to published posts

## Docker

### Running with Docker Compose

Start all services:

```bash
docker-compose up --build
```

Run in background:

```bash
docker-compose up -d
```

View logs:

```bash
docker-compose logs -f app
docker-compose logs -f db
```

Stop services:

```bash
docker-compose down
```

Clean database and volumes:

```bash
docker-compose down -v
```

### Docker Components

- **db** - PostgreSQL 16 database service
- **app** - FastAPI application service

Both services are configured with proper networking and volume management.

## Security and Vulnerability Scanning

This project includes comprehensive security scanning to identify and track vulnerabilities in dependencies and Docker images.

### Docker Scout

Docker Scout analyzes Docker images for vulnerabilities:

```bash
# Scan the built Docker image
docker scout cves BlogFastAPI:latest
```

The Docker Scout report is available in:

```
docs/security/docker-scout_report-04-2026.txt
```

This report identifies:
- Known vulnerabilities in base images
- Severity levels and CVE information
- Remediation recommendations
- Image layers analysis

### Safety

Safety checks Python dependencies for known security vulnerabilities:

```bash
# Scan installed packages
safety check

# Generate report
safety report > safety_report.txt
```

The Safety report is available in:

```
docs/security/safety_report-04-2026.txt
```

This report identifies:
- Vulnerable Python packages
- CVE and security advisory references
- Recommended updates
- Version compatibility information

### Running Security Scans

To keep security reports up-to-date:

```bash
# Install safety (if not already installed)
pip install safety

# Run safety scan on current environment
safety check --file requirements.txt

# Build Docker image and scan with scout
docker build -t blog-fastapi:latest .
docker scout cves blog-fastapi:latest
```

### Security Best Practices

- Keep dependencies updated regularly
- Review security reports before deployment
- Use environment variables for sensitive data (never commit .env)
- Implement rate limiting for production
- Use HTTPS in production
- Rotate JWT secrets regularly
- Keep PostgreSQL updated

All security concerns should be addressed before deploying to production.

## Development

### Running Tests

Execute the test suite:

```bash
pytest tests/
```

Run tests with coverage:

```bash
pytest tests/ --cov=app
```

### API Testing

You have multiple options to test the API:

#### Interactive Testing (Recommended)

Use Swagger UI for immediate testing without command line:

```
http://localhost:8000/docs
```

This allows real-time testing of all endpoints with live responses.

#### Command Line Testing

Test endpoints using curl:

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# List posts
curl http://localhost:8000/api/v1/posts/
```

### API Documentation

Access interactive API documentation:

- Swagger UI (recommended for testing): http://localhost:8000/docs
- ReDoc (alternative view): http://localhost:8000/redoc

Both interfaces provide complete endpoint documentation with authentication support.

### Database Access

Access PostgreSQL directly:

```bash
docker exec -it blog_db psql -U postgres -d blog_db
```

### Code Style

Follow these guidelines:

- Use type hints for all functions
- Follow PEP 8 naming conventions
- Document complex functions with docstrings
- Keep functions focused and single-purpose
- Use async/await for I/O operations

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: git checkout -b feature/my-feature
4. Make your changes with clear commit messages
5. Push to your fork: git push origin feature/my-feature
6. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

Last updated: April 6, 2026
Version: 1.0.0-MVP
