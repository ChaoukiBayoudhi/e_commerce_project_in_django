# E commerce project in Django

A Django project with 6 models and a REST API (Django REST Framework).

## Tech stack

- Python 3
- Django
- Django REST Framework
- Database: PostgreSQL

## Project structure

- `e_commerce_project/`: project settings and root URLs
- `e_commerce_app/`: Django app
- Tests: `e_commerce_app/tests.py`

## Data model

| Model | App | Fields |
|---|---|---|
| `Address` | `e_commerce_app` | houseNumber, street, city, country, postalCode |
| `User` | `e_commerce_app` | name, password, email, phone, address |
| `Provider` | `e_commerce_app` | site_url |
| `Product` | `e_commerce_app` | label, price, stock, image, description, expirationDate, fabricationDate, provider |
| `Client` | `e_commerce_app` | familyName, typeClient, client_products |
| `Command` | `e_commerce_app` | client, product, date_cmd, quantity, amount |

## URL routes

Declared in `urls.py`:

- `/max_min_price/`
- `/<int:pk>/client_products/`
- `/client_products`
- `/not_satisfied/`
- `/products/ (router)`
- `/clients/ (router)`
- `/addresses/ (router)`
- `/providers/ (router)`
- `/commands/ (router)`
- `/blog/`
- `/ecommerce/`

## How to run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install django djangorestframework psycopg2-binary
python manage.py migrate
python manage.py runserver
```

There is no `requirements.txt`; the packages above are the ones the settings and imports refer to.

`settings.py` is configured for PostgreSQL: create the database and use your own credentials before running `migrate`.

Then open `http://127.0.0.1:8000/`.

---

Author: [Chaouki Bayoudhi](https://github.com/ChaoukiBayoudhi)
