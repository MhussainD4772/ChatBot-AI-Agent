"""
Data Migration Script for AI Chatbot
====================================

This script moves training data from the hardcoded list in main.py
to the PostgreSQL database. This makes the data persistent and
easier to manage.

Author: Mohammed (SDET & AI Enthusiast)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.database import DatabaseManager

# Original training data from main.py
# This is what we're moving to the database
training_data = [
    # Greeting intents
    ("hello", "greet"),
    ("hi there", "greet"),
    ("hey", "greet"),
    ("good morning", "greet"),
    ("good afternoon", "greet"),
    
    # Goodbye intents
    ("bye", "bye"),
    ("goodbye", "bye"),
    ("see you later", "bye"),
    ("talk to you soon", "bye"),
    ("have a good day", "bye"),
    
    # Weather intents
    ("what's the weather", "weather"),
    ("how's the weather today", "weather"),
    ("is it raining", "weather"),
    ("will it be sunny", "weather"),
    ("weather forecast", "weather"),
    
    # Personal info intents
    ("tell me about you", "personal"),
    ("who are you", "personal"),
    ("what do you know about me", "personal"),
    ("tell me about mohammed", "personal"),
    ("what's your background", "personal"),
    ("introduce yourself", "personal")
]

# Responses for each intent
# These will be stored in the database as well
intent_responses = {
    "greet": [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?"
    ],
    "bye": [
        "Goodbye! Have a great day!",
        "See you later! Take care!"
    ],
    "weather": [
        "I can help with weather info! What city are you interested in?",
        "Weather updates coming right up! Which location?"
    ],
    "personal": [
        "I'm Mohammed, an SDET and AI enthusiast building hands-on projects to transition into AI/ML roles. Currently, I'm creating an AI agent - a chatbot with Python, FastAPI, and PostgreSQL to strengthen my skills in applied AI workflows!",
        "Hi! I'm Mohammed, working as an SDET while pursuing my passion for AI/ML. I'm building this chatbot as part of my journey to transition into applied AI roles.",
        "I'm Mohammed - an SDET by day, AI enthusiast by night! I'm working on this chatbot project to develop my skills in Python, FastAPI, and PostgreSQL for AI applications."
    ]
}

def migrate_data():
    """
    Migrate training data from code to database.
    
    This function:
    1. Connects to the database
    2. Clears any existing data (optional)
    3. Inserts all training patterns and responses
    4. Verifies the data was inserted correctly
    """
    print("🚀 Starting data migration...")
    
    # Create database manager
    db = DatabaseManager()
    
    # Connect to database
    if not db.connect():
        print("❌ Failed to connect to database!")
        return False
    
    try:
        # Clear existing data (optional - remove this if you want to keep existing data)
        print("🧹 Clearing existing data...")
        db.cursor.execute("DELETE FROM intents")
        db.connection.commit()
        
        # Insert training data
        print("📝 Inserting training data...")
        inserted_count = 0
        
        for pattern, tag in training_data:
            # Get a random response for this intent
            import random
            responses = intent_responses.get(tag, ["I'm not sure how to help with that."])
            response = random.choice(responses)
            
            # Insert into database
            if db.insert_intent(tag, pattern, response):
                inserted_count += 1
                print(f"  ✅ {tag}: '{pattern}' -> '{response[:50]}...'")
            else:
                print(f"  ❌ Failed to insert: {tag}: '{pattern}'")
        
        print(f"\n📊 Migration complete!")
        print(f"   Inserted {inserted_count} training examples")
        
        # Verify data was inserted
        print("\n🔍 Verifying data...")
        all_intents = db.get_all_intents()
        print(f"   Total records in database: {len(all_intents)}")
        
        # Show summary by intent
        intent_counts = {}
        for intent in all_intents:
            tag = intent['tag']
            intent_counts[tag] = intent_counts.get(tag, 0) + 1
        
        print("\n📈 Intent distribution:")
        for tag, count in intent_counts.items():
            print(f"   {tag}: {count} examples")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False
        
    finally:
        # Always close the database connection
        db.close()

if __name__ == "__main__":
    """
    Run the migration when this file is executed directly.
    """
    print("🤖 AI Chatbot Data Migration")
    print("=" * 40)
    
    if migrate_data():
        print("\n🎉 Migration successful!")
        print("💡 Your chatbot data is now stored in PostgreSQL!")
        print("🚀 Ready to update the chatbot to use the database!")
    else:
        print("\n❌ Migration failed!")
        print("💡 Check the error messages above for details.")