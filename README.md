# Enterprise Incident Management System

A full-stack incident management application designed to help teams create, track, update, assign, and manage enterprise incidents through a role-based web application.

The system provides secure user authentication, incident lifecycle management, admin controls, REST APIs, PostgreSQL persistence, containerized deployment with Docker, and automated backend testing through GitHub Actions.

## 🚀 Key Features

* 🔐 JWT-based user authentication
* 👥 Role-based access control (User / Admin)
* 📝 Create and update incidents
* 📋 View and filter incidents
* 👨‍💻 Assign incidents to users
* 🗑️ Admin-only incident deletion
* 🐘 PostgreSQL database
* ⚡ FastAPI REST backend
* ⚛️ React frontend
* 🐳 Docker & Docker Compose
* 🧪 Automated API tests with Pytest
* 🔄 GitHub Actions CI pipeline

## 🏗️ Architecture


                    ┌─────────────────────┐
                    │    React Frontend   │
                    │      Port: 5173     │
                    └──────────┬──────────┘
                               │
                         HTTP / REST API
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │      Port: 8000     │
                    └──────────┬──────────┘
                               │
                         SQLAlchemy ORM
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PostgreSQL DB    │
                    │      Port: 5432     │
                    └─────────────────────┘

              Docker Compose
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     Frontend    Backend     PostgreSQL
```

### Application Flow

1. Users authenticate through the React frontend.
2. The frontend sends REST API requests to the FastAPI backend.
3. FastAPI validates authentication and authorization.
4. SQLAlchemy handles database operations.
5. PostgreSQL stores users and incident records.
6. Docker Compose runs the frontend, backend, and database as separate services.
7. GitHub Actions automatically runs the backend test suite on pushes and pull requests.

## 🛠️ Tech Stack

| Layer            | Technologies                   |
| ---------------- | ------------------------------ |
| Frontend         | React, JavaScript, Vite, Axios |
| Backend          | Python, FastAPI                |
| Database         | PostgreSQL                     |
| ORM              | SQLAlchemy                     |
| Authentication   | JWT, Passlib, bcrypt           |
| Testing          | Pytest                         |
| Containerization | Docker, Docker Compose         |
| CI/CD            | GitHub Actions                 |
| Version Control  | Git, GitHub                    |

## 👤 User Capabilities

* Register a new account
* Login securely using JWT authentication
* View available incidents
* Create new incidents
* Edit incident details
* View incident status, priority, and assignment
* Logout securely

## 👑 Admin Capabilities

In addition to standard user capabilities, administrators can:

* Assign incidents to users
* Delete incidents
* Manage incidents based on their role permissions

## 🔐 Security & Authorization

The backend implements role-based authorization using JWT authentication.

Protected API endpoints require a valid access token, while admin-only operations additionally verify that the authenticated user has the `admin` role.

## 🐳 Running the Project with Docker

### Prerequisites

Make sure you have:

* Docker Desktop
* Git

### 1. Clone the repository

```bash
git clone https://github.com/NEH073/enterprise-incident-management.git
cd enterprise-incident-management
```

### 2. Start the application

```bash
docker compose up --build
```

This starts three services:

* **Frontend** — React application
* **Backend** — FastAPI REST API
* **PostgreSQL** — Application database

### 3. Access the application

Frontend:

```text
http://localhost:5173
```

Backend API:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

### 4. Stop the application

```bash
docker compose down
```

To stop the containers while keeping the PostgreSQL data volume:

```bash
docker compose down
```
## 🧪 Testing

The backend includes automated API tests using **Pytest**.

Run the tests locally:

```bash
cd backend
pytest
```

Current test coverage includes:

* Health/root endpoint
* Authentication
* User registration
* User login
* JWT-protected endpoints
* User authorization
* Admin authorization
* Incident creation
* Incident deletion
* Incident filtering
* Pagination

### Test Result

```text
10 passed
```

## 🔄 CI/CD

The project uses **GitHub Actions** for continuous integration.

The CI pipeline automatically:

1. Checks out the repository
2. Sets up Python
3. Starts a PostgreSQL service
4. Installs backend dependencies
5. Runs the complete Pytest suite

The workflow runs automatically on:

* Pushes to `main`
* Pull requests targeting `main`

This helps ensure that backend changes are automatically validated before being merged.

## 📡 API Endpoints

### Authentication

| Method | Endpoint    | Description                      |
| ------ | ----------- | -------------------------------- |
| POST   | `/register` | Register a new user              |
| POST   | `/login`    | Authenticate user and obtain JWT |
| GET    | `/me`       | Get current authenticated user   |

### Incidents

| Method | Endpoint          | Description        |
| ------ | ----------------- | ------------------ |
| GET    | `/incidents`      | Retrieve incidents |
| POST   | `/incidents`      | Create an incident |
| PUT    | `/incidents/{id}` | Update an incident |
| DELETE | `/incidents/{id}` | Delete an incident |

### API Documentation

FastAPI automatically generates interactive API documentation:

```text
http://localhost:8000/docs
```

You can use Swagger UI to test the available REST endpoints directly from the browser.

## ⭐ Project Highlights

* Built a full-stack enterprise incident management application using **React, FastAPI, and PostgreSQL**.
* Implemented **JWT authentication and role-based authorization** for users and administrators.
* Designed REST APIs for incident creation, retrieval, updating, filtering, assignment, and deletion.
* Containerized the application using **Docker and Docker Compose**.
* Added automated backend API testing with **Pytest**.
* Implemented a **GitHub Actions CI pipeline** to automatically run tests against PostgreSQL.
* Structured the application into separate frontend, backend, and database services for easier development and deployment.

## 📌 Project Status

The application is currently functional with authentication, role-based access control, incident management, Docker-based deployment, automated testing, and CI validation.

## 📄 License

This project is intended for learning, portfolio, and demonstration purposes.
