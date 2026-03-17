# Django Weather Application

A modern, responsive weather application built with Django and Django REST Framework. This application provides real-time weather information for any city using the Open-Meteo API and Nominatim geocoding service.

## Project Structure

This repository contains a single, complete Django weather application:

```
weather_project/          # Complete Django project with working weather app
├── weather/              # Django app containing all weather functionality
│   ├── models.py         # Database models for caching
│   ├── services.py       # Core service layer for API calls
│   ├── views.py          # DRF API views
│   ├── serializers.py    # DRF serializers
│   ├── templates/        # HTML templates
│   └── static/           # CSS and JavaScript files
└── weather_project/      # Project configuration
    ├── settings.py       # Django settings
    ├── urls.py           # URL routing
    └── wsgi.py           # WSGI configuration
```

**This is a complete, functional weather application** with:
- Full backend API using Django REST Framework
- Complete frontend with Bootstrap 5 and JavaScript
- Database models for caching and persistence
- Working API endpoints and user interface

## Features

- **Real-time Weather Data**: Current temperature, humidity, wind speed, and weather conditions
- **City Geocoding**: Automatic conversion of city names to coordinates
- **Smart Caching**: 10-minute cache for improved performance
- **Responsive Design**: Bootstrap 5 frontend that works on all devices
- **RESTful API**: Clean API endpoints for weather data
- **Error Handling**: Comprehensive error management with user-friendly messages
- **Modern UI**: Beautiful gradient design with smooth animations

## Project Structure

```
weather_project/
├── weather/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Database models for caching
│   ├── services.py        # Core service layer for API calls
│   ├── views.py           # DRF API views
│   ├── urls.py            # App-level URL routing
│   ├── serializers.py     # DRF serializers
│   ├── templates/weather/
│   │   └── index.html     # Bootstrap 5 frontend
│   └── static/weather/
│       ├── js/weather.js  # JavaScript for API calls
│       └── css/style.css  # Modern responsive styling
└── weather_project/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py        # Configured for templates, static files, DRF
    ├── urls.py            # Project-level URL routing
    └── wsgi.py
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- Existing virtual environment at `C:\Users\Rogue\Documents\projects\.venv`

### 1. Activate Virtual Environment

```bash
# Navigate to the project directory
cd C:\Users\Rogue\Documents\projects

# Activate the existing virtual environment
C:\Users\Rogue\Documents\projects\.venv\Scripts\activate
```

### 2. Install Dependencies

The project uses the existing requirements.txt which includes:
- Django 6.0.3
- Django REST Framework 3.16.1
- requests 2.31.0

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Navigate to the weather project directory
cd weather_project

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver 8001
```

The application will be available at:
- **Frontend**: http://127.0.0.1:8001/
- **Admin**: http://127.0.0.1:8001/admin/
- **API Endpoint**: http://127.0.0.1:8001/api/weather/

## API Usage

### Endpoint

```
POST /weather/api/weather/
```

### Request Format

```json
{
    "city": "CityName"
}
```

### Response Format

```json
{
    "city": "London",
    "country": "United Kingdom",
    "temperature": 15.2,
    "humidity": 65,
    "wind_speed": 12.5,
    "weather_condition": "Partly cloudy",
    "sunrise": "2023-12-16T07:30:00+00:00",
    "sunset": "2023-12-16T17:45:00+00:00",
    "timestamp": "2023-12-16T12:00:00+00:00"
}
```

### Error Responses

```json
{
    "error": "City 'InvalidCity' not found"
}
```

## Backend Architecture

### Service Layer (`weather/services.py`)

The application implements a clean service layer architecture:

1. **GeocodingService**: Handles city-to-coordinates conversion using Nominatim API
2. **WeatherService**: Fetches weather data from Open-Meteo API
3. **WeatherCodeMapper**: Maps Open-Meteo weather codes to user-friendly descriptions
4. **WeatherManager**: Orchestrates all services and handles caching

### Caching Strategy

- **Geocoding Cache**: 1-hour cache for city coordinates (geocoding doesn't change often)
- **Weather Cache**: 10-minute cache for weather data (balances freshness with performance)
- **Database Cache**: Persistent storage of city and weather data for offline access

### Models (`weather/models.py`)

- **City**: Stores city information and coordinates
- **WeatherCache**: Caches weather data with expiration tracking

## Frontend Features

### Technologies Used

- **Bootstrap 5**: Responsive framework
- **Font Awesome**: Icons
- **Custom CSS**: Modern styling with gradients and animations
- **Vanilla JavaScript**: API communication and DOM manipulation

### Key Features

- **Loading States**: Spinner during API calls
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Works on mobile and desktop
- **Smooth Animations**: Professional user experience

## API Integration

### Open-Meteo API

- **Purpose**: Provides current weather data
- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Data**: Temperature, humidity, wind speed, weather codes, sunrise/sunset
- **Rate Limits**: Free tier with generous limits for development

### Nominatim API

- **Purpose**: Geocoding city names to coordinates
- **Endpoint**: `https://nominatim.openstreetmap.org/search`
- **Usage**: Converts city names to latitude/longitude for weather API
- **Rate Limits**: 1 request per second, must include User-Agent

## Configuration

### Settings (`weather_project/settings.py`)

Key configurations:
- **Templates**: Located in `weather/templates/`
- **Static Files**: Located in `weather/static/`
- **Django REST Framework**: JSON renderer and parser only
- **Caching**: Local memory cache with 10-minute timeout
- **Security**: CSRF protection enabled

### Environment Variables

No environment variables required for basic functionality. For production deployment, consider:

```python
# In settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')
```

## Testing

### Manual Testing

Test the application with various inputs:

1. **Valid Cities**: "London", "New York", "Tokyo"
2. **Invalid Input**: Empty strings, special characters
3. **Non-existent Cities**: Made-up city names
4. **Edge Cases**: Very long city names, cities with special characters

### API Testing

Use curl or Postman to test the API endpoint:

```bash
curl -X POST http://127.0.0.1:8000/weather/api/weather/ \
  -H "Content-Type: application/json" \
  -d '{"city": "London"}'
```

## Performance Considerations

### Caching Benefits

- **Reduced API Calls**: Caching minimizes external API requests
- **Faster Response Times**: Cached data serves instantly
- **Rate Limit Protection**: Prevents hitting API rate limits
- **Offline Capability**: Database cache allows some functionality without internet

### Optimization Features

- **Smart Cache Keys**: Unique keys based on city name and coordinates
- **Cache Expiration**: Automatic cleanup of expired cache entries
- **Database Indexing**: Optimized queries for city lookups
- **Error Resilience**: Graceful handling of API failures

## Security

### CSRF Protection

- Enabled by default in Django
- Required for POST requests to API endpoint
- Automatically handled by frontend JavaScript

### Input Validation

- **City Name**: Maximum 100 characters, minimum 1 character
- **Trimming**: Automatic whitespace removal
- **Error Messages**: User-friendly validation feedback

### API Security

- **No Authentication**: Simple public API for weather data
- **Rate Limiting**: Handled by external APIs
- **Input Sanitization**: Django handles SQL injection protection

## Deployment

### Production Considerations

1. **Static Files**: Configure static file serving (e.g., with Nginx)
2. **Database**: Use PostgreSQL instead of SQLite
3. **Caching**: Use Redis for distributed caching
4. **Security**: Set DEBUG=False, configure ALLOWED_HOSTS
5. **Environment**: Use environment variables for sensitive data

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure virtual environment is activated
2. **Port Already in Use**: Change port with `python manage.py runserver 8001`
3. **API Rate Limits**: Check if requests are being blocked by external APIs
4. **Static Files Not Loading**: Run `python manage.py collectstatic`

### Debug Mode

Enable debug mode in `settings.py`:

```python
DEBUG = True
```

### Logging

Check Django logs for API errors:

```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'weather': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper documentation
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
- Check the troubleshooting section
- Review Django and DRF documentation
- Open an issue on the project repository

## Third-Party APIs

### Open-Meteo
- **Website**: https://open-meteo.com/
- **API Documentation**: https://open-meteo.com/en/docs
- **Rate Limits**: Free tier with generous limits

### Nominatim
- **Website**: https://nominatim.org/
- **Usage Policy**: https://operations.osmfoundation.org/policies/nominatim/
- **Rate Limits**: 1 request per second

## Assumptions and Limitations

### Assumptions

1. **Internet Connection**: Application requires internet for API calls
2. **API Availability**: Depends on Open-Meteo and Nominatim API uptime
3. **Timezone**: Uses UTC for internal operations, converts to local timezone for display
4. **User Input**: Assumes users will enter valid city names

### Limitations

1. **No Dark Mode**: As specified in requirements
2. **No Geolocation**: As specified in requirements
3. **Single City**: Only supports one city at a time
4. **Current Weather Only**: No historical or forecast data
5. **No Authentication**: Public API without user accounts

## Future Enhancements

Potential improvements for future versions:

1. **Forecast Data**: Add 7-day weather forecast
2. **Multiple Cities**: Support for multiple saved cities
3. **User Accounts**: Personalized weather preferences
4. **Push Notifications**: Weather alerts and notifications
5. **Advanced Caching**: Redis for production deployments
6. **Mobile App**: Native mobile application
7. **Unit Tests**: Comprehensive test suite
8. **CI/CD**: Automated deployment pipeline