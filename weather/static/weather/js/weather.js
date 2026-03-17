/**
 * Weather App JavaScript
 * Handles API communication and DOM updates
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('weatherForm');
    const cityInput = document.getElementById('cityInput');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    const weatherCard = document.getElementById('weatherCard');
    
    // Form submission handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const city = cityInput.value.trim();
        
        if (city) {
            getWeatherData(city);
        }
    });
    
    /**
     * Fetch weather data from the API
     * @param {string} city - City name
     */
    async function getWeatherData(city) {
        // Show loading state
        showLoading(true);
        hideError();
        hideWeatherCard();
        
        try {
            const csrfToken = getCsrfToken();
            const response = await fetch('/api/weather/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                },
                body: JSON.stringify({ city: city })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayWeatherData(data);
            } else {
                showError(data.error || 'Failed to fetch weather data');
            }
            
        } catch (error) {
            console.error('Error fetching weather data:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            showLoading(false);
        }
    }
    
    /**
     * Display weather data in the UI
     * @param {Object} data - Weather data object
     */
    function displayWeatherData(data) {
        // Update city and country
        document.getElementById('cityName').textContent = data.city;
        document.getElementById('countryName').textContent = data.country || 'Unknown';
        
        // Update temperature
        document.getElementById('temperature').textContent = Math.round(data.temperature);
        
        // Update weather condition
        document.getElementById('weatherCondition').textContent = data.weather_condition;
        
        // Update details
        document.getElementById('apparentTemperature').textContent = `${Math.round(data.apparentTemperature || data.temperature)}°C`;
        document.getElementById('humidity').textContent = `${data.humidity}%`;
        
        // Show weather card
        weatherCard.classList.remove('d-none');
    }
    
    /**
     * Show error message
     * @param {string} message - Error message
     */
    function showError(message) {
        errorText.textContent = message;
        errorMessage.classList.remove('d-none');
    }
    
    /**
     * Hide error message
     */
    function hideError() {
        errorMessage.classList.add('d-none');
    }
    
    /**
     * Show or hide loading spinner
     * @param {boolean} show - Whether to show loading spinner
     */
    function showLoading(show) {
        if (show) {
            loadingSpinner.classList.remove('d-none');
        } else {
            loadingSpinner.classList.add('d-none');
        }
    }
    
    /**
     * Hide weather card
     */
    function hideWeatherCard() {
        weatherCard.classList.add('d-none');
    }
    
    /**
     * Format time as HH:MM
     * @param {Date} date - Date object
     * @returns {string} Formatted time string
     */
    function formatTime(date) {
        if (!date || isNaN(date.getTime())) {
            return 'N/A';
        }
        
        // Convert to local time to handle timezone properly
        const localTime = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
        const hours = localTime.getHours().toString().padStart(2, '0');
        const minutes = localTime.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
    
    /**
     * Get CSRF token from cookies
     * @returns {string} CSRF token
     */
    function getCsrfToken() {
        let token = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === 'csrftoken=') {
                    token = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return token;
    }
});