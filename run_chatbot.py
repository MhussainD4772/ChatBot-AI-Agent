#!/usr/bin/env python3
"""
AI Chatbot - Main Entry Point
============================

This is the main entry point for running the AI chatbot.
It provides a simple command-line interface for testing.

Usage:
    python run_chatbot.py

Author: Mohammed (SDET & AI Enthusiast)
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ml.main import main

if __name__ == "__main__":
    main()
