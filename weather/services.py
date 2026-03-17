import requests
import logging
from datetime import datetime
from django.core.cache import cache
from django.utils import timezone
from .models import City, WeatherCache

logger = logging.getLogger(__name__)


class WeatherServiceError(Exception):
    """Custom exception for weather service errors."""
    pass


class GeocodingService:
    """
    Service for geocoding city names to coordinates using Nominatim API.
    """
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            'User-Agent': 'WeatherApp/1.0 (https://github.com/weather-app/contact)'
        }
    
    def get_coordinates(self, city_name):
        """
        Get coordinates for a city using Nominatim API.
        
        Args:
            city_name (str): Name of the city
            
        Returns:
            dict: Dictionary with latitude, longitude, and country
            
        Raises:
            WeatherServiceError: If geocoding fails
        """
        cache_key = f"geocode_{city_name.lower().strip()}"
        
        # Check cache first
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Geocoding cache hit for: {city_name}")
            return cached_result
        
        try:
            params = {
                'q': city_name,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                raise WeatherServiceError(f"City '{city_name}' not found")
            
            location = data[0]
            lat = float(location['lat'])
            lon = float(location['lon'])
            country = location.get('address', {}).get('country', '')
            
            result = {
                'latitude': lat,
                'longitude': lon,
                'country': country
            }
            
            # Cache for 1 hour (geocoding doesn't change often)
            cache.set(cache_key, result, 3600)
            logger.info(f"Geocoding successful for: {city_name}")
            
            return result
            
        except requests.RequestException as e:
            logger.error(f"Geocoding request failed for {city_name}: {e}")
            raise WeatherServiceError(f"Failed to connect to geocoding service: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Invalid response format for {city_name}: {e}")
            raise WeatherServiceError(f"Invalid response from geocoding service")


class WeatherService:
    """
    Service for fetching weather data using Open-Meteo API.
    """
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_weather(self, latitude, longitude):
        """
        Get current weather data for coordinates using Open-Meteo API.
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            dict: Weather data dictionary
            
        Raises:
            WeatherServiceError: If weather fetch fails
        """
        cache_key = f"weather_{latitude}_{longitude}"
        
        # Check cache first
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Weather cache hit for coordinates: {latitude}, {longitude}")
            return cached_result
        
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,wind_direction_10m,apparent_temperature,pressure_msl,visibility',
                'daily': 'temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_probability_max',
                'timezone': 'auto'
            }
            
            # Increased timeout to 15 seconds to handle slow connections
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if 'current' not in data:
                raise WeatherServiceError("No weather data available")
            
            current = data['current']
            
            # Convert timestamps
            sunrise_time = datetime.fromisoformat(data.get('daily', {}).get('sunrise', [''])[0]) if data.get('daily', {}).get('sunrise') else None
            sunset_time = datetime.fromisoformat(data.get('daily', {}).get('sunset', [''])[0]) if data.get('daily', {}).get('sunset') else None
            
            result = {
                'temperature': current['temperature_2m'],
                'humidity': current['relative_humidity_2m'],
                'wind_speed': current['wind_speed_10m'],
                'wind_direction': current.get('wind_direction_10m', 0),
                'weather_code': current['weather_code'],
                'apparent_temperature': current.get('apparent_temperature'),
                'pressure': current.get('pressure_msl'),
                'visibility': current.get('visibility'),
                'sunrise': sunrise_time,
                'sunset': sunset_time,
                'timestamp': timezone.now()
            }
            
            # Cache for 10 minutes
            cache.set(cache_key, result, 600)
            logger.info(f"Weather fetch successful for coordinates: {latitude}, {longitude}")
            
            return result
            
        except requests.RequestException as e:
            logger.error(f"Weather request failed for {latitude}, {longitude}: {e}")
            raise WeatherServiceError(f"Failed to connect to weather service: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Invalid weather response format: {e}")
            raise WeatherServiceError(f"Invalid response from weather service")


class WeatherCodeMapper:
    """
    Service for mapping Open-Meteo weather codes to user-friendly descriptions.
    """
    
    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    
    @classmethod
    def get_description(cls, code):
        """
        Get weather description for a given code.
        
        Args:
            code (int): Open-Meteo weather code
            
        Returns:
            str: User-friendly weather description
        """
        return cls.WEATHER_CODES.get(code, "Unknown weather condition")


class WeatherManager:
    """
    Main service class that orchestrates weather operations.
    """
    
    def __init__(self):
        self.geocoding_service = GeocodingService()
        self.weather_service = WeatherService()
    
    def get_weather_for_city(self, city_name):
        """
        Get weather data for a city by name.
        
        This method:
        1. Geocodes the city name to coordinates
        2. Fetches weather data for those coordinates
        3. Maps weather codes to descriptions
        4. Handles caching and database operations
        
        Args:
            city_name (str): Name of the city
            
        Returns:
            dict: Complete weather information including city details
            
        Raises:
            WeatherServiceError: If any step fails
        """
        try:
            # Step 1: Get coordinates
            geo_data = self.geocoding_service.get_coordinates(city_name)
            
            # Step 2: Get weather data
            weather_data = self.weather_service.get_weather(
                geo_data['latitude'], 
                geo_data['longitude']
            )
            
            # Step 3: Map weather code to description
            weather_description = WeatherCodeMapper.get_description(weather_data['weather_code'])
            
            # Step 4: Update or create city in database
            city, created = City.objects.get_or_create(
                name=city_name,
                defaults={
                    'latitude': geo_data['latitude'],
                    'longitude': geo_data['longitude'],
                    'country': geo_data['country']
                }
            )
            
            # Update city coordinates if they changed
            if not created and (city.latitude != geo_data['latitude'] or city.longitude != geo_data['longitude']):
                city.latitude = geo_data['latitude']
                city.longitude = geo_data['longitude']
                city.country = geo_data['country']
                city.save()
            
            # Step 5: Update or create weather cache
            weather_cache, created = WeatherCache.objects.update_or_create(
                city=city,
                defaults={
                    'temperature': weather_data['temperature'],
                    'humidity': weather_data['humidity'],
                    'wind_speed': weather_data['wind_speed'],
                    'weather_code': weather_data['weather_code'],
                    'weather_description': weather_description,
                    'sunrise': weather_data['sunrise'],
                    'sunset': weather_data['sunset']
                }
            )
            
            # Return complete weather information
            return {
                'city': city.name,
                'country': city.country,
                'temperature': weather_data['temperature'],
                'humidity': weather_data['humidity'],
                'wind_speed': weather_data['wind_speed'],
                'weather_condition': weather_description,
                'apparent_temperature': weather_data.get('apparent_temperature'),
                'pressure': weather_data.get('pressure'),
                'visibility': weather_data.get('visibility'),
                'sunrise': weather_data['sunrise'],
                'sunset': weather_data['sunset'],
                'timestamp': weather_data['timestamp']
            }
            
        except WeatherServiceError:
            # Re-raise service errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_weather_for_city: {e}")
            raise WeatherServiceError(f"An unexpected error occurred: {str(e)}")