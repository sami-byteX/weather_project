# 🌦️ Weather App

A modern weather application built with **Django** and **Django REST Framework** that lets users search for any city in the world and get real-time weather information.

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Bootstrap_5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"/>
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>

---

## Overview

This is a complete, functional weather application with:

- Full backend API using Django REST Framework
- Complete frontend with Bootstrap 5 and JavaScript
- Database models for caching and persistence
- Working API endpoints and user interface

### How it works

1. User visits the website (`http://127.0.0.1:8001/`)
2. Types a city name in the search box (e.g., "London", "New York")
3. Clicks **"Get Weather"**
4. Sees a loading spinner while data is fetched
5. Views the weather information:
   - Current temperature
   - Weather condition (sunny, cloudy, etc.)
   - Humidity percentage
   - Feels-like temperature
   - Country name

---

## Architecture

```
User (Browser)          Frontend                Backend
                      (HTML+CSS+JS)           (Django+DRF)
 Enter City    ──▶   JavaScript Fetch   ──▶    API Views
 View Results  ◀──   Updates DOM        ◀──    Service Layer
                                                    │
                                                    ▼
                                          External APIs
                                          • Open-Meteo (weather)
                                          • Nominatim (geocoding)
```

**Request flow:** form submit → JavaScript `fetch()` → Django URL router → `WeatherAPIView` → `WeatherRequestSerializer` validation → service layer → Nominatim geocoding (cached) → Open-Meteo weather fetch (cached) → JSON response → DOM update.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django, Django REST Framework, Python |
| Frontend | HTML, CSS, Bootstrap, vanilla JavaScript (Fetch API) |
| Data format | JSON |
| Geocoding | [Nominatim](https://nominatim.openstreetmap.org/) |
| Weather data | [Open-Meteo](https://api.open-meteo.com/) |
| Caching | Django's cache framework + database models |

---

## Project Structure

```
weather_project/           # Main project directory
├── weather/                # Django app for weather functionality
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # Database models (City, WeatherCache)
│   ├── services.py           # Business logic and external API calls
│   ├── views.py               # API endpoints and request handling
│   ├── urls.py                 # URL routing for the app
│   ├── serializers.py          # Data validation and serialization
│   ├── templates/
│   │   └── weather/
│   │       └── index.html
│   └── static/
│       └── weather/
│           ├── css/
│           │   └── style.css
│           └── js/
│               └── weather.js
└── weather_project/         # Project configuration
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

---

## Backend

### Key components

- **Models** (`models.py`) — database structure (City, WeatherCache)
- **Views** (`views.py`) — handle HTTP requests and responses
- **Serializers** (`serializers.py`) — validate input and format output
- **Service layer** (`services.py`) — business logic and external API calls

### API endpoint

`POST /api/weather/`

**Request:**
```json
{
    "city": "London"
}
```

**Response:**
```json
{
    "city": "London",
    "country": "United Kingdom",
    "temperature": 15.2,
    "humidity": 65,
    "weather_condition": "Partly cloudy"
}
```

### Service layer flow (`WeatherManager`)

1. Convert city name to coordinates via `GeocodingService`
2. Fetch weather data for those coordinates via `WeatherService`
3. Map the numeric weather code to a human-readable description
4. Return the formatted result

### External API integration

**Nominatim (geocoding)**
```
GET https://nominatim.openstreetmap.org/search
    ?q=London
    &format=json
    &limit=1
    &addressdetails=1
```
Must include a proper `User-Agent` header and stay within 1 request per second.

**Open-Meteo (weather)**
```
GET https://api.open-meteo.com/v1/forecast
    ?latitude=51.5074
    &longitude=-0.1278
    &current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code
    &timezone=auto
```

**Weather codes:**

| Code | Condition |
|---|---|
| 0 | Clear sky |
| 1 | Mainly clear |
| 2 | Partly cloudy |
| 3 | Overcast |
| 45 | Fog |
| 51–57 | Drizzle |
| 61–67 | Rain |
| 71–77 | Snow |
| 80–86 | Showers |
| 95–99 | Thunderstorm |

### Error handling

Custom `WeatherServiceError` exceptions are raised for failures and mapped to specific HTTP responses:

- Empty/invalid city input → validation error
- City not found → `400` with a specific message
- Network/upstream failure → `503` with a friendly message

---

## Frontend

- **Search form** — captures the city name and submits without a page reload
- **Loading spinner** — shown while the request is in flight
- **Weather card** — populated via DOM updates once data returns
- **Error message box** — shown on failed lookups

The frontend uses the JavaScript `fetch()` API to call `/api/weather/`, including a CSRF token (required by Django) read from cookies.

---

## Caching Strategy

| Data | Cache duration | Why |
|---|---|---|
| Geocoding result (city → coordinates) | 1 hour (3600s) | Coordinates don't change |
| Weather data | 10 minutes (600s) | Balances freshness with API load |

Two levels of caching are used:

1. **In-memory cache** for external API responses (geocoding + weather), keyed by `geocode_<city>` and `weather_<lat>_<lon>`.
2. **Database persistence** via the `City` model using `get_or_create()`, so repeated lookups don't need a fresh geocode.

---

## Software Engineering Concepts Demonstrated

- **REST API design** — resource-based endpoints using standard HTTP methods and JSON
- **MTV architecture** (Django's Model-Template-View pattern) — clear separation between data, logic, and presentation
- **Client-server communication** — stateless HTTP requests/responses between the JS frontend and Django backend
- **Asynchronous requests** — non-blocking `fetch()` calls with loading states
- **API abstraction** — the service layer hides the complexity of calling two external APIs behind a simple interface
- **Separation of concerns** — models, views, serializers, services, templates, and static files each handle one responsibility

---

## Running Locally

```bash
git clone <your-repo-url>
cd weather_project
python manage.py migrate
python manage.py runserver 8001
```

Then open `http://127.0.0.1:8001/` and search for a city.
