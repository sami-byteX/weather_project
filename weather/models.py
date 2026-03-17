from django.db import models
from django.utils import timezone


class City(models.Model):
    """
    Model to store city information for caching geocoding results.
    """
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country}"


class WeatherCache(models.Model):
    """
    Model to cache weather data for 10 minutes to improve performance.
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_cache')
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.IntegerField(help_text="Humidity percentage")
    wind_speed = models.FloatField(help_text="Wind speed in km/h")
    weather_code = models.IntegerField(help_text="Open-Meteo weather code")
    weather_description = models.CharField(max_length=100)
    sunrise = models.DateTimeField(null=True, blank=True)
    sunset = models.DateTimeField(null=True, blank=True)
    cached_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Weather Cache'
        verbose_name_plural = 'Weather Cache'
        unique_together = ['city', 'cached_at']
        ordering = ['-cached_at']

    def __str__(self):
        return f"Weather for {self.city.name} at {self.cached_at}"

    @property
    def is_expired(self):
        """Check if cache entry is older than 10 minutes."""
        cache_duration = timezone.now() - self.cached_at
        return cache_duration.total_seconds() > 600  # 10 minutes