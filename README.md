# 🍽️ Homely Kitchen

A **multi-role food ordering platform** that connects home cooks with local food lovers. Homemakers can list their homemade dishes, consumers can discover and order food, and delivery personnel can manage deliveries - all in one place.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [Database Schema](#-database-schema)
- [API Routes](#-api-routes)


## ✨ Features

### 👤 For Consumers (Food Lovers)
- **Browse Food Items**: View all available homemade dishes with images, prices, and ratings
- **Search Functionality**: Find specific food items by name
- **Food Details**: View detailed information about each dish including description, location, and homemaker details
- **Place Orders**: Order food with quantity selection and automatic price calculation
- **User Profile**: Manage personal information and update passwords securely
- **Simple Authentication**: Easy signup and login process with email verification

### 👩‍🍳 For Homemakers (Cooks)
- **Dashboard**: Centralized view of all your listed food items and incoming orders
- **Complete CRUD Operations**:
  - **Add** new food items with details (name, location, price, rating, description, image filename)
  - **Edit** existing food items with pre-populated forms
  - **Delete** food items with confirmation prompt
- **Order Management**: View all orders placed for your food items with consumer details
- **Profile Management**: Update personal information and change password

### 🚚 For Delivery Personnel
- **Order Overview**: View all orders in the system sorted by timestamp
- **Status Updates**: Mark orders as "Pending" or "Completed" with one-click buttons
- **Comprehensive View**: See order details including food item, consumer, homemaker, quantity, and total price

### 🔧 General Features
- **Role-based Access Control**: Separate login systems and dashboards for different user types
- **Secure Authentication**: Password hashing with Werkzeug security
- **Session Management**: Persistent login sessions with flash messages
- **Database Persistence**: SQLite with SQLAlchemy ORM and relationship mapping
- **Responsive Design**: Bootstrap 5 for mobile-friendly, modern interface
- **Error Handling**: Proper flash messages for user feedback

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.x** | Core programming language |
| **Flask** | Web framework for routing and rendering |
| **Flask-SQLAlchemy** | ORM for database operations |
| **SQLite** | Lightweight database for development |
| **Werkzeug** | Password hashing and security |
| **Bootstrap 5** | Frontend styling and responsive design |
| **HTML5/CSS3** | Template structure and custom styling |
| **Jinja2** | Template engine for dynamic content |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager, comes with Python)
- **Git** ([Download](https://git-scm.com/downloads))
- **Virtual environment** (recommended for dependency isolation)

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/Shampath1102/HomelyKitchen.git
cd HomelyKitchen
```
### Step 2: Create and Activate Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Step 4: Initialize the Database

#### Option A: Create Empty Database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

#### Option B: Seed with Sample Data
```bash
python seed.py
# OR
python seed1.py
```

---

### Step 5: Run the Application
```bash
python app.py
```

---

### Step 6: Access the Application

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

# 📁 Project Structure

```
HomelyKitchen/
│
├── app.py                      # Main application with all routes and models
├── requirements.txt            # Python dependencies
├── seed.py                     # Database seeder with sample data
├── seed1.py                    # Additional sample data seeder
│
├── instance/                   # Database files (created on first run)
│   └── homely_kitchen.db       # SQLite database
│
├── static/
│   └── images/                 # Food item images and icons
│       ├── spaghetti.jpg
│       ├── chicken_curry.jpg
│       ├── buddha_bowl.jpg
│       ├── cheeseburger.jpg
│       ├── profile-icon.jpg
│       ├── consumer-icon.jpg
│       └── homemaker-icon.jpg
│
└── templates/                  # HTML templates
    ├── index.html
    │
    ├── consumer_login.html
    ├── consumer_signup.html
    ├── consumer_home.html
    ├── food_detail.html
    │
    ├── homemaker_login.html
    ├── homemaker_signup.html
    ├── homemaker_dashboard.html
    ├── add_food_item.html
    ├── edit_food_item.html
    │
    ├── delivery_orders.html
    └── profile.html
```

---

# 💡 Usage Guide

## 👤 As a Consumer

### Registration / Login
- Navigate to home page  
- Click **"Sign Up as Consumer"**  
- Fill in name, email, password, city, address  
- Login with credentials  

### Browse Food Items
- View all food items on dashboard  
- Each card shows image, name, location, price, rating  

### Search Food
- Use search bar  
- Results update in real-time  

### View Food Details
- Click any food card  
- View description and full image  

### Place an Order
- Select quantity (minimum 1)  
- Click **"Place Order"**  
- Receive confirmation message  

### Manage Profile
- Click profile icon  
- Update details  
- Change password (optional)  

---

## 👩‍🍳 As a Homemaker

### Registration / Login
- Click **"Sign Up as Homemaker"**  
- Enter cooking location  
- Login to access dashboard  

### Dashboard Overview
- View listed food items  
- See incoming orders  
- Add/Edit/Delete items  

### Add Food Items
- Click **"Add New Item"**  
- Enter name, location, price, rating, description  
- Provide image filename (must exist in `static/images/`)  

### Manage Items
- Edit existing items  
- Delete items (confirmation required)  

### View Orders
- Scroll to orders section  
- View consumer details and quantity  

---

## 🚚 As Delivery Personnel

### Access Orders
- Navigate to delivery orders section  
- View all orders sorted by timestamp  

### Update Order Status
- Click **"Mark as Completed"**  
- Click **"Mark as Pending"**  
- Status updates instantly  

---

# 📊 Database Schema

## User Model
```python
{
    "id": Integer (Primary Key),
    "first_name": String(150),
    "last_name": String(150),
    "email": String(150) (Unique),
    "password": String(256) (Hashed),
    "city": String(100),
    "address": String(300),
    "is_homemaker": Boolean
}
```

## FoodItem Model
```python
{
    "id": Integer (Primary Key),
    "name": String(150),
    "location": String(100),
    "price": Float,
    "rating": Float,
    "description": Text,
    "image": String(150),
    "homemaker_id": Integer (Foreign Key to User)
}
```

## Order Model
```python
{
    "id": Integer (Primary Key),
    "consumer_id": Integer (Foreign Key to User),
    "food_item_id": Integer (Foreign Key to FoodItem),
    "quantity": Integer,
    "total_price": Float,
    "status": String(50) (Default: "Pending"),
    "timestamp": DateTime (Auto-generated)
}
```

---

# 🛣️ API Routes

| Route | Methods | Description | Access |
|-------|---------|------------|--------|
| `/` | GET | Landing page | Public |
| `/consumer_signup` | GET, POST | Consumer registration | Public |
| `/consumer_login` | GET, POST | Consumer login | Public |
| `/homemaker_signup` | GET, POST | Homemaker registration | Public |
| `/homemaker_login` | GET, POST | Homemaker login | Public |
| `/consumer_home` | GET | Consumer dashboard | Consumer only |
| `/food_detail/<id>` | GET | Food item details | Consumer only |
| `/order_food/<id>` | POST | Place food order | Consumer only |
| `/search_food` | GET | Search food items | Consumer only |
| `/homemaker_dashboard` | GET | Homemaker dashboard | Homemaker only |
| `/add_food_item` | GET, POST | Add new food item | Homemaker only |
| `/edit_food_item/<id>` | GET, POST | Edit food item | Homemaker only |
| `/delete_food_item/<id>` | POST | Delete food item | Homemaker only |
| `/delivery_orders` | GET | View all orders | Delivery only |
| `/update_order_status/<id>` | POST | Update order status | Delivery only |
| `/profile` | GET, POST | View/edit profile | Authenticated |
| `/logout` | GET | Logout user | Authenticated |

---



