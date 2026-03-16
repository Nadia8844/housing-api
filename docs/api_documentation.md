# Housing API — Documentation

**Base URL (Local):** http://127.0.0.1:8000  
**Base URL (Live):** https://nadia8844.pythonanywhere.com  
**Version:** 1.0  
**Author:** Nadia  
**Module:** COMP3011 Web Services and Web Data, University of Leeds  

---

## Table of Contents

1. Introduction
2. Architecture
3. Authentication and Security
4. Common Workflows
5. API Reference — Listings
6. API Reference — Regions
7. API Reference — Analytics
8. API Reference — Authentication
9. MCP Server Integration
10. Error Reference

---

## 1. Introduction

### 1.1 What This API Provides

The Housing API is a RESTful web service for UK rental market data. It 
allows clients to browse, filter, and analyse rental property listings 
across major UK cities, and provides regional economic data sourced from 
ONS statistics.

The API is designed for use by property platforms, housing researchers, 
or any application that needs to query and analyse UK rental market data 
programmatically.

### 1.2 Design Principles

The API is designed according to REST architectural principles as defined 
by Fielding (2000):

- **Statelessness** — every request contains all information needed to 
  process it. No session state is stored server-side.
- **Resource-based design** — endpoints are named using nouns, not verbs.
- **Uniform interface** — HTTP methods (GET, POST, PUT, DELETE) indicate 
  the type of operation.
- **JSON responses** — all responses are returned in JSON format with 
  appropriate HTTP status codes.

### 1.3 Quick Start

#### Run the API Locally
```bash
git clone https://github.com/Nadia8844/housing-api.git
cd housing-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_data
python3 manage.py runserver
```

The API will be available at http://127.0.0.1:8000

#### Explore the Live API

The API is deployed at https://nadia8844.pythonanywhere.com

Try this endpoint to verify it is running:
```
GET https://nadia8844.pythonanywhere.com/api/listings/
```

### 1.4 Conventions

#### Dates

All timestamps are returned in ISO 8601 format in UTC:
```
2026-03-17T13:05:05.226110Z
```

#### Authentication Header

Protected endpoints require a Bearer token in the request header:
```
Authorization: Bearer <your_access_token>
```

#### Error Format

All error responses follow this structure:
```json
{
    "error": "A human-readable description of the error"
}
```

#### Versioning

The current version is v1.0. The version is not included in the URL path. 
Future versions would be distinguished by an `/api/v2/` prefix.

---

## 2. Architecture

### 2.1 High-Level Request Flow
```
Client Request
      │
      ▼
Django URL Router  ←── housing_api/urls.py
      │
      ▼
JWT Middleware  ←── Validates Bearer token if present
      │
      ▼
API View  ←── listings/views.py
      │
      ├── Serialiser  ←── listings/serializers.py
      │       │
      │       ▼
      └── Django ORM  ←── listings/models.py
              │
              ▼
         SQLite Database  ←── db.sqlite3
              │
              ▼
         JSON Response  ←── Returned to client
```

### 2.2 Data Models

#### Listing

Represents a rental property listing.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Auto-generated primary key |
| title | CharField (200) | Name of the listing |
| address | CharField (300) | Street address |
| city | CharField (100) | City name |
| postcode | CharField (10) | UK postcode |
| property_type | CharField (50) | flat, house, or studio |
| bedrooms | IntegerField | Number of bedrooms |
| monthly_rent | DecimalField | Monthly rent in GBP |
| available | BooleanField | Whether the property is available |
| created_at | DateTimeField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated on save |

#### Region

Represents a UK region with ONS economic data.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Auto-generated primary key |
| name | CharField (100) | Region name (unique) |
| average_annual_salary | DecimalField | ONS average annual salary in GBP |
| median_monthly_rent | DecimalField | ONS median monthly rent in GBP |
| population | IntegerField | Regional population |
| country | CharField (50) | England, Scotland, Wales, or N. Ireland |

---

## 3. Authentication and Security

### 3.1 JWT Bearer Authentication

The API uses JSON Web Tokens (JWT) for authentication, implemented 
via the djangorestframework-simplejwt library.

**Token lifetimes:**
- Access token: 5 minutes
- Refresh token: 24 hours

**Authentication flow:**
```
1. Register   →  POST /api/register/
2. Login      →  POST /api/token/          (returns access + refresh tokens)
3. Use API    →  Include access token in Authorization header
4. Refresh    →  POST /api/token/refresh/  (when access token expires)
```

### 3.2 Endpoint Protection

| Access Level | Endpoints |
|---|---|
| Public (no auth) | GET /api/listings/, GET /api/listings/{id}/, all analytics, all regions GET |
| Authenticated | POST, PUT, DELETE on listings and regions |
| No auth required | /api/register/, /api/token/, /api/token/refresh/ |

---

## 4. Common Workflows

### Workflow 1 — Browse Listings Without an Account

No authentication is required to read listings or analytics.
```bash
# Get all listings
curl https://nadia8844.pythonanywhere.com/api/listings/

# Filter by city
curl https://nadia8844.pythonanywhere.com/api/listings/?city=Leeds

# Filter by bedrooms
curl https://nadia8844.pythonanywhere.com/api/listings/?bedrooms=2

# Filter by property type
curl https://nadia8844.pythonanywhere.com/api/listings/?property_type=flat

# Get market summary
curl https://nadia8844.pythonanywhere.com/api/analytics/summary/
```

### Workflow 2 — Register, Login, and Create a Listing
```bash
# Step 1: Register a new account
curl -X POST https://nadia8844.pythonanywhere.com/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepassword123"}'

# Step 2: Login to obtain a JWT token
curl -X POST https://nadia8844.pythonanywhere.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepassword123"}'

# Response contains:
# {
#   "access": "eyJhbGci...",
#   "refresh": "eyJhbGci..."
# }

# Step 3: Use the access token to create a listing
curl -X POST https://nadia8844.pythonanywhere.com/api/listings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGci..." \
  -d '{
    "title": "2-Bed Flat in Leeds",
    "address": "10 Briggate",
    "city": "Leeds",
    "postcode": "LS1 6HD",
    "property_type": "flat",
    "bedrooms": 2,
    "monthly_rent": 950.00,
    "available": true
  }'
```

### Workflow 3 — Analyse the Market
```bash
# Average rent per city
curl https://nadia8844.pythonanywhere.com/api/analytics/average-rent/

# Affordability index per city
curl https://nadia8844.pythonanywhere.com/api/analytics/affordability/

# Overall market summary
curl https://nadia8844.pythonanywhere.com/api/analytics/summary/

# Regional ONS data
curl https://nadia8844.pythonanywhere.com/api/regions/
```

### Workflow 4 — Update and Delete a Listing
```bash
# Update a listing (authentication required)
curl -X PUT https://nadia8844.pythonanywhere.com/api/listings/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGci..." \
  -d '{
    "title": "Updated Studio in Leeds",
    "address": "12 Park Row",
    "city": "Leeds",
    "postcode": "LS1 5HD",
    "property_type": "studio",
    "bedrooms": 0,
    "monthly_rent": 800.00,
    "available": true
  }'

# Delete a listing (authentication required)
curl -X DELETE https://nadia8844.pythonanywhere.com/api/listings/1/ \
  -H "Authorization: Bearer eyJhbGci..."
```

---

## 5. API Reference — Listings

### GET /api/listings/

Returns all property listings. Supports optional query parameters for filtering.

**Authentication:** Not required

**Query Parameters:**

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| city | string | No | Filter by city name (case-insensitive) | ?city=Leeds |
| bedrooms | integer | No | Filter by number of bedrooms | ?bedrooms=2 |
| property_type | string | No | Filter by property type | ?property_type=flat |
| available | boolean | No | Filter by availability | ?available=true |

**Success Response — 200 OK:**
```json
[
    {
        "id": 1,
        "title": "Modern Studio in Central Leeds",
        "address": "12 Park Row",
        "city": "Leeds",
        "postcode": "LS1 5HD",
        "property_type": "studio",
        "bedrooms": 0,
        "monthly_rent": "750.00",
        "available": true,
        "created_at": "2026-03-17T13:05:05.226110Z",
        "updated_at": "2026-03-17T13:05:05.226152Z"
    }
]
```

---

### POST /api/listings/

Creates a new property listing.

**Authentication:** Required

**Request Body:**
```json
{
    "title": "2-Bed Flat in Leeds",
    "address": "10 Briggate",
    "city": "Leeds",
    "postcode": "LS1 6HD",
    "property_type": "flat",
    "bedrooms": 2,
    "monthly_rent": 950.00,
    "available": true
}
```

**Success Response — 201 Created:**
```json
{
    "id": 9,
    "title": "2-Bed Flat in Leeds",
    "address": "10 Briggate",
    "city": "Leeds",
    "postcode": "LS1 6HD",
    "property_type": "flat",
    "bedrooms": 2,
    "monthly_rent": "950.00",
    "available": true,
    "created_at": "2026-03-18T10:00:00.000000Z",
    "updated_at": "2026-03-18T10:00:00.000000Z"
}
```

**Error Responses:**

| Status | Reason |
|--------|--------|
| 400 Bad Request | Missing or invalid fields |
| 401 Unauthorised | No valid token provided |

---

### GET /api/listings/{id}/

Returns a single property listing by its ID.

**Authentication:** Not required

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | The ID of the listing |

**Success Response — 200 OK:**
```json
{
    "id": 1,
    "title": "Modern Studio in Central Leeds",
    "address": "12 Park Row",
    "city": "Leeds",
    "postcode": "LS1 5HD",
    "property_type": "studio",
    "bedrooms": 0,
    "monthly_rent": "750.00",
    "available": true,
    "created_at": "2026-03-17T13:05:05.226110Z",
    "updated_at": "2026-03-17T13:05:05.226152Z"
}
```

**Error Response — 404 Not Found:**
```json
{
    "error": "Listing not found"
}
```

---

### PUT /api/listings/{id}/

Updates an existing property listing. All fields must be provided.

**Authentication:** Required

**Request Body:** Same fields as POST /api/listings/

**Success Response — 200 OK:** Returns the updated listing object.

**Error Responses:**

| Status | Reason |
|--------|--------|
| 400 Bad Request | Missing or invalid fields |
| 401 Unauthorised | No valid token provided |
| 404 Not Found | Listing does not exist |

---

### DELETE /api/listings/{id}/

Permanently deletes a property listing.

**Authentication:** Required

**Success Response — 204 No Content:**
```json
{
    "message": "Listing successfully deleted"
}
```

**Error Responses:**

| Status | Reason |
|--------|--------|
| 401 Unauthorised | No valid token provided |
| 404 Not Found | Listing does not exist |

---

## 6. API Reference — Regions

### GET /api/regions/

Returns all UK regions with ONS salary and rental data.

**Authentication:** Not required

**Success Response — 200 OK:**
```json
[
    {
        "id": 1,
        "name": "London",
        "average_annual_salary": "44850.00",
        "median_monthly_rent": "2000.00",
        "population": 8799800,
        "country": "England"
    },
    {
        "id": 3,
        "name": "Yorkshire and The Humber",
        "average_annual_salary": "29500.00",
        "median_monthly_rent": "800.00",
        "population": 5502967,
        "country": "England"
    }
]
```

---

### POST /api/regions/

Creates a new region entry.

**Authentication:** Required

**Request Body:**
```json
{
    "name": "East Midlands",
    "average_annual_salary": 28500.00,
    "median_monthly_rent": 750.00,
    "population": 4934939,
    "country": "England"
}
```

**Success Response — 201 Created:** Returns the created region object.

---

### GET /api/regions/{id}/

Returns a single region by its ID.

**Authentication:** Not required

**Success Response — 200 OK:** Returns the region object.

**Error Response — 404 Not Found:**
```json
{
    "error": "Region not found"
}
```

---

### PUT /api/regions/{id}/

Updates an existing region. All fields must be provided.

**Authentication:** Required

**Success Response — 200 OK:** Returns the updated region object.

---

### DELETE /api/regions/{id}/

Permanently deletes a region.

**Authentication:** Required

**Success Response — 204 No Content:**
```json
{
    "message": "Region successfully deleted"
}
```

---

## 7. API Reference — Analytics

### GET /api/analytics/average-rent/

Returns average, minimum, and maximum monthly rent grouped by city.
Results are ordered alphabetically by city.

**Authentication:** Not required

**Success Response — 200 OK:**
```json
[
    {
        "city": "Birmingham",
        "average_rent": 1100.0,
        "total_listings": 1,
        "min_rent": 1100.0,
        "max_rent": 1100.0
    },
    {
        "city": "Leeds",
        "average_rent": 700.0,
        "total_listings": 2,
        "min_rent": 650.0,
        "max_rent": 750.0
    },
    {
        "city": "London",
        "average_rent": 2200.0,
        "total_listings": 1,
        "min_rent": 2200.0,
        "max_rent": 2200.0
    }
]
```

---

### GET /api/analytics/affordability/

Returns an affordability index per city. The index is calculated as:
```
affordability_index = (average_monthly_rent / UK_median_monthly_salary) × 100
```

The UK median monthly salary used is £2,500, based on ONS ASHE 2023 data.

**Authentication:** Not required

**Affordability Ratings:**

| Rating | Condition |
|--------|-----------|
| affordable | Index below 30% |
| moderate | Index between 30% and 40% |
| expensive | Index above 40% |

**Success Response — 200 OK:**
```json
[
    {
        "city": "Leeds",
        "average_rent": 700.0,
        "affordability_index": 28.0,
        "affordability_rating": "affordable"
    },
    {
        "city": "London",
        "average_rent": 2200.0,
        "affordability_index": 88.0,
        "affordability_rating": "expensive"
    }
]
```

---

### GET /api/analytics/summary/

Returns an overall snapshot of the housing market dataset.

**Authentication:** Not required

**Success Response — 200 OK:**
```json
{
    "total_listings": 8,
    "available_listings": 7,
    "unavailable_listings": 1,
    "overall_average_rent": 1156.25,
    "cities_covered": 7
}
```

---

## 8. API Reference — Authentication

### POST /api/register/

Creates a new user account.

**Authentication:** Not required

**Request Body:**
```json
{
    "username": "testuser",
    "password": "securepassword123"
}
```

**Success Response — 201 Created:**
```json
{
    "message": "User 'testuser' registered successfully"
}
```

**Error Responses:**

| Status | Reason |
|--------|--------|
| 400 Bad Request | Username already exists or missing fields |

---

### POST /api/token/

Authenticates a user and returns a JWT access and refresh token pair.

**Authentication:** Not required

**Request Body:**
```json
{
    "username": "testuser",
    "password": "securepassword123"
}
```

**Success Response — 200 OK:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response — 401 Unauthorised:**
```json
{
    "detail": "No active account found with the given credentials"
}
```

---

### POST /api/token/refresh/

Returns a new access token using a valid refresh token.
Use this when the access token has expired.

**Authentication:** Not required

**Request Body:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response — 200 OK:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 9. MCP Server Integration

The API includes an MCP (Model Context Protocol) server that exposes 
the housing data as tools for AI assistants such as Claude Desktop.

### Available Tools

| Tool | Description |
|------|-------------|
| get_all_listings | Returns listings with optional city, bedrooms, and property_type filters |
| get_market_summary | Returns overall market statistics |
| get_average_rent_by_city | Returns average, min, and max rent per city |
| get_affordability_index | Returns affordability ratings per city |
| get_all_regions | Returns all UK regions with ONS data |
| get_region | Returns a single region by name |

### Setup for Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
```json
{
    "mcpServers": {
        "housing-api": {
            "command": "/path/to/venv/bin/python3",
            "args": ["/path/to/housing-api/mcp_server.py"]
        }
    }
}
```

Once connected, you can ask Claude things like:
- "Which UK city is most affordable for renters?"
- "Show me all available flats with 2 bedrooms"
- "What is the average rent in London compared to Leeds?"

---

## 10. Error Reference

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Missing or invalid fields in request body |
| 401 | Unauthorised | Missing, expired, or invalid JWT token |
| 404 | Not Found | Resource with given ID does not exist |
| 405 | Method Not Allowed | HTTP method not supported on this endpoint |