"""
API Integration Module
=====================

This module handles all external API integrations:
- OpenWeatherMap API (weather data)
- NewsAPI (news headlines)
- CoinGecko API (cryptocurrency prices)

Author: Mohammed (SDET & AI Enthusiast)
"""

from .api_manager import APIManager

__all__ = ['APIManager']
