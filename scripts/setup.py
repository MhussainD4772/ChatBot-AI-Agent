#!/usr/bin/env python3
"""
Setup Script for AI Chatbot
===========================

This script helps set up the AI chatbot project:
- Creates necessary directories
- Sets up database
- Installs dependencies
- Downloads language models

Usage:
    python scripts/setup.py

Author: Mohammed (SDET & AI Enthusiast)
"""

import os
import sys
import subprocess
import shutil

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        'data',
        'logs',
        'config',
        'src/api',
        'src/database', 
        'src/ml',
        'src/frontend',
        'tests',
        'docs',
        'scripts'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ Created {directory}/")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("   ✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error installing dependencies: {e}")
        return False
    
    return True

def download_language_model():
    """Download spaCy language model"""
    print("\n🧠 Downloading language model...")
    
    try:
        subprocess.run([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'], check=True)
        print("   ✅ Language model downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error downloading language model: {e}")
        return False
    
    return True

def setup_database():
    """Set up PostgreSQL database"""
    print("\n🗄️ Setting up database...")
    
    try:
        # Check if PostgreSQL is running
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ PostgreSQL is installed")
            
            # Create database
            subprocess.run(['createdb', 'chatbot_db'], check=True)
            print("   ✅ Database 'chatbot_db' created")
            
            # Run migration
            subprocess.run([sys.executable, 'scripts/migrate_data.py'], check=True)
            print("   ✅ Database migration completed")
        else:
            print("   ⚠️ PostgreSQL not found. Please install PostgreSQL first.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error setting up database: {e}")
        return False
    
    return True

def create_env_file():
    """Create .env file from template"""
    print("\n🔑 Creating environment file...")
    
    if not os.path.exists('.env'):
        if os.path.exists('config/env_example.txt'):
            shutil.copy('config/env_example.txt', '.env')
            print("   ✅ Created .env file from template")
            print("   💡 Please edit .env file with your API keys")
        else:
            print("   ⚠️ Environment template not found")
    else:
        print("   ✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up AI Chatbot Project")
    print("=" * 40)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        return False
    
    # Download language model
    if not download_language_model():
        print("\n❌ Setup failed at language model download")
        return False
    
    # Set up database
    if not setup_database():
        print("\n⚠️ Database setup failed, but continuing...")
    
    # Create environment file
    create_env_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Edit .env file with your API keys")
    print("   2. Run: python run_chatbot.py")
    print("   3. Run: python run_webapp.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
