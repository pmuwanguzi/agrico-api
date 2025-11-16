# Agrico API Assignment Work


Farm Management System A web-based farm management system built with Flask (Backend) and modern frontend technologies.


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
pip install -r requirements.txt
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

### Livestock Routes

All livestock routes are prefixed with /livestock
Authentication Required: Yes (JWT token)

## Create Livestock Record

**URL**: POST /livestock/

**Headers**:

**Authorization**: Bearer <your_jwt_token>

**Content-Type**: application/json

**Body**:

{
    "farm_id": 1,
    "animal_type": "Cattle",
    "quantity": 15,
    "purchase_date": "2024-01-15",
    "health_status": "Healthy"
}


**Success Response (201)**:

{
    "message": "Livestock created successfully",
    "id": 5
}

## Get All Livestock for a Farm

URL: GET /livestock/<farm_id>

Headers:

Authorization: Bearer <your_jwt_token>

**Success Response (200)**:

[
    {
        "id": 1,
        "animal_type": "Goats",
        "quantity": 20,
        "purchase_date": "2024-02-01",
        "health_status": "Good"
    }
]

## Update Livestock

URL: PUT /livestock/<id>

Headers:

Authorization: Bearer <your_jwt_token>

Content-Type: application/json

Body:

{
    "animal_type": "Cattle",
    "quantity": 12,
    "purchase_date": "2024-01-20",
    "health_status": "Vaccinated"
}


Success Response (200):

{
    "message": "Livestock updated successfully"
}

## Delete Livestock

URL: DELETE /livestock/<id>

Headers:

Authorization: Bearer <your_jwt_token>

**Success Response (200)**:

{
    "message": "Livestock deleted successfully"
}

### Expenses Routes

All expenses routes are prefixed with /expenses
Note: Create/Update/Delete requires admin role

## Create Expense (Admin Only)

URL: POST /expenses/

Headers:

Authorization: Bearer <your_jwt_token>

Content-Type: application/json

Body:

{
    "farm_id": 1,
    "amount": 50000,
    "description": "Purchase of animal feeds",
    "date": "2024-01-10"
}


**Success Response (201)**:

{
    "message": "Expense created",
    "expense": {
        "expense_id": 3,
        "description": "Purchase of animal feeds",
        "amount": 50000,
        "date": "2024-01-10",
        "farm_id": 1
    }
}

## Get All Expenses for a Farm

URL: GET /expenses/<farm_id>

Headers:

Authorization: Bearer <your_jwt_token>

**Success Response (200)**:

[
    {
        "expense_id": 1,
        "description": "Veterinary services",
        "amount": 15000,
        "date": "2024-01-05",
        "farm_id": 1
    }
]

## Update Expense (Admin Only)

URL: PUT /expenses/<expense_id>

Headers:

Authorization: Bearer <your_jwt_token>

Content-Type: application/json

Body:

{
    "description": "Updated description",
    "amount": 60000,
    "date": "2024-01-12"
}


**Success Response (200)**:

{
    "message": "Expense updated",
    "expense": {
        "expense_id": 3,
        "description": "Updated description",
        "amount": 60000,
        "date": "2024-01-12",
        "farm_id": 1
    }
}

## Delete Expense (Admin Only)

URL: DELETE /expenses/<expense_id>

Headers:

Authorization: Bearer <your_jwt_token>

**Success Response (200)**:

{
    "message": "Expense deleted"
}

## Database Setup

Before running the application:

1. Create the database in PostgreSQL
2. Update the `.env` file with your database credentials
3. Run the database initialization script:
```bash
python create_tables.py
```

## Error Responses

- **400**: Missing required fields
- **401**: Invalid login credentials
- **409**: User already exists (on signup)
