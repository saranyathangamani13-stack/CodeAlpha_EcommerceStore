# CodeAlpha E-commerce Store

A clean and simplified e-commerce web application developed using Django as part of the CodeAlpha Full Stack Development Internship.

## Project Overview

This project demonstrates the core workflow of an online shopping application.

Users can:

- Browse products
- Search and filter products
- View product details
- Register and log in
- Add products to a shopping cart
- Update or remove cart items
- Proceed to checkout
- Place orders
- View order history and order details

The application also includes basic product stock management and Django admin management.

> Note: This project uses a demo checkout flow. A real payment gateway has not been integrated.

## CodeAlpha Task

**Task 1 - Simple E-commerce Store**

The project covers the main requirements of the CodeAlpha Full Stack Development internship:

- Product listings
- Product details page
- Shopping cart
- Order processing
- User registration and login
- Database storage for products, users, and orders

## Features

### User Authentication
- User registration
- User login
- User logout
- Login-protected checkout and order features

### Product Management
- Product listing
- Product details
- Category filtering
- Product search
- Product stock information

### Shopping Cart
- Add products to cart
- Update product quantity
- Remove products from cart
- View cart subtotal and total
- Empty cart handling
- Stock validation

### Checkout and Orders
- Checkout page
- Shipping information
- Order creation
- Automatic stock reduction after successful order
- Order history
- Order details

### Admin Management
Django Admin can be used to manage the application's products and orders.

### Responsive Design
The storefront interface is designed to work across:

- Desktop
- Tablet
- Mobile

## Technologies Used

### Frontend
- HTML5
- CSS3
- Responsive CSS design

### Backend
- Python
- Django

### Database
- SQLite

### Development Tools
- Visual Studio Code
- Git
- GitHub

## Project Structure

```text
CodeAlpha_EcommerceStore/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── store/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_seed_products.py
│   │   └── __init__.py
│   │
│   ├── static/
│   │   └── store/
│   │       └── store.css
│   │
│   ├── templates/
│   │   └── store/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── product_detail.html
│   │       ├── cart.html
│   │       ├── checkout.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── orders.html
│   │       └── order_detail.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md