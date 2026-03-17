# Housing API

A RESTful API for UK housing market and rental data, built with Django and Django REST Framework as part of COMP3011 Web Services and Web Data at the University of Leeds.

The API allows users to browse, filter, and analyse rental listings across major UK cities. It includes JWT-based authentication, full CRUD functionality, and three analytics endpoints that compute average rent, affordability indices, and market summaries.

## Live Deployment

The API is live at: https://nadia8844.pythonanywhere.com

## Tech Stack

- Python 3.12
- Django 6.0.3
- Django REST Framework 3.16.1
- SQLite (development and production)
- JWT Authentication via djangorestframework-simplejwt

## Getting Started

Clone the repository and navigate into the project folder:
```bash
git clone https://github.com/Nadia8844/housing-api.git
cd housing-api
```

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run database migrations:
```bash
python3 manage.py migrate
```

Seed the database with sample UK housing data:
```bash
python3 manage.py seed_data
```

Start the development server:
```bash
python3 manage.py runserver
```

The API will be available at http://127.0.0.1:8000

## API Endpoints

### Listings

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/listings/ | Returns all listings | No |
| POST | /api/listings/ | Creates a new listing | Yes |
| GET | /api/listings/{id}/ | Returns a single listing | No |
| PUT | /api/listings/{id}/ | Updates a listing | Yes |
| DELETE | /api/listings/{id}/ | Deletes a listing | Yes |

Listings can be filtered using query parameters:
```
/api/listings/?city=Leeds
/api/listings/?bedrooms=2
/api/listings/?property_type=flat
/api/listings/?available=true
```

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/analytics/average-rent/ | Average rent per city |
| GET | /api/analytics/affordability/ | Affordability index per city |
| GET | /api/analytics/summary/ | Overall market summary |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register/ | Register a new user |
| POST | /api/token/ | Obtain a JWT token |
| POST | /api/token/refresh/ | Refresh an expired token |

## Authentication

To access protected endpoints, first obtain a token:
```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

Then include the access token in your request headers:
```
Authorization: Bearer <your_access_token>
```

## API Documentation

Full API documentation is available as a PDF in this repository:
[View API Documentation](docs/api_documentation.pdf)

## Running Tests
```bash
python3 manage.py test listings
```