# **Agrico Farm Management System – Backend API (Flask)**

A RESTful API for managing farm operations including authentication, livestock, expenses, sales, and farm summaries.
Built using **Flask**, **PostgreSQL**, and **JWT authentication**.

---

# ** Project Structure**

```
backend/
│── app/
│   ├── auth/          # Authentication routes
│   ├── livestock/     # Livestock routes
│   ├── expenses/      # Expense routes
│   ├── sales/         # Sales routes
│   ├── summary/       # Summary analytics
│   ├── models/        # SQLAlchemy models
│   ├── utils/         # JWT utilities and helpers
│── create_tables.py   # Database initialization
│── check_db.py        # Database connectivity test
│── run.py             # Entry point to run the server
│── requirements.txt
│── .env.example
```

---

# **🔧 Setup Instructions**

## **1. Create and Activate Virtual Environment**

### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

---

## **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **3. Create `.env` File**

Create a `.env` in the `backend/` directory.

Example:

```
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=agrico_db

JWT_SECRET_KEY=your_jwt_secret_key
```

---

# ** Database Setup**

### **1. Create PostgreSQL Database**

```sql
CREATE DATABASE agrico_db;
```

### **2. Run Table Initialization**

```bash
python create_tables.py
```

### **3. Test Database Connection**

```bash
python check_db.py
```

If successful, you will see:

```
Database connection successful!
```

---

# ** Running the Server**

```bash
python run.py
```

Server runs on:

```
http://127.0.0.1:5000
```

---

# ** API DOCUMENTATION**

---

# **1️⃣ Authentication Routes**

Prefix: **`/auth`**

---

## **🔹 Create Account (Signup)**

**POST** `http://127.0.0.1:5000/auth/signup`

**Body**

```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "StrongPass123",
  "role": "farmer"
}
```

---

## **🔹 Login**

**POST** `http://127.0.0.1:5000/auth/login`

**Body**

```json
{
  "email": "john@example.com",
  "password": "StrongPass123"
}
```

---

## **🔹 List All Routes (Test Route)**

**GET** `http://127.0.0.1:5000/auth/test`

---

# **2️⃣ Livestock Routes**

Prefix: **`/livestock`**
(JWT Required)

---

## **🔹 Create Livestock**

**POST** `http://127.0.0.1:5000/livestock/`

**Body**

```json
{
  "farm_id": 1,
  "animal_type": "Cattle",
  "quantity": 10,
  "purchase_date": "2024-01-15",
  "health_status": "Healthy"
}
```

---

## **🔹 Get Livestock by Farm**

**GET** `http://127.0.0.1:5000/livestock/<farm_id>`

---

## **🔹 Update Livestock**

**PUT** `http://127.0.0.1:5000/livestock/<livestock_id>`

**Body**

```json
{
  "animal_type": "Goat",
  "quantity": 18,
  "purchase_date": "2024-02-01",
  "health_status": "Vaccinated"
}
```

---

## **🔹 Delete Livestock**

**DELETE**
`http://127.0.0.1:5000/livestock/<livestock_id>`

---

# **3️⃣ Expenses Routes**

Prefix: **`/expenses`**
(Admin-only for CREATE/UPDATE/DELETE)

---

## **🔹 Create Expense (Admin)**

**POST** `http://127.0.0.1:5000/expenses/`

**Body**

```json
{
  "farm_id": 1,
  "amount": 45000,
  "description": "Animal feed purchase",
  "date": "2024-01-10"
}
```

---

## **🔹 Get Expenses by Farm**

**GET** `http://127.0.0.1:5000/expenses/<farm_id>`

---

## **🔹 Update Expense (Admin)**

**PUT** `http://127.0.0.1:5000/expenses/<expense_id>`

**Body**

```json
{
  "description": "Updated description",
  "amount": 50000,
  "date": "2024-01-12"
}
```

---

## **🔹 Delete Expense (Admin)**

**DELETE**
`http://127.0.0.1:5000/expenses/<expense_id>`

---

# **4️⃣ Sales Routes**

Prefix: **`/sales`**

---

## **🔹 Record Sale**

**POST** `http://127.0.0.1:5000/sales/`

**Body**

```json
{
  "farm_id": 1,
  "product": "Milk",
  "quantity": 120,
  "unit_price": 150,
  "date": "2024-01-20"
}
```

---

## **🔹 Get Sales for Farm**

**GET** `http://127.0.0.1:5000/sales/<farm_id>`

---

## **🔹 Update Sale**

**PUT** `http://127.0.0.1:5000/sales/<sale_id>`

**Body**

```json
{
  "quantity": 130,
  "unit_price": 160,
  "date": "2024-01-22"
}
```

---

## **🔹 Delete Sale**

**DELETE**
`http://127.0.0.1:5000/sales/<sale_id>`

---

# **5️⃣ Summary / Analytics Routes**

Prefix: **`/summary`**

---

## **🔹 Get Farm Summary**

**GET** `http://127.0.0.1:5000/summary/<farm_id>`

Returns aggregated data:

* total livestock count
* total expenses
* total sales revenue
* profit/loss
* livestock breakdown
* monthly expense/sales chart

Sample Response:

```json
{
  "farm_id": 1,
  "total_livestock": 25,
  "total_expenses": 120000,
  "total_sales": 180000,
  "profit": 60000
}
```

---

# ** Error Responses**

| Code    | Meaning                                        |
| ------- | ---------------------------------------------- |
| **400** | Bad Request / Missing fields                   |
| **401** | Unauthorized (invalid credentials or no token) |
| **403** | Forbidden (admin-only routes)                  |
| **404** | Record not found                               |
| **409** | Conflict (duplicate email on signup)           |

---

# **✔️ Endpoints Overview (Quick Copy Table)**

| Category  | Method | Endpoint                    |
| --------- | ------ | --------------------------- |
| Auth      | POST   | `/auth/signup`              |
| Auth      | POST   | `/auth/login`               |
| Auth      | GET    | `/auth/test`                |
| Livestock | POST   | `/livestock/`               |
| Livestock | GET    | `/livestock/<farm_id>`      |
| Livestock | PUT    | `/livestock/<livestock_id>` |
| Livestock | DELETE | `/livestock/<livestock_id>` |
| Expenses  | POST   | `/expenses/`                |
| Expenses  | GET    | `/expenses/<farm_id>`       |
| Expenses  | PUT    | `/expenses/<expense_id>`    |
| Expenses  | DELETE | `/expenses/<expense_id>`    |
| Sales     | POST   | `/sales/`                   |
| Sales     | GET    | `/sales/<farm_id>`          |
| Sales     | PUT    | `/sales/<sale_id>`          |
| Sales     | DELETE | `/sales/<sale_id>`          |
| Summary   | GET    | `/summary/<farm_id>`        |

---


