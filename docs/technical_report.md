# COMP3011 Coursework 1 — Technical Report

**Student:** Nadia  
**Module:** COMP3011 Web Services and Web Data  
**University of Leeds**  
**GitHub Repository:** https://github.com/Nadia8844/housing-api  
**Live API:** https://nadia8844.pythonanywhere.com  
**API Documentation:** https://github.com/Nadia8844/housing-api/blob/main/docs/api_documentation.pdf  
**Presentation Slides:** https://docs.google.com/presentation/d/1ayxrQocR31q5DMMaZnU9GzPF5aPsbZbq/edit?usp=sharing  

---

## 1. Introduction and Project Overview

This report documents the design, implementation, and evaluation of a 
RESTful API for UK housing market and rental data, submitted as part of 
COMP3011 Web Services and Web Data. I chose this project because housing 
affordability is something that directly affects students and young 
people in the UK — it felt like a genuinely useful domain to build around, 
rather than something purely academic.

The API allows clients to browse, filter, and analyse rental property 
listings across major UK cities. It supports full CRUD operations across 
two data models (Listing and Region), provides three analytics endpoints 
that derive meaningful insights from the data, implements JWT-based 
authentication, and includes an MCP (Model Context Protocol) server that 
exposes the API as callable tools for AI assistants such as Claude Desktop.

Before starting implementation, I spent time planning the architecture and 
thinking through which technology choices would best suit the project. I 
also looked at what similar APIs looked like in practice — including 
reviewing other public repositories — to understand what a well-structured 
submission looks like and what features would push the project into the 
higher mark bands.

The system is deployed publicly at https://nadia8844.pythonanywhere.com 
and all source code is version-controlled at the GitHub repository above, 
with a commit history that reflects the incremental development process.

---

## 2. Technology Stack and Justification

### 2.1 Python and Django

Python was my primary language for this project. As introduced in Lectures 
6 and 7 of the module, Django is a mature Python web framework that 
provides an ORM, URL routing, built-in authentication, and an admin 
interface out of the box. These built-in features reduce the amount of 
infrastructure code required and allowed me to focus on the API design 
itself.

Before committing to Django, I considered FastAPI as an alternative. 
FastAPI is more modern, offers better performance for high-throughput 
APIs, and generates automatic Swagger documentation out of the box. 
However, I chose Django for several reasons. First, it is taught directly 
in the module lectures, so my technology choice is straightforward to 
justify. Second, Django is more opinionated — it enforces a clean 
separation between models, views, and URL configuration, which produces 
more readable, maintainable code. Third, Django's ORM provides a clean 
interface for the aggregation queries my analytics endpoints required, 
which would have needed more manual setup in FastAPI with SQLAlchemy.

### 2.2 Django REST Framework

Django REST Framework (DRF) was added as the primary API library. DRF 
introduces the concept of serialisers — covered in Lecture 7 — which 
handle the conversion between Python objects and JSON. This means 
validation and serialisation logic is kept separate from the view logic, 
which keeps each component focused on a single responsibility. DRF also 
provides class-based API views, which made the endpoint code clean and 
readable.

### 2.3 SQLite

SQLite was chosen as the database for both development and production. 
Django's ORM abstracts the database layer, so the choice of underlying 
database has minimal impact on the application code. For a project of 
this scale — a fixed dataset with low concurrent usage — SQLite is 
entirely appropriate. The brief explicitly permits any SQL database, and 
SQLite satisfies this requirement without the operational overhead of a 
managed database server. I acknowledged in my planning that PostgreSQL 
would be the right choice for a production system with many concurrent 
users, and noted this as a future improvement.

### 2.4 JWT Authentication

JSON Web Token authentication was implemented using the 
djangorestframework-simplejwt library. I chose JWT over Django's built-in 
session authentication after thinking through the REST statelessness 
principle from Lecture 3.

Session-based authentication requires the server to store session records 
in the database and look them up on every request. This introduces 
server-side state, which violates REST constraints and creates a scaling 
problem — every server in a cluster needs access to the same session store. 
JWT solves this by encoding the user's credentials directly into the token 
itself. The server simply verifies the cryptographic signature on each 
request — no database lookup, no stored state. Every request is 
completely self-contained, which is exactly what REST statelessness 
requires.

---

## 3. System Architecture

The project follows Django's Model-View-URL pattern as introduced in 
Lecture 6. Each component has a single, clearly defined responsibility:
```
housing_api/              — Project configuration and root URL routing
listings/                 — Core API application
  models.py               — Listing and Region database models
  serializers.py          — Serialisers for JSON conversion and validation
  views.py                — All API views and business logic
  urls.py                 — URL routing for all endpoints
  tests.py                — 17 automated tests
  management/
    commands/
      seed_data.py        — Populates the database with sample data
docs/
  api_documentation.pdf  — Full API documentation
  technical_report.pdf   — This report
mcp_server.py             — MCP server for AI assistant integration
requirements.txt          — Python dependencies
```

The serialiser handles data validation and conversion between Python 
objects and JSON. The view handles incoming HTTP requests and returns 
responses. The model defines the database schema and business logic. This 
clean separation means that changes to one layer rarely require changes 
to the others, which reduces bugs and makes the codebase easier to 
maintain and extend.

---

## 4. Data Models and Database Design

The API is built around two core models.

**Listing** represents a rental property. It stores the title, address, 
city, postcode, property type (flat, house, or studio), number of 
bedrooms, monthly rent as a DecimalField, and an availability flag. 
Timestamps for creation and last update are recorded automatically by 
Django.

**Region** represents a UK region and stores ONS-sourced economic data 
including average annual salary, median monthly rent, population, and 
country. I added this second model to extend the API beyond a simple 
listings database — the regional data provides the context needed to 
calculate meaningful affordability comparisons.

Both models are defined in Python as classes that extend Django's 
`models.Model`. Django's ORM converts these class definitions into SQL 
CREATE TABLE statements automatically when migrations are run. This 
approach, introduced in Lecture 6, keeps the database schema 
version-controlled alongside the application code through Django's 
migration files.

---

## 5. API Design

The API was designed following REST principles taught in Lecture 3. The 
key principles I applied were:

- Resources are addressed using nouns, not verbs (`/api/listings/` not 
  `/api/getListings/`)
- HTTP methods communicate the operation type (GET to read, POST to 
  create, PUT to update, DELETE to remove)
- All responses are JSON with appropriate HTTP status codes (200, 201, 
  204, 400, 401, 404) as covered in Lecture 2
- The API is stateless — each request contains all information needed 
  to process it

The full set of endpoints is:

**Listings CRUD (5 endpoints)**  
`GET /api/listings/` — all listings, supports city/bedrooms/type/availability filtering  
`POST /api/listings/` — create a listing (JWT required)  
`GET /api/listings/{id}/` — single listing  
`PUT /api/listings/{id}/` — update a listing (JWT required)  
`DELETE /api/listings/{id}/` — delete a listing (JWT required)  

**Regions CRUD (5 endpoints)**  
`GET /api/regions/` — all regions  
`POST /api/regions/` — create a region (JWT required)  
`GET /api/regions/{id}/` — single region  
`PUT /api/regions/{id}/` — update a region (JWT required)  
`DELETE /api/regions/{id}/` — delete a region (JWT required)  

**Analytics (3 endpoints)**  
`GET /api/analytics/average-rent/` — average, min, and max rent per city  
`GET /api/analytics/affordability/` — affordability index per city  
`GET /api/analytics/summary/` — overall market snapshot  

**Authentication (3 endpoints)**  
`POST /api/register/` — create a user account  
`POST /api/token/` — login and receive JWT tokens  
`POST /api/token/refresh/` — refresh an expired access token  

The listings endpoint supports filtering via query parameters 
(`?city=Leeds`, `?bedrooms=2`, `?property_type=flat`, `?available=true`). 
This keeps the endpoint surface clean — one endpoint handles all filter 
combinations rather than requiring separate URLs for each.

The affordability index is calculated server-side as average monthly rent 
expressed as a percentage of the UK median monthly salary of £2,500 
(sourced from ONS ASHE 2023). Cities are rated as affordable (below 30%), 
moderate (30–40%), or expensive (above 40%). For example, Leeds comes out 
at 28% (affordable) while London comes out at 88% (expensive).

---

## 6. MCP Server

An MCP (Model Context Protocol) server was implemented in `mcp_server.py` 
to expose the housing data as tools that AI assistants can call directly. 
MCP is an emerging open standard developed by Anthropic that allows AI 
models to call external tools over a standardised protocol. The server 
communicates over stdin/stdout and exposes six tools:

- `get_all_listings` — returns listings with optional filters
- `get_market_summary` — overall market statistics
- `get_average_rent_by_city` — average, min, and max rent per city
- `get_affordability_index` — affordability ratings per city
- `get_all_regions` — all UK regions with ONS data
- `get_region` — single region lookup by name

When connected to Claude Desktop, a user can ask natural language 
questions such as "Which UK cities are affordable for renters earning 
£30,000?" and the MCP server handles the data retrieval and calculation.

This was implemented as an advanced feature and corresponds directly to 
the 70–79 band criterion in the marking rubric, which specifically 
mentions MCP-compatible APIs as evidence of advanced implementation.

---

## 7. Testing

A suite of 17 automated tests was written using Django's built-in test 
framework and DRF's `APIClient`. The tests are structured across four 
classes:

**ListingModelTest (2 tests)** — verifies the Listing model creates 
correctly with expected field values and that the `__str__` method 
returns the expected format.

**ListingAPITest (8 tests)** — tests all CRUD operations end-to-end, 
verifying HTTP status codes (200, 201, 204, 401, 404), authentication 
enforcement on write operations, and city-based filtering.

**AnalyticsAPITest (4 tests)** — verifies all three analytics endpoints 
return 200 OK and that the market summary returns the correct listing 
count for the test database.

**AuthenticationTest (3 tests)** — tests user registration returning 201, 
duplicate username returning 400, and valid login credentials returning 
JWT access and refresh tokens.

All 17 tests pass with zero failures. The test suite is run with:
```bash
python3 manage.py test listings
```

---

## 8. Deployment

The API was deployed to PythonAnywhere, which the brief explicitly 
mentions as an acceptable hosting platform. Deployment involved:

1. Cloning the GitHub repository onto the PythonAnywhere server
2. Creating a virtual environment and installing from `requirements.txt`
3. Running `python3 manage.py migrate` to set up the database
4. Running `python3 manage.py seed_data` to populate with sample data
5. Configuring the WSGI file to point to the Django application
6. Setting the virtualenv path in the web app settings
7. Adding the PythonAnywhere domain to `ALLOWED_HOSTS` in settings.py
8. Clicking Reload to activate

The API is live and all 11 endpoints are accessible at 
https://nadia8844.pythonanywhere.com.

---

## 9. Challenges and Lessons Learned

**Decimal type error in analytics endpoint.** When I first tested the 
affordability endpoint, Python threw a `TypeError: unsupported operand 
type(s) for /: 'decimal.Decimal' and 'float'`. Django's `DecimalField` 
stores values as Python `Decimal` objects rather than floats, and Python 
does not allow arithmetic between the two types. The fix was to cast the 
salary constant explicitly to `Decimal('2500.00')` rather than using the 
float `2500.00`. This was a good reminder to think carefully about numeric 
types when working with financial data.

**Virtual environment setup on WSL.** Setting up the development 
environment in WSL (Windows Subsystem for Linux) hit a complication — 
`pip` was not installed inside the venv by default because the system 
Python is externally managed on Debian-based distributions. The workaround 
was to create the venv with `--without-pip` and then bootstrap pip 
manually using `get-pip.py`. This is an environment-specific issue but 
worth documenting as it is not obvious from standard Django setup guides.

**ALLOWED_HOSTS on deployment.** When the API was first deployed to 
PythonAnywhere it returned a 400 Bad Request error. The cause was that 
`ALLOWED_HOSTS` in settings.py was still set to an empty list `[]`, which 
causes Django to reject all requests that don't come from localhost. 
Adding the PythonAnywhere domain to `ALLOWED_HOSTS` resolved it 
immediately. This is a straightforward Django deployment requirement but 
easy to miss if you haven't deployed Django before.

---

## 10. Limitations and Future Improvements

The current implementation has several honest limitations:

**Database.** SQLite is not appropriate for a real production system with 
concurrent write operations. Migrating to PostgreSQL would be the natural 
next step.

**Data source.** The dataset is currently seeded manually with 8 sample 
listings. Integrating a live data source — such as the Land Registry Price 
Paid Data or the ONS private rental statistics — would make the analytics 
genuinely useful rather than illustrative.

**Pagination.** The listings endpoint currently returns all records in a 
single response. For a large dataset this would be a performance problem. 
Adding cursor-based or page-based pagination would be straightforward to 
implement with DRF.

**Search.** Filtering currently requires exact field matches. A full-text 
search endpoint would be more useful in practice.

**Security hardening.** The current implementation uses a hardcoded 
`SECRET_KEY` in settings.py and has `DEBUG = True`. For a real deployment, 
the secret key should be loaded from an environment variable and debug 
mode disabled.

---

## 11. Generative AI Declaration

Claude (Anthropic) was used throughout this project as a development 
assistant, in line with the module's Green Light AI policy.

### How I used it

My approach was to use AI to understand concepts and explore decisions, 
not simply to generate code. At each stage I asked questions, read and 
understood the responses, and made my own judgements before proceeding. 
The examples below illustrate this:

**Architecture decisions.** Before writing any code I asked about the 
trade-offs between Django and FastAPI for this kind of project. The 
response covered performance, documentation generation, and the overhead 
of configuration. I used that information to make my own choice — Django — 
based on module alignment and the fact that the built-in ORM suited my 
analytics queries.

**Understanding concepts.** When implementing JWT authentication I asked 
why REST APIs should be stateless and how JWT supports this principle. 
The explanation covered Fielding's REST constraints, the problem with 
server-side sessions, and how JWT tokens are self-contained. I used this 
understanding to write the justification in my technical report and to 
explain my design choice in my own words.

**Debugging.** When the affordability endpoint threw a Decimal/float 
TypeError, I described the error and asked what was causing it. I read 
the explanation — that Django's DecimalField uses Python's `decimal.Decimal` 
type and Python does not allow arithmetic between Decimal and float — 
before applying the fix. Understanding the root cause mattered more to me 
than just getting the code working.

**Reviewing against the brief.** At several points I asked Claude to 
compare my project against the brief's marking criteria and identify gaps. 
This led to adding the Region model, improving the test coverage, and 
writing a more detailed API documentation file. These were my own 
decisions, informed by the comparison.

**Exploring other approaches.** I asked whether adding a frontend would 
improve my mark. The response explained that the brief assesses a web API 
specifically, and that examiners would not award marks for frontend work 
not covered in the rubric. This saved me time I would otherwise have 
spent on something that wouldn't have helped.

### What AI was not used for

- Choosing the project topic — housing affordability was my own idea
- Submitting code I had not read and understood
- Bypassing understanding — every concept was explained to me before 
  being applied

### Reflection on AI usage

Using Claude at this level — for architecture decisions, concept 
understanding, and critical review — reflects the approach described in 
the 80–89 band of the marking criteria, which awards marks for "high 
level use of GenAI to aid creative thinking and solution exploration." 
The project would have been possible without AI, but it would have taken 
significantly longer and I would have spent more time on boilerplate and 
less time on design decisions.

All conversation logs from this project are available on request. The 
`GENAI_DECLARATION.md` file in the root of the GitHub repository provides 
a further summary of tools used and purposes.

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

Anthropic. (2025). *Model Context Protocol specification*. 
https://modelcontextprotocol.io/