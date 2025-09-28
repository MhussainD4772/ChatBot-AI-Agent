"""
Test script for the Streamlit frontend
=====================================

This script tests the chatbot functionality without the web interface.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ml.main import DatabaseChatbot

def test_chatbot():
    """Test the chatbot functionality"""
    print("🧪 Testing Chatbot Functionality")
    print("=" * 40)
    
    # Create chatbot
    bot = DatabaseChatbot()
    
    # Load training data
    if not bot.load_training_data():
        print("❌ Failed to load training data!")
        return
    
    # Train the model
    bot.train()
    
    # Test messages
    test_messages = [
        "hello",
        "tell me about you",
        "what's the weather",
        "goodbye"
    ]
    
    print("\n💬 Testing Chat Messages:")
    print("-" * 30)
    
    for message in test_messages:
        print(f"\nYou: {message}")
        
        # Get response
        intent, confidence = bot.predict_intent(message)
        response = bot.get_response(intent)
        
        print(f"Bot: {response}")
        print(f"Intent: {intent}")
        print(f"Confidence: {confidence:.2f}")
        
        # Log conversation
        bot.log_conversation(message, intent, response, float(confidence))
    
    print("\n✅ Test completed successfully!")
    
    # Close database connection
    bot.close()

if __name__ == "__main__":
    test_chatbot()
