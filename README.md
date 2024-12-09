# Warehouse Management System - Flask Application

This repository contains a Flask-based Warehouse Management System that handles various operations such as inventory management, inbound and outbound shipments, and user authentication with role-based access control. The application uses PostgreSQL as the database backend, with SQLAlchemy for ORM (Object-Relational Mapping).

## Prerequisites

Before running the application, ensure you have the following installed on your system:

- **Python 3.7+**
- **PostgreSQL 12+** or any version compatible with SQLAlchemy
- **pip** (Python package manager)
- **Flask** and other required Python packages

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/NafeesSadat/Inventory-Management.git
cd Inventory-Management
```

### 2. Set up a virtual environment (recommended)

Activate a virtual environment by running the following commands:

#### On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

Once the virtual environment is activated, install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL Database

#### Database Configuration:

You need to have PostgreSQL running on your local machine or use a remote PostgreSQL server. Create a new database for the application: `warehouse_db`.

1. **Create the database**:
   Log into PostgreSQL and run the following command to create the database:

   ```sql
   CREATE DATABASE warehouse_db;
   ```

2. **Update the Database URL in the config file**:
   Open the `config.py` file in your project and update the database URI to match your PostgreSQL credentials:

   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@localhost/warehouse_db'
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   ```

   Replace `<username>` and `<password>` with your actual PostgreSQL username and password.

#### Table Creation:

When running the application for the first time, the tables should be automatically created. If there’s an error or the tables are not created, you can manually create them by running the following SQL script in your PostgreSQL database:

```sql
CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(200)
);

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    supplier VARCHAR(100) NOT NULL
);

CREATE TABLE inbound (
    id SERIAL PRIMARY KEY,
    reference VARCHAR(50) NOT NULL,
    date_received DATE NOT NULL,
    product_sku VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    location VARCHAR(100) NOT NULL,
    remarks VARCHAR(200),
    FOREIGN KEY (product_sku) REFERENCES inventory(sku)
);

CREATE TABLE outbound (
    id SERIAL PRIMARY KEY,
    reference VARCHAR(50) NOT NULL,
    date_shipped DATE NOT NULL,
    product_sku VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    destination VARCHAR(100) NOT NULL,
    remarks VARCHAR(200),
    FOREIGN KEY (product_sku) REFERENCES inventory(sku)
);
```

### 5. Run the Flask Application

To start the Flask application, simply run:

```bash
python run.py
```

The application will be hosted locally, and you can access it in your web browser at:

```
http://127.0.0.1:5000/
```

## Application Features

1. **Inventory Management**:
   - Add, update, and search inventory items.
   - Inventory records include product category, SKU, name, location, quantity, and supplier.

2. **Inbound Shipments**:
   - Add new inbound shipments.
   - Track received products, including SKU, quantity, location, and remarks.
   - Automatically update the inventory when items are received.

3. **Outbound Shipments**:
   - Add new outbound shipments.
   - Track shipped products, including SKU, quantity, destination, and remarks.
   - Automatically update the inventory when items are shipped.

4. **User Authentication and Role-based Access**:
   - Users can register and log in with their credentials.
   - Roles such as `manager` and `operator` control access to different parts of the application.
   - The manager role has access to inventory management, while the operator role has access to inbound and outbound shipment management.

## Running the Application

1. **User Login**:
   - Navigate to `/login` and enter the username and password. The application uses hashed passwords for security.

2. **Inventory Actions**:
   - You can view and search inventory items under the `/inventory` route.
   - Managers can add or update inventory items.

3. **Inbound and Outbound Shipments**:
   - Operators can manage inbound and outbound shipments via the `/inbound` and `/outbound` routes.
   - Both routes allow users to add records and automatically update inventory levels.

## Troubleshooting

- **Error Creating Tables**: If the tables are not created automatically, you can create them manually using the provided SQL script.
- **Database Connection Issues**: Ensure that your PostgreSQL server is running and the credentials in the `config.py` file are correct.
- **Missing Dependencies**: If you encounter missing dependencies, make sure you have installed all required Python packages by running `pip install -r requirements.txt`.

---
