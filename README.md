# Booking Service API

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Django](https://img.shields.io/badge/django-6.0-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.16-red.svg)
![Postgres](https://img.shields.io/badge/postgres-15-blue)
![Docker](https://img.shields.io/badge/docker-compose-orange)
![Celery](https://img.shields.io/badge/celery-5.4-green)

A professional REST API service for a room booking system. This application focuses on data integrity, asynchronous task processing, and robust architectural patterns.

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

### With Docker (Recommended)
```bash
# Clone and enter the project
git clone https://github.com/your-username/booking_service.git
cd booking_service

# Prepare environment
cp .env.example .env

# Build and run all services (DB, Redis, Django, Worker)
docker-compose up --build
```
*API: http://localhost:8000 | Swagger UI: http://localhost:8000/docs/*

### Locally (Development)
1. **Environment:** `python -m venv .venv` and `source .venv/bin/activate`
2. **Dependencies:** `pip install -r requirements.txt`
3. **Config:** `cp .env.example .env` (fill in your DB and Redis credentials)
4. **Database:** `python manage.py migrate`
5. **Run:** `python manage.py runserver`

---

## API Endpoints

### Authentication
| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| POST | `/auth/register/` | User registration | Public |
| POST | `/auth/login/` | Obtain JWT token | Public |
| POST | `/auth/refresh/` | Refresh JWT token | Public |

### Rooms
| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
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