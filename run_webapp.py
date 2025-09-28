#!/usr/bin/env python3
"""
AI Chatbot - Web Application Entry Point
=======================================

This is the entry point for running the Streamlit web application.

Usage:
    python run_webapp.py
    # or
    streamlit run run_webapp.py

Author: Mohammed (SDET & AI Enthusiast)
"""

import sys
import os
import subprocess

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    # Run the Streamlit app
    streamlit_app_path = os.path.join(os.path.dirname(__file__), 'src', 'frontend', 'streamlit_app.py')
    subprocess.run(['streamlit', 'run', streamlit_app_path])
