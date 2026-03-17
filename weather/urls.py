from django.urls import path
from .views import WeatherAPIView, WeatherFrontendView

app_name = 'weather'

urlpatterns = [
    path('', WeatherFrontendView.as_view(), name='index'),
    path('api/weather/', WeatherAPIView.as_view(), name='weather_api'),
]