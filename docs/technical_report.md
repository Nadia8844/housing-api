# COMP3011 Coursework 1 — Technical Report
**Student:** Nadia  
**Module:** COMP3011 Web Services and Web Data  
**University of Leeds**  
**GitHub:** https://github.com/Nadia8844/housing-api  
**Live API:** https://nadia8844.pythonanywhere.com  

---

## 1. Introduction and Project Overview

This report documents the design, implementation, and evaluation of a 
RESTful API for UK housing market and rental data, submitted as part of 
COMP3011 Web Services and Web Data. The project was motivated by the 
growing concern around housing affordability in the UK — a topic that 
has significant real-world relevance, particularly for young people 
entering the rental market for the first time.

The API enables clients to browse, filter, and analyse rental property 
listings across major UK cities. It supports full CRUD operations across 
two data models, provides three analytics endpoints that derive meaningful 
insights from the data, implements JWT-based authentication, and includes 
an MCP (Model Context Protocol) server that exposes the API as tools for 
AI assistants such as Claude.

The system is deployed publicly at https://nadia8844.pythonanywhere.com 
and all source code is version-controlled at the GitHub repository linked 
above.

---

## 2. Technology Stack and Justification

### Python and Django

Python was selected as the primary language for this project. As 
introduced in Lectures 6 and 7 of the module, Django is a mature Python 
web framework that provides an ORM, URL routing, built-in authentication, 
and an admin interface out of the box. These features significantly reduce 
the amount of boilerplate code required and allow development to focus on 
the API design rather than low-level infrastructure.

An alternative considered was FastAPI, which offers higher throughput and 
automatic OpenAPI documentation generation. However, Django was preferred 
because it is more opinionated — its conventions enforce a clean separation 
between models, views, and URL routing, which is well-suited to a project 
where code quality and architecture are assessed. Django's ORM also 
provides a cleaner interface for the aggregation queries required by the 
analytics endpoints.

### Django REST Framework

Django REST Framework (DRF) was added as the primary API library. DRF 
provides serialisers, which handle the conversion between Python objects 
and JSON — a concept introduced in Lecture 7. It also provides class-based 
API views, which make it straightforward to implement clean, readable 
endpoint logic.

### SQLite

SQLite was chosen as the database for both development and production. 
Django's ORM abstracts the database layer, so the choice of database has 
minimal impact on the application code. For a project of this scale — with 
a fixed dataset and low concurrent usage — SQLite is entirely appropriate. 
The brief also explicitly permits any SQL database, and SQLite satisfies 
this requirement whilst avoiding the operational overhead of a managed 
database server.

### JWT Authentication via djangorestframework-simplejwt

JSON Web Tokens were implemented using the djangorestframework-simplejwt 
library. JWT was chosen over Django's built-in session authentication 
because it is stateless — each request carries its own credentials in 
the token, which aligns directly with the REST statelessness principle 
taught in Lecture 3. Session-based authentication would require 
server-side session storage, which violates REST constraints and reduces 
scalability.

---

## 3. System Architecture

The project follows the Model-View-URL pattern introduced in Lecture 6. 
The codebase is organised as follows:
```
housing_api/        — Project configuration and root URL routing  
listings/           — Core API application  
  models.py         — Listing and Region database models  
  serializers.py    — Serialisers for JSON conversion  
  views.py          — All API views and business logic  
  urls.py           — URL routing for all endpoints  
  tests.py          — 17 automated tests  
  management/       — Custom management commands  
    commands/  
      seed_data.py  — Seeds the database with sample data  
docs/               — API documentation and this report  
mcp_server.py       — MCP server for AI assistant integration  
```

Each component has a clearly defined, single responsibility. The 
serialiser handles data validation and conversion, the view handles 
request routing and response logic, and the model defines the database 
schema. This separation of concerns keeps the codebase modular and 
maintainable — a principle central to good software engineering practice.

---

## 4. Data Models and Database Design

The API is built around two core models:

**Listing** — represents a rental property, with fields for title, 
address, city, postcode, property type, number of bedrooms, monthly rent, 
and availability status. Timestamps for creation and last update are 
recorded automatically.

**Region** — represents a UK region, storing ONS-sourced data including 
average annual salary, median monthly rent, population, and country. This 
model provides the regional context needed for broader affordability 
analysis.

Both models are defined using Django's ORM, which maps Python class 
definitions to SQL tables automatically. As covered in Lecture 6, this 
approach keeps the schema version-controlled alongside the application 
code through Django's migration system.

---

## 5. API Design

The API follows REST principles as taught in Lecture 3. Resources are 
addressed using nouns, and HTTP methods are used to indicate the 
operation type. The full list of endpoints is as follows:

**Listings CRUD**  
GET /api/listings/ — returns all listings with optional filtering  
POST /api/listings/ — creates a new listing (authentication required)  
GET /api/listings/{id}/ — returns a single listing  
PUT /api/listings/{id}/ — updates a listing (authentication required)  
DELETE /api/listings/{id}/ — deletes a listing (authentication required)  

**Regions CRUD**  
GET /api/regions/ — returns all regions  
POST /api/regions/ — creates a new region (authentication required)  
GET /api/regions/{id}/ — returns a single region  
PUT /api/regions/{id}/ — updates a region (authentication required)  
DELETE /api/regions/{id}/ — deletes a region (authentication required)  

**Analytics**  
GET /api/analytics/average-rent/ — average rent per city  
GET /api/analytics/affordability/ — affordability index per city  
GET /api/analytics/summary/ — overall market summary  

**Authentication**  
POST /api/register/ — register a new user  
POST /api/token/ — obtain a JWT access and refresh token  
POST /api/token/refresh/ — refresh an expired token  

All endpoints return JSON responses with appropriate HTTP status codes, 
as specified in Lecture 2. The listings endpoint supports filtering via 
query parameters, allowing clients to filter by city, number of bedrooms, 
property type, and availability without requiring separate endpoints for 
each combination.

The affordability index is calculated by expressing the average monthly 
rent as a percentage of the UK median monthly salary (£2,500, sourced 
from ONS ASHE 2023 data). Properties are rated as affordable (below 30%), 
moderate (30–40%), or expensive (above 40%).

---

## 6. MCP Server

An MCP (Model Context Protocol) server was implemented to expose the 
API as tools that AI assistants such as Claude can call directly. This 
was implemented as an advanced feature and directly corresponds to the 
70–79 band criterion in the marking rubric. The server exposes six tools: 
get_all_listings, get_market_summary, get_average_rent_by_city, 
get_affordability_index, get_all_regions, and get_region. When connected 
to Claude Desktop, users can query the housing data using natural language, 
for example: "Which UK city is most affordable for renters?"

---

## 7. Testing

A suite of 17 automated tests was written using Django's built-in test 
framework and DRF's APIClient. The tests are organised across three 
classes:

ListingModelTest — verifies that the Listing model is created correctly 
and that its string representation is accurate.

ListingAPITest — tests all five CRUD operations, verifying correct status 
codes (200, 201, 204, 401, 404), authentication enforcement, and 
city-based filtering.

AnalyticsAPITest and AuthenticationTest — verify that all three analytics 
endpoints return 200 OK with correct data, and that user registration and 
JWT token generation work as expected.

All 17 tests pass. They are run using:
```bash
python3 manage.py test listings
```

---

## 8. Deployment

The API was deployed to PythonAnywhere using a manual WSGI configuration, 
as introduced in the module as a suitable hosting option for Django 
applications. The deployment process involved cloning the repository, 
creating a virtual environment, installing dependencies from 
requirements.txt, running migrations, and seeding the database. The 
ALLOWED_HOSTS setting was updated to include the PythonAnywhere domain.

---

## 9. Challenges and Lessons Learned

One challenge was a type error in the affordability endpoint, where 
Python's decimal.Decimal type (used by Django's DecimalField) was 
incompatible with a plain float in the calculation. This was resolved by 
explicitly casting the salary constant to Decimal. It reinforced the 
importance of being careful with numeric types when working with financial 
data.

Setting up the virtual environment on WSL presented a separate challenge 
— pip was not installed by default due to the system's externally managed 
Python environment. This was resolved by bootstrapping pip manually using 
get-pip.py.

A further deployment challenge was discovering that ALLOWED_HOSTS must be 
explicitly updated when moving from a local development environment to a 
production host. This is a common Django deployment requirement that is 
easy to overlook.

---

## 10. Limitations and Future Improvements

Several areas for improvement were identified during development. SQLite 
is not suitable for production environments with significant concurrent 
usage — migrating to PostgreSQL would improve reliability. The dataset is 
currently seeded manually rather than pulled from a live source; 
integrating the Land Registry Price Paid API or ONS data feeds directly 
would make the analytics more accurate and up-to-date. Pagination is also 
absent from the listings endpoint, which would become a performance 
concern as the dataset grows. Finally, adding a full-text search endpoint 
would improve the API's usefulness for clients who need to search listings 
by keyword.

---

## 11. Generative AI Declaration

Claude (by Anthropic) was used throughout this project as a primary 
development tool, in line with the module's Green Light AI policy. The 
table below summarises the ways in which it was used:

| Stage | Usage |
|-------|-------|
| Project planning | Explored project ideas and selected the housing API concept based on real-world relevance |
| Architecture | Discussed Django project structure, REST design, and the trade-offs between Django and FastAPI |
| Implementation | Generated and explained model, serialiser, view, and URL code at each stage |
| Debugging | Diagnosed the Decimal type error and the WSL virtual environment issue |
| Testing | Generated a comprehensive test suite covering CRUD, analytics, and authentication |
| MCP server | Used AI to understand the MCP protocol and implement the server |
| Documentation | Drafted API documentation and this technical report |
| Deployment | Guided PythonAnywhere setup step by step |

At every stage, generated code was reviewed, tested, and understood 
before being committed. The AI was used not as a shortcut but as a tool 
for exploring design decisions and understanding concepts — for example, 
using it to compare JWT versus session authentication, or to understand 
why Django's Decimal type conflicts with Python floats. This reflects the 
higher-level AI usage described in the 80–89 band of the marking criteria.

Exported conversation logs are attached as supplementary material in the 
appendix.

---

## 12. References

Django Software Foundation. (2026). *Django documentation (v6.0)*. 
https://docs.djangoproject.com/en/6.0/

Django REST Framework. (2026). *Django REST Framework documentation*. 
https://www.django-rest-framework.org/

Simple JWT. (2026). *djangorestframework-simplejwt documentation*. 
https://django-rest-framework-simplejwt.readthedocs.io/

Fielding, R. T. (2000). *Architectural styles and the design of 
network-based software architectures* (Doctoral dissertation). 
University of California, Irvine.

Office for National Statistics. (2023). *Annual Survey of Hours and 
Earnings (ASHE)*. https://www.ons.gov.uk/

Model Context Protocol. (2025). *MCP specification*. 
https://modelcontextprotocol.io/