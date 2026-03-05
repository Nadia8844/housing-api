# Housing API — Documentation

**Base URL (Local):** http://127.0.0.1:8000  
**Base URL (Live):** https://nadia8844.pythonanywhere.com  
**Version:** 1.0  
**Format:** All responses are returned in JSON

---

## Authentication

This API uses JSON Web Tokens (JWT) for authentication. Certain endpoints require a valid token to be included in the request header.

To authenticate, include the following header in your request:
```
Authorization: Bearer <your_access_token>
```

---

## Endpoints

### 1. Register a New User

**POST** `/api/register/`

Creates a new user account.

**Request Body:**
```json
{
    "username": "testuser",
    "password": "securepassword"
}
```

**Success Response — 201 Created:**
```json
{
    "message": "User 'testuser' registered successfully"
}
```

**Error Response — 400 Bad Request:**
```json
{
    "error": "Username already exists"
}
```

---

### 2. Obtain JWT Token (Login)

**POST** `/api/token/`

Returns an access token and refresh token for a valid user.

**Request Body:**
```json
{
    "username": "testuser",
    "password": "securepassword"
}
```

**Success Response — 200 OK:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response — 401 Unauthorized:**
```json
{
    "detail": "No active account found with the given credentials"
}
```

---

### 3. Refresh JWT Token

**POST** `/api/token/refresh/`

Returns a new access token using a valid refresh token.

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

### 4. Get All Listings

**GET** `/api/listings/`

Returns all property listings. Supports optional query parameters for filtering.

**Authentication:** Not required

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| city | string | Filter by city name | ?city=Leeds |
| bedrooms | integer | Filter by number of bedrooms | ?bedrooms=2 |
| property_type | string | Filter by property type | ?property_type=flat |
| available | boolean | Filter by availability | ?available=true |

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

### 5. Create a Listing

**POST** `/api/listings/`

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
    "created_at": "2026-03-17T20:00:00.000000Z",
    "updated_at": "2026-03-17T20:00:00.000000Z"
}
```

**Error Response — 400 Bad Request:**
```json
{
    "monthly_rent": ["This field is required."]
}
```

---

### 6. Get a Single Listing

**GET** `/api/listings/{id}/`

Returns a single property listing by ID.

**Authentication:** Not required

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

### 7. Update a Listing

**PUT** `/api/listings/{id}/`

Updates an existing property listing.

**Authentication:** Required

**Request Body:**
```json
{
    "title": "Modern Studio in Central Leeds",
    "address": "12 Park Row",
    "city": "Leeds",
    "postcode": "LS1 5HD",
    "property_type": "studio",
    "bedrooms": 0,
    "monthly_rent": 800.00,
    "available": true
}
```

**Success Response — 200 OK:**
```json
{
    "id": 1,
    "title": "Modern Studio in Central Leeds",
    "monthly_rent": "800.00",
    "available": true
}
```

**Error Response — 404 Not Found:**
```json
{
    "error": "Listing not found"
}
```

---

### 8. Delete a Listing

**DELETE** `/api/listings/{id}/`

Deletes a property listing.

**Authentication:** Required

**Success Response — 204 No Content:**
```json
{
    "message": "Listing successfully deleted"
}
```

**Error Response — 404 Not Found:**
```json
{
    "error": "Listing not found"
}
```

---

### 9. Average Rent by City

**GET** `/api/analytics/average-rent/`

Returns average, minimum, and maximum monthly rent per city.

**Authentication:** Not required

**Success Response — 200 OK:**
```json
[
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

### 10. Affordability Index

**GET** `/api/analytics/affordability/`

Returns an affordability index per city, calculated as average rent as a percentage of the UK median monthly salary (£2,500).

**Authentication:** Not required

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

**Affordability Ratings:**

| Rating | Condition |
|--------|-----------|
| affordable | Index below 30% |
| moderate | Index between 30% and 40% |
| expensive | Index above 40% |

---

### 11. Market Summary

**GET** `/api/analytics/summary/`

Returns an overall summary of the housing market data.

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

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK — request successful |
| 201 | Created — resource created successfully |
| 204 | No Content — resource deleted successfully |
| 400 | Bad Request — invalid input data |
| 401 | Unauthorised — authentication credentials missing or invalid |
| 404 | Not Found — resource does not exist |
| 405 | Method Not Allowed — HTTP method not supported on this endpoint |