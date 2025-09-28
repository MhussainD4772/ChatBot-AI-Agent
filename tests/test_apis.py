"""
Test script for API integrations
===============================

This script tests the API integrations without requiring API keys.
It demonstrates how the APIs will work once keys are added.

Author: Mohammed (SDET & AI Enthusiast)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.api_manager import APIManager

def test_apis():
    """Test all API integrations"""
    print("🧪 Testing API Integrations")
    print("=" * 40)
    
    api = APIManager()
    
    # Test Crypto API (works without keys)
    print("\n💰 Testing Crypto API...")
    crypto_result = api.get_crypto_price("bitcoin")
    if crypto_result['success']:
        data = crypto_result['data']
        print(f"✅ Bitcoin Price: ${data['price_usd']:,.2f}")
        print(f"   24h Change: {data['price_change_24h']:.2f}%")
        print(f"   Market Cap: ${data['market_cap']:,.0f}")
    else:
        print(f"❌ Error: {crypto_result['error']}")
    
    # Test top cryptocurrencies
    print("\n📊 Testing Top Cryptocurrencies...")
    top_crypto_result = api.get_top_cryptocurrencies(3)
    if top_crypto_result['success']:
        cryptos = top_crypto_result['data']['cryptocurrencies']
        print("✅ Top 3 Cryptocurrencies:")
        for crypto in cryptos:
            print(f"   {crypto['rank']}. {crypto['name']} ({crypto['symbol']}) - ${crypto['price']:,.2f}")
    else:
        print(f"❌ Error: {top_crypto_result['error']}")
    
    # Test Weather API (needs API key)
    print("\n🌤️ Testing Weather API...")
    weather_result = api.get_weather("London")
    if weather_result['success']:
        data = weather_result['data']
        print(f"✅ Weather in {data['city']}: {data['temperature']}°C")
        print(f"   Description: {data['description']}")
        print(f"   Humidity: {data['humidity']}%")
    else:
        print(f"❌ Weather API needs API key: {weather_result['error']}")
    
    # Test News API (needs API key)
    print("\n📰 Testing News API...")
    news_result = api.get_news("technology")
    if news_result['success']:
        articles = news_result['data']['articles']
        print(f"✅ Found {len(articles)} tech news articles:")
        for i, article in enumerate(articles[:2], 1):
            print(f"   {i}. {article['title'][:60]}...")
    else:
        print(f"❌ News API needs API key: {news_result['error']}")
    
    print("\n🎉 API testing completed!")
    print("\n💡 Next steps:")
    print("   1. Get free API keys for Weather and News")
    print("   2. Add keys to .env file")
    print("   3. Test with real data")

if __name__ == "__main__":
    test_apis()
