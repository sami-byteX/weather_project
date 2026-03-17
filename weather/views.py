from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
import json
from .serializers import WeatherRequestSerializer, WeatherAPI, WeatherServiceError


class WeatherAPIView(View):
    """
    API view for handling weather requests.
    Endpoint: POST /weather/api/weather/
    """
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        """
        Handle POST requests for weather data.
        
        Expected JSON format:
        {
            "city": "CityName"
        }
        
        Returns:
        {
            "city": "CityName",
            "country": "Country",
            "temperature": 25.5,
            "humidity": 60,
            "wind_speed": 15.2,
            "weather_condition": "Clear sky",
            "sunrise": "2023-12-16T07:30:00+00:00",
            "sunset": "2023-12-16T17:45:00+00:00",
            "timestamp": "2023-12-16T12:00:00+00:00"
        }
        """
        try:
            # Parse JSON data
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'error': 'Invalid JSON format'
                }, status=400)
            
            # Validate input
            serializer = WeatherRequestSerializer(data=data)
            if not serializer.is_valid():
                return JsonResponse({
                    'error': 'Invalid input',
                    'details': serializer.errors
                }, status=400)
            
            city_name = serializer.validated_data['city']
            
            # Get weather data
            weather_api = WeatherAPI()
            weather_data = weather_api.get_weather(city_name)
            
            return JsonResponse(weather_data, status=200)
            
        except WeatherServiceError as e:
            error_message = str(e)
            # Provide more user-friendly error messages for common issues
            if "Failed to connect to weather service" in error_message:
                return JsonResponse({
                    'error': 'Unable to fetch weather data. Please check your internet connection and try again in a few minutes.'
                }, status=503)  # Service Unavailable
            elif "City" in error_message and "not found" in error_message:
                return JsonResponse({
                    'error': f'City "{city_name}" not found. Please check the spelling and try again.'
                }, status=400)  # Bad Request
            else:
                return JsonResponse({
                    'error': error_message
                }, status=503)  # Service Unavailable
        except Exception as e:
            return JsonResponse({
                'error': 'An unexpected error occurred'
            }, status=500)


class WeatherFrontendView(TemplateView):
    """
    Frontend view that serves the weather application interface.
    """
    template_name = 'weather/index.html'