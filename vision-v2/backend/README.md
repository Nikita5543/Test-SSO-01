# NOC Vision Backend

FastAPI-based backend for NOC Vision - Network Operations Center Platform.

## Features

- User authentication with JWT tokens
- User management (CRUD operations)
- Role-based access control (admin/user)
- SQLite database (configurable for PostgreSQL)
- CORS enabled for frontend integration

## Default Credentials

- **Username:** admin
- **Password:** admin

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file (optional - uses defaults if not present):
```bash
cp .env.example .env
```

4. Run the application:
```bash
python run.py
# or
uvicorn app.main:app --reload
```

## API Documentation

Once running, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/init` - Create default admin user

### Users (Admin only)
- `GET /api/users/` - List all users
- `GET /api/users/{id}` - Get user by ID
- `POST /api/users/` - Create user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   └── users.py
│   │       └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── services/
│   │   └── user_service.py
│   └── main.py
├── requirements.txt
└── run.py
```
