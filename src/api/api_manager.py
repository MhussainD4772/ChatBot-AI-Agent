"""
API Manager for AI Chatbot
=========================

This module handles all external API integrations for the chatbot.
It provides methods to fetch real-time data from:
- OpenWeatherMap API (weather data)
- NewsAPI (news headlines)
- CoinGecko API (cryptocurrency prices)

Author: Mohammed (SDET & AI Enthusiast)
"""

import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIManager:
    """
    API Manager class handles all external API calls.
    
    This class provides methods to:
    - Fetch weather data from OpenWeatherMap
    - Get news headlines from NewsAPI
    - Retrieve cryptocurrency prices from CoinGecko
    - Handle API errors gracefully
    """
    
    def __init__(self):
        """
        Initialize the API Manager with API keys and base URLs.
        
        Sets up configuration for all external APIs:
        - Weather API (OpenWeatherMap)
        - News API (NewsAPI.org)
        - Crypto API (CoinGecko - no key required)
        """
        # API Keys (you'll need to get these)
        self.weather_api_key = os.getenv('WEATHER_API_KEY', 'your_weather_api_key_here')
        self.news_api_key = os.getenv('NEWS_API_KEY', 'your_news_api_key_here')
        
        # API Base URLs
        self.weather_base_url = "http://api.openweathermap.org/data/2.5"
        self.news_base_url = "https://newsapi.org/v2"
        self.crypto_base_url = "https://api.coingecko.com/api/v3"
        
        # Request timeout (in seconds)
        self.timeout = 10
    
    def get_weather(self, city, country_code=None):
        """
        Get current weather data for a city.
        
        This method fetches real-time weather information including:
        - Temperature (current, min, max)
        - Weather description
        - Humidity and pressure
        - Wind speed and direction
        
        Args:
            city (str): Name of the city
            country_code (str, optional): Country code (e.g., 'US', 'UK')
            
        Returns:
            dict: Weather data or error message
        """
        try:
            # Construct the API URL
            if country_code:
                location = f"{city},{country_code}"
            else:
                location = city
            
            url = f"{self.weather_base_url}/weather"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'metric'  # Celsius
            }
            
            # Make API request
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract relevant weather information
                weather_info = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'min_temp': round(data['main']['temp_min']),
                    'max_temp': round(data['main']['temp_max']),
                    'description': data['weather'][0]['description'].title(),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', 0),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                return {
                    'success': True,
                    'data': weather_info
                }
            
            else:
                return {
                    'success': False,
                    'error': f"Weather API error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': "Weather API request timed out. Please try again."
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Weather API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error fetching weather: {str(e)}"
            }
    
    def get_news(self, topic=None, country='us', language='en'):
        """
        Get latest news headlines.
        
        This method fetches current news articles from various sources:
        - Can filter by topic (e.g., 'technology', 'business')
        - Supports different countries and languages
        - Returns headlines, descriptions, and source information
        
        Args:
            topic (str, optional): News topic to filter by
            country (str): Country code for news (default: 'us')
            language (str): Language code (default: 'en')
            
        Returns:
            dict: News data or error message
        """
        try:
            # Construct the API URL
            if topic:
                url = f"{self.news_base_url}/everything"
                params = {
                    'q': topic,
                    'apiKey': self.news_api_key,
                    'language': language,
                    'sortBy': 'publishedAt',
                    'pageSize': 5  # Limit to 5 articles
                }
            else:
                url = f"{self.news_base_url}/top-headlines"
                params = {
                    'country': country,
                    'apiKey': self.news_api_key,
                    'pageSize': 5
                }
            
            # Make API request
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'ok' and data['totalResults'] > 0:
                    articles = []
                    for article in data['articles']:
                        articles.append({
                            'title': article['title'],
                            'description': article['description'],
                            'source': article['source']['name'],
                            'url': article['url'],
                            'published_at': article['publishedAt']
                        })
                    
                    return {
                        'success': True,
                        'data': {
                            'topic': topic or 'top headlines',
                            'articles': articles,
                            'total_results': data['totalResults']
                        }
                    }
                else:
                    return {
                        'success': False,
                        'error': "No news articles found for the given topic."
                    }
            else:
                return {
                    'success': False,
                    'error': f"News API error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': "News API request timed out. Please try again."
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"News API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error fetching news: {str(e)}"
            }
    
    def get_crypto_price(self, coin_id='bitcoin'):
        """
        Get cryptocurrency price information.
        
        This method fetches real-time crypto data including:
        - Current price in USD
        - Price change (24h)
        - Market cap and volume
        - Price change percentage
        
        Args:
            coin_id (str): Cryptocurrency ID (default: 'bitcoin')
            
        Returns:
            dict: Crypto data or error message
        """
        try:
            # Construct the API URL
            url = f"{self.crypto_base_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            # Make API request
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                if coin_id in data:
                    crypto_data = data[coin_id]
                    
                    crypto_info = {
                        'coin_id': coin_id,
                        'coin_name': coin_id.title(),
                        'price_usd': crypto_data['usd'],
                        'price_change_24h': crypto_data.get('usd_24h_change', 0),
                        'market_cap': crypto_data.get('usd_market_cap', 0),
                        'volume_24h': crypto_data.get('usd_24h_vol', 0),
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    return {
                        'success': True,
                        'data': crypto_info
                    }
                else:
                    return {
                        'success': False,
                        'error': f"Cryptocurrency '{coin_id}' not found."
                    }
            else:
                return {
                    'success': False,
                    'error': f"Crypto API error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': "Crypto API request timed out. Please try again."
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Crypto API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error fetching crypto data: {str(e)}"
            }
    
    def get_top_cryptocurrencies(self, limit=5):
        """
        Get top cryptocurrencies by market cap.
        
        This method fetches a list of the top performing cryptocurrencies
        with their current prices and market information.
        
        Args:
            limit (int): Number of cryptocurrencies to return (default: 5)
            
        Returns:
            dict: Top crypto data or error message
        """
        try:
            # Construct the API URL
            url = f"{self.crypto_base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': False
            }
            
            # Make API request
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                top_cryptos = []
                for crypto in data:
                    top_cryptos.append({
                        'rank': crypto['market_cap_rank'],
                        'name': crypto['name'],
                        'symbol': crypto['symbol'].upper(),
                        'price': crypto['current_price'],
                        'price_change_24h': crypto['price_change_percentage_24h'],
                        'market_cap': crypto['market_cap'],
                        'volume': crypto['total_volume']
                    })
                
                return {
                    'success': True,
                    'data': {
                        'cryptocurrencies': top_cryptos,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f"Crypto API error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': "Crypto API request timed out. Please try again."
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Crypto API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error fetching top cryptocurrencies: {str(e)}"
            }

# Test the API Manager
if __name__ == "__main__":
    """
    Test section - runs when we execute: python api_manager.py
    
    This tests all API endpoints to ensure they're working correctly.
    """
    print("🧪 Testing API Manager...")
    
    api = APIManager()
    
    # Test weather API
    print("\n🌤️ Testing Weather API...")
    weather_result = api.get_weather("London")
    if weather_result['success']:
        print(f"✅ Weather: {weather_result['data']['temperature']}°C in {weather_result['data']['city']}")
    else:
        print(f"❌ Weather Error: {weather_result['error']}")
    
    # Test news API
    print("\n📰 Testing News API...")
    news_result = api.get_news("technology")
    if news_result['success']:
        print(f"✅ News: Found {len(news_result['data']['articles'])} articles")
    else:
        print(f"❌ News Error: {news_result['error']}")
    
    # Test crypto API
    print("\n💰 Testing Crypto API...")
    crypto_result = api.get_crypto_price("bitcoin")
    if crypto_result['success']:
        print(f"✅ Crypto: Bitcoin = ${crypto_result['data']['price_usd']:,.2f}")
    else:
        print(f"❌ Crypto Error: {crypto_result['error']}")
    
    print("\n🎉 API Manager test completed!")
