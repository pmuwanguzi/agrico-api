# Agrico API Backend

This is the backend API for the Agrico Farm Management System built with Flask.

## Setup

1. Create a virtual environment and activate it:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended psycopg2-binary python-dotenv
```

3. Create a `.env` file in the `backend` directory with your database configuration:
```env
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_db_name
JWT_SECRET_KEY=your_secret_key
```

## Running the Server

From the `backend` directory:
```bash
python run.py
```
The server will start at `http://127.0.0.1:5000`

## API Routes

### Authentication Routes

All authentication routes are prefixed with `/auth`

#### Create Account (Signup)
- **URL**: `POST /auth/signup`
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "secretpassword",
    "role": "farmer"  // optional, defaults to "farmer"
}
```
- **Success Response** (201):
```json
{
    "message": "User john@example.com created successfully"
}
```

#### Login
- **URL**: `POST /auth/login`
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
    "email": "john@example.com",
    "password": "secretpassword"
}
```
- **Success Response** (200):
```json
{
    "message": "Login successful",
    "access_token": "your.jwt.token",
    "user": {
        "id": 1,
        "full_name": "John Doe",
        "email": "john@example.com",
        "role": "farmer"
    }
}
```

### Test Routes

#### List All Routes
- **URL**: `GET /auth/test`
- **Description**: Returns a list of all registered routes in the application
- **No authentication required**

## Testing with PowerShell

### List Routes
```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/auth/test' -Method Get
```

### Create Account
```powershell
$body = @{
    full_name = "John Doe"
    email = "john@example.com"
    password = "secretpassword"
    role = "farmer"
}
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/auth/signup' -Method Post -ContentType 'application/json' -Body ($body | ConvertTo-Json)
```

### Login
```powershell
$body = @{
    email = "john@example.com"
    password = "secretpassword"
}
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/auth/login' -Method Post -ContentType 'application/json' -Body ($body | ConvertTo-Json)
```

## Database Setup

Before running the application:

1. Create the database in PostgreSQL
2. Update the `.env` file with your database credentials
3. Run the database initialization script:
```bash
python create_tables.py
```

## Database migrations (optional)

If you'd rather use migrations (recommended for evolving schemas) the project can use Flask-Migrate.

1. Install dependencies (from the `backend` folder with your venv active):
```powershell
pip install -r requirements.txt
```

2. Set the FLASK_APP environment variable and run migration commands from the `backend` folder:
```powershell
# PowerShell (session-only variable)
$env:FLASK_APP = 'run.py'

# initialize migrations (only first time)
flask db init

# generate a migration from models
flask db migrate -m "initial"

# apply migrations to the database
flask db upgrade
```

Notes:
- If PowerShell can't find the `flask` command, ensure your virtualenv is activated or run `python -m flask` instead. Example:
```powershell
# with venv active you can also run
python -m flask db init
```
- You can keep using `create_tables.py` as a simple alternative to migrations. Migrations are useful when the schema changes over time.

## Error Responses

- **400**: Missing required fields
- **401**: Invalid login credentials
- **409**: User already exists (on signup)