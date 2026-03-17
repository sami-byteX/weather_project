from rest_framework import serializers
from .services import WeatherManager, WeatherServiceError


class WeatherRequestSerializer(serializers.Serializer):
    """
    Serializer for weather API requests.
    Validates that city name is provided and not empty.
    """
    city = serializers.CharField(
        max_length=100,
        min_length=1,
        trim_whitespace=True,
        error_messages={
            'blank': 'City name cannot be empty.',
            'max_length': 'City name cannot exceed 100 characters.',
            'min_length': 'City name must contain at least one character.'
        }
    )


class WeatherResponseSerializer(serializers.Serializer):
    """
    Serializer for weather API responses.
    Formats the weather data in a user-friendly way.
    """
    city = serializers.CharField()
    country = serializers.CharField()
    temperature = serializers.FloatField(help_text="Temperature in Celsius")
    humidity = serializers.IntegerField(help_text="Humidity percentage")
    wind_speed = serializers.FloatField(help_text="Wind speed in km/h")
    weather_condition = serializers.CharField()
    sunrise = serializers.DateTimeField(allow_null=True, required=False)
    sunset = serializers.DateTimeField(allow_null=True, required=False)
    timestamp = serializers.DateTimeField()


class WeatherAPI:
    """
    API class that handles weather requests and responses.
    """
    
    def __init__(self):
        self.weather_manager = WeatherManager()
    
    def get_weather(self, city_name):
        """
        Get weather data for a city.
        
        Args:
            city_name (str): Name of the city
            
        Returns:
            dict: Serialized weather data
            
        Raises:
            WeatherServiceError: If weather fetch fails
        """
        weather_data = self.weather_manager.get_weather_for_city(city_name)
        serializer = WeatherResponseSerializer(weather_data)
        return serializer.data