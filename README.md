# AI-Native Inventory & Operations Management Platform

A full-stack inventory and order-management application built with **FastAPI, SQLAlchemy, MySQL, React, and Vite**. The project demonstrates modular backend architecture, inventory tracking across warehouses, order allocation, JWT authentication, refresh-token rotation, role-based access control (RBAC), and automated testing.

> **Project status:** The planned Day 8 implementation has been committed to GitHub. End-to-end acceptance checks through Stage 6 have been reported as passing by the developer. Review the limitations section before treating this as production-ready.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Repository Structure](#repository-structure)
- [Business Workflow](#business-workflow)
- [Authentication and Authorization](#authentication-and-authorization)
- [API Documentation](#api-documentation)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Installation and Running](#installation-and-running)
- [Testing](#testing)
- [Known Limitations and Security Notes](#known-limitations-and-security-notes)
- [Potential Future Improvements](#potential-future-improvements)

## Overview

Inventory operations often require teams to track products across multiple warehouses, allocate stock to customer orders, and prevent overselling. This application provides a backend API and React frontend for managing product and warehouse records, inventory quantities, and order workflows.

The backend uses routers, services, repositories, schemas, and SQLAlchemy models to separate HTTP handling, business logic, data access, validation, and persistence.

## Features

- Product and warehouse management.
- Inventory tracking by product–warehouse combination.
- Order creation and warehouse allocation workflow.
- Inventory integrity checks and transactional/concurrency-focused implementation.
- User registration and login.
- Password hashing.
- JWT access-token validation and refresh-token rotation.
- Role-based authorization enforced by the backend.
- React pages for dashboard, products, warehouses, inventory, orders, analytics, login, and registration.
- Automated tests covering authentication, authorization, inventory integrity, core workflows, full-stack workflows, registration, and refresh-token behavior.

The presence of an analytics or inventory-insights interface should not be interpreted as proof that a trained demand-forecasting model is included. Document or advertise a specific forecasting model only if its implementation is present and verified.

## Technology Stack

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- MySQL
- JWT-based authentication
- Pytest

### Frontend
- React
- Vite
- Axios
- React Router
- Tailwind CSS

Exact package versions are defined by the project dependency files where applicable.

## Architecture

The backend follows a layered structure:

1. **Routers** — expose HTTP endpoints and coordinate request handling.
2. **Schemas** — validate incoming data and define response shapes.
3. **Services** — implement application and business logic.
4. **Repositories** — encapsulate database access.
5. **Models** — define SQLAlchemy database entities.
6. **Core** — contains configuration, database setup, security, dependencies, and exception handling.

The frontend calls the backend through an Axios API client. Authentication state is managed through React context, and protected routes require an authenticated session. Frontend route visibility is a usability feature; the backend remains responsible for enforcing authorization.

## Repository Structure

```text
inventory-platform/
├── app/
│   ├── core/           # Configuration, database, security, dependencies, exceptions
│   ├── models/         # SQLAlchemy models
│   ├── repositories/   # Data-access layer
│   ├── routers/        # FastAPI endpoints
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/       # Business/application logic
│   └── main.py         # FastAPI application entry point
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── context/
│   │   ├── layouts/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── vite.config.js
├── tests/              # Pytest suite
├── Documentations/     # Project documentation
├── .env                # Local backend configuration (do not commit)
├── requirements.txt    # Python dependencies; currently needs to be populated
└── README.md
```

The exact contents may evolve as the project develops.

## Business Workflow

A typical workflow is:

1. Authenticate as a user.
2. Create or review products and warehouses.
3. Initialize or update stock for a product in a warehouse.
4. Create an order for a requested product quantity.
5. Allocate the order against available stock according to the implemented allocation logic.
6. Verify the order/allocation records and inventory quantities.
7. Handle insufficient stock without leaving inconsistent inventory or partial allocations.

The precise order lifecycle and the point at which stock is deducted should be confirmed against the implementation and API responses.

## Authentication and Authorization

The application provides registration and login endpoints and uses JWT access tokens for authenticated API requests. Refresh tokens are stored in the database in hashed form and rotated when refreshed. The backend loads the current user and checks their role for restricted operations.

The implemented role policy is:

| Resource | Read | Create | Update | Delete |
|---|---|---|---|---|
| Products | All authenticated roles | Admin | Admin | Admin |
| Warehouses | All authenticated roles | Admin | Admin | Admin |
| Inventory | All authenticated roles | Admin, Manager | Admin, Manager | Admin |
| Orders | All authenticated roles | All authenticated roles | Admin, Manager | Admin |

Public registration assigns the `employee` role; clients must not be allowed to choose an elevated role during public registration.

## API Documentation

Start the backend and open the automatically generated Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Common endpoint groups include authentication, products, warehouses, inventory, and orders. Use the exact paths and schemas shown in Swagger UI because route prefixes may change.

Authentication endpoints implemented for the project include:

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`

## Prerequisites

Install the following before running the project:

- Python 3.12 or a compatible version supported by the dependencies.
- Node.js and npm.
- MySQL Server.
- Git.

## Configuration

### Backend environment

Create a local `.env` file in the repository root. Use the variable names expected by `app/core/config.py`; inspect that file before configuring a new environment. Typical configuration categories include:

- MySQL connection settings.
- JWT access-token secret and expiry.
- Separate refresh-token secret and expiry.
- Any application-specific settings required by the configuration module.

Use strong, unique secrets in local development and deployment. Never commit `.env`, real credentials, signing keys, or tokens to Git.

### Frontend environment

The frontend uses `VITE_API_URL_BASE` to identify the backend API base URL. For local development, the value is commonly:

```dotenv
VITE_API_URL_BASE=http://127.0.0.1:8000
```

Vite exposes variables prefixed with `VITE_` to browser code. Do not place passwords, database credentials, JWT secrets, or other server-side secrets in frontend environment variables.

## Installation and Running

The repository's root `requirements.txt` was empty at the time this README was drafted. Populate it with the actual backend dependencies before relying on `pip install -r requirements.txt` for a fresh installation.

### 1. Clone the repository

```powershell
git clone https://github.com/dharmpreet468/ai-native-inventory-platform.git
cd ai-native-inventory-platform
```

### 2. Create and activate a Python virtual environment

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies used by the project. Once `requirements.txt` contains the verified dependencies, use:

```powershell
pip install -r requirements.txt
```

### 3. Configure MySQL and environment variables

Create the development database, configure the local root `.env` using the names expected by `app/core/config.py`, and ensure MySQL is running. Do not copy real secrets into this README.

### 4. Start the backend

From the repository root, with the virtual environment active:

```powershell
uvicorn app.main:app --reload
```

The API is typically available at `http://127.0.0.1:8000`, with Swagger UI at `http://127.0.0.1:8000/docs`.

### 5. Configure and start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
```

Create `frontend/.env` with the appropriate `VITE_API_URL_BASE` value, then run:

```powershell
npm run dev
```

Open the local URL printed by Vite (commonly `http://localhost:5173`).

### 6. Build the frontend

From the `frontend` directory:

```powershell
npm run build
```

## Testing

Run the backend tests from the repository root with the virtual environment activated:

```powershell
pytest -v
```

The tests use the database and settings configured for the test run. Ensure you understand the test database configuration before running tests against any database containing important data. Some integration tests may create persistent test records if the database setup does not isolate or roll them back.

Build the frontend separately:

```powershell
cd frontend
npm run build
```

The developer reported 45 passing backend tests and a successful frontend production build during the Day 8 checkpoint. Re-run these commands against the current checkout to verify the present state.

## Known Limitations and Security Notes

- The refresh token is held in JavaScript memory in the current frontend implementation. A full page reload loses it; if the access token is also expired, automatic refresh cannot recover the session using that in-memory token.
- Frontend logout clears local authentication state. A dedicated server-side logout/revocation endpoint was not implemented at the time this README was drafted.
- These limitations should be reviewed before production deployment. Consider an appropriately secured refresh-token cookie strategy, CSRF protections where applicable, explicit server-side revocation/logout, rate limiting, secure transport, and deployment-specific secret management.
- Automated tests and manual acceptance checks are useful evidence but do not replace a security audit or penetration test.
- Do not claim production readiness or a trained AI demand-forecasting model unless those requirements have been implemented and verified.

## Potential Future Improvements

- Harden refresh-token persistence and logout/revocation.
- Add deployment configuration, migrations, observability, and structured audit logs.
- Add CI automation for tests and frontend builds.
- Expand operational monitoring and performance tests.
- Implement and evaluate a demand-forecasting model if forecasting is a project requirement, documenting its dataset, evaluation method, and limitations.

## Repository

GitHub: https://github.com/dharmpreet468/ai-native-inventory-platform
