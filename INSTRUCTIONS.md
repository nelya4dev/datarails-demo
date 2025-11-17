markdown# DataRails Demo - Setup Instructions

## 📋 Overview

This is a full-stack data processing application that:
- Uploads Excel files with employee and project data
- Validates and transforms data using configurable rules
- Processes files asynchronously using Celery
- Stores data in PostgreSQL
- Provides a React frontend for file upload and data viewing

## 🏗️ Architecture
```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│   React     │─────▶│   FastAPI   │─────▶│  PostgreSQL  │
│  Frontend   │      │   Backend   │      │   Database   │
└─────────────┘      └─────────────┘      └──────────────┘
                            │
                            ▼
                     ┌─────────────┐      ┌──────────────┐
                     │   Celery    │─────▶│    Redis     │
                     │   Worker    │      │    Broker    │
                     └─────────────┘      └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### 1. Clone Repository
```bash
git clone git@github.com:nelya4dev/datarails-demo.git
cd datarails-demo
```

### 2. Configure Environment

Create `.env` file in the root directory:
```bash
# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=datarails
DB_USER=datarails_user
DB_PASSWORD=your_secure_password_here

# PgAdmin
PGADMIN_DEFAULT_EMAIL=admin@datarails.com
PGADMIN_DEFAULT_PASSWORD=admin123

# Backend
CORS_ALLOW_ALL_ORIGINS=true
CORS_ALLOWED_ORIGINS=http://localhost:3000
ALLOWED_HOSTS=*
UPLOAD_DIR=uploads
UPLOAD_MAX_FILE_SIZE=10485760
APP_MODE=development
CONFIG_CSV_PATH=config/config.csv

# Celery/Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# Frontend
VITE_API_BASE_URL=http://localhost:8001
VITE_MAX_FILE_SIZE_MB=10
VITE_POLLING_INTERVAL_MS=2000
VITE_USE_MOCKS=false
```

### 3. Start Services
```bash
# Build and start all services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Celery Flower**: http://localhost:5555
- **PgAdmin**: http://localhost:5050

## 📁 Project Structure
```
datarails-demo/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   └── backend/
│   │       ├── api/        # API endpoints
│   │       ├── core/       # Configuration
│   │       ├── crud/       # Database operations
│   │       ├── models/     # SQLAlchemy models
│   │       ├── schemas/    # Pydantic schemas
│   │       ├── services/   # Business logic
│   │       └── tasks/      # Celery tasks
│   ├── alembic/            # Database migrations
│   ├── config/             # Transformation config
│   ├── docker/             # Docker files
│   └── pyproject.toml      # Python dependencies
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   └── types/         # TypeScript types
│   ├── docker/            # Docker files
│   └── package.json       # Node dependencies
│
├── docker-compose.yml     # Docker orchestration
└── .env                   # Environment variables
```

## 📊 Monitoring

### Celery Flower Dashboard

Access: http://localhost:5555

Features:
- Task monitoring
- Worker status
- Task history
- Performance metrics

### API Documentation

Access: http://localhost:8001/docs

Interactive Swagger UI for testing API endpoints.

### Database Monitoring

Access PgAdmin: http://localhost:5050

Monitor:
- Table sizes
- Query performance
- Active connections

## 🧹 Cleanup

### Remove All Data
```bash
# Stop and remove containers, volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Clean everything
docker-compose down -v --rmi all --remove-orphans
```

### Reset Database Only
```bash
# Stop services
docker-compose down

# Remove database volume
docker volume rm datarails-demo_postgres-data

# Start fresh
docker-compose up -d
```

## 🔐 Security Notes

**For Production Deployment:**

1. **Change default passwords** in `.env`
2. **Disable CORS_ALLOW_ALL_ORIGINS** (set to `false`)
3. **Set specific CORS_ALLOWED_ORIGINS**
4. **Use strong DB password**
5. **Set APP_MODE=production**
6. **Configure proper ALLOWED_HOSTS**
7. **Use HTTPS with reverse proxy (nginx)**
8. **Enable authentication/authorization**

## 📈 Performance Tips

### For Large Files

Increase upload limits in `.env`:
```bash
UPLOAD_MAX_FILE_SIZE=52428800  # 50MB
VITE_MAX_FILE_SIZE_MB=50
```
