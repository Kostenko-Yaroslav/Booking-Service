# Booking Service API

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Django](https://img.shields.io/badge/django-6.0.1-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)
![Postgres](https://img.shields.io/badge/postgres-15-blue)
![Docker](https://img.shields.io/badge/docker-compose-orange)
![Celery](https://img.shields.io/badge/celery-5.6.2-green)

A REST API service for a room booking system. This application focuses on data integrity, asynchronous task processing, and robust architectural patterns.

## 🔗 Live Links (Deployment)  
  
| Resource | Link |  
| --- | --- |  
| **🚀 Live API Demo (Swagger)** | [https://yaroslav-kostenko.dev/docs/](https://yaroslav-kostenko.dev/docs/) |  
| **📘 Interactive Docs (Redoc)** | [https://yaroslav-kostenko.dev/redoc/](https://yaroslav-kostenko.dev/schema/redoc/) |  
  

---

## Project Overview

### Technology Stack
* **Core:** Python 3.12, Django 6.0, Django Rest Framework
* **Database:** PostgreSQL 15 (utilizing `ExclusionConstraint` and `DateRangeField`)
* **Async Tasks:** Celery & Redis (Email notifications, PDF generation)
* **Security:** JWT Authentication (Simple JWT)
* **Documentation:** OpenAPI 3.0 / Swagger (drf-spectacular)
* **Containerization:** Docker & Docker Compose

### Key Functionality
* **Smart Bookings:** Database-level protection against overlapping dates (Race Condition safe).
* **Rooms Management:** Advanced filtering and search for room listings.
* **Async Notifications:** Background email confirmations using Celery workers.
* **Granular Permissions:** Clean separation of access rights for Public, Authenticated, and Admin users.

---

## Quick Start

### 🐳 With Docker (Recommended)  
```bash  
# 1. Clone and enter the project  
git clone https://github.com/Kostenko-Yaroslav/Booking-Service
cd booking_service  
  
# 2. Prepare environment variables  
cp .env.example .env  
  
# 3. Build and run all services (DB, Redis, Django, Celery Worker)  
docker-compose up --build -d  
  
# 4. Run migrations  
docker-compose exec web python manage.py migrate  
  
# 5. Create a superuser (for Admin access)  
docker-compose exec web python manage.py createsuperuser  
```  
*API: http://localhost:8000 | Swagger UI: http://localhost:8000/docs/*

### Locally (Development)  
1. **Environment:** `python -m venv .venv` and `source .venv/bin/activate` (or `venv\Scripts\activate` on Windows)  
2. **Dependencies:** `pip install -r requirements.txt`  
3. **Config:** `cp .env.example .env` (fill in your DB and Redis credentials)  
4. **Database:** `python manage.py migrate`  
5. **Run Services:**  
    *   **Django:** `python manage.py runserver`  
    *   **Worker:** `celery -A config worker -l info` (requires Redis running)

---

## API Endpoints

### Authentication
| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| POST | `/auth/register/` | User registration | Public |
| POST | `/auth/login/` | Obtain JWT token | Public |
| POST | `/auth/refresh/` | Refresh JWT token | Public |

### Specialties

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| GET | `/specialties/` | List specialty | Admin  |
| GET | `/specialties/{id}/` | Get specialty details | Admin  |
| POST | `/specialties/` | Create a specialty | Admin  |

### Rooms
| Method | Endpoint | Description    | Access |
| --- | --- |----------------|--------|
| GET | `/rooms/` | List rooms (filtering, search) | Public |
| GET | `/rooms/{id}/` | Get room details | Public |
| POST | `/rooms/` | Create a room | Admin |

### Bookings
| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| GET | `/bookings/` | List my bookings | Authenticated |
| POST | `/bookings/` | Create a booking | Authenticated |
| PATCH | `/bookings/{id}/cancel/` | Cancel a booking | Owner / Staff |

---

## Quality Assurance

**Run tests via Docker:**
```bash
docker-compose exec web pytest
```

**Run tests locally:**
```bash
pytest tests/
```