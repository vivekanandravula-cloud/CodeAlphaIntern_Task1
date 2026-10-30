# CodeAlpha Internship — Task 1: Simple E-commerce Store

A beginner-friendly Django e-commerce project with HTML, CSS, JavaScript, SQLite, authentication, product details, session cart, and order processing.

## Requirements
- Python 3.10+
- pip

## Run on macOS / Linux
```bash
cd CodeAlpha_Task1_Ecommerce
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Run on Windows
```powershell
cd CodeAlpha_Task1_Ecommerce
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Features
- Product listing and product detail pages
- Add to cart, update quantity, and remove items
- Registration, login, and logout using Django authentication
- Checkout and order creation
- SQLite database for products, users, orders, and order items
- Responsive layout and client-side quantity controls

## Notes
- The checkout is a demo order flow; it does not take real payments.
- Run `python manage.py seed_products` to add sample products.
- To create an admin account, run `python manage.py createsuperuser`, then visit `/admin/`.
