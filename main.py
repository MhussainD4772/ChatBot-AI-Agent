"""
AI Chatbot with Database Integration
===================================

This chatbot uses PostgreSQL to store training data and conversation logs.
It loads training data from the database instead of hardcoded lists,
making it more scalable and maintainable.

Features:
- Intent classification using TF-IDF + Naive Bayes
- PostgreSQL database integration
- Conversation logging
- Multiple response variations per intent

Author: Mohammed (SDET & AI Enthusiast)
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import spacy
from database import DatabaseManager

# Load the English language model for text preprocessing
nlp = spacy.load("en_core_web_sm")

class DatabaseChatbot:
    """
    AI Chatbot that uses PostgreSQL for data storage.
    
    This chatbot:
    1. Loads training data from the database
    2. Uses TF-IDF + Naive Bayes for intent classification
    3. Logs all conversations to the database
    4. Provides multiple response variations per intent
    """
    
    def __init__(self):
        """
        Initialize the chatbot with database connection.
        
        Sets up:
        - Database connection manager
        - TF-IDF vectorizer for text processing
        - Naive Bayes classifier for intent prediction
        - Intent response mappings
        """
        # Database connection manager
        self.db = DatabaseManager()
        
        # Machine learning components
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        
        # Intent responses (will be loaded from database)
        self.intent_responses = {}
        
        # Training data (will be loaded from database)
        self.training_data = []
    
    def load_training_data(self):
        """
        Load training data from the PostgreSQL database.
        
        This method:
        1. Connects to the database
        2. Retrieves all intents and patterns
        3. Organizes data for machine learning
        4. Builds response mappings
        
        Returns:
            bool: True if successful, False if failed
        """
        print("📚 Loading training data from database...")
        
        # Connect to database
        if not self.db.connect():
            print("❌ Failed to connect to database!")
            return False
        
        try:
            # Get all intents from database
            intents = self.db.get_all_intents()
            
            if not intents:
                print("❌ No training data found in database!")
                return False
            
            # Process the data
            self.training_data = []
            self.intent_responses = {}
            
            for intent in intents:
                # Extract data from database record
                tag = intent['tag']
                pattern = intent['pattern']
                response = intent['response']
                
                # Add to training data (pattern, tag)
                self.training_data.append((pattern, tag))
                
                # Add to response mappings
                if tag not in self.intent_responses:
                    self.intent_responses[tag] = []
                self.intent_responses[tag].append(response)
            
            print(f"✅ Loaded {len(self.training_data)} training examples")
            print(f"📊 Found {len(self.intent_responses)} intent categories")
            
            # Show intent distribution
            for tag, responses in self.intent_responses.items():
                print(f"   {tag}: {len(responses)} examples")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading training data: {e}")
            return False
    
    def preprocess_text(self, text):
        """
        Clean and prepare text for machine learning.
        
        This method:
        1. Converts text to lowercase
        2. Removes stop words (the, and, is, etc.)
        3. Removes punctuation
        4. Lemmatizes words (running -> run)
        
        Args:
            text (str): Raw text input
            
        Returns:
            str: Cleaned and processed text
        """
        # Process text with spaCy
        doc = nlp(text.lower())
        
        # Extract meaningful tokens
        # - Remove stop words (common words like "the", "and")
        # - Remove punctuation
        # - Use lemmatized form (running -> run)
        tokens = [
            token.lemma_ 
            for token in doc 
            if not token.is_stop and not token.is_punct
        ]
        
        return " ".join(tokens)
    
    def train(self):
        """
        Train the machine learning model.
        
        This method:
        1. Preprocesses all training text
        2. Converts text to TF-IDF vectors
        3. Trains the Naive Bayes classifier
        4. Prepares for prediction
        """
        print("🧠 Training the AI model...")
        
        # Extract texts and intents from training data
        texts = [self.preprocess_text(text) for text, intent in self.training_data]
        intents = [intent for text, intent in self.training_data]
        
        # Convert text to numerical features (TF-IDF)
        # TF-IDF = Term Frequency × Inverse Document Frequency
        # This gives higher weight to important words
        X = self.vectorizer.fit_transform(texts)
        
        # Train the Naive Bayes classifier
        # This learns patterns from the training data
        self.classifier.fit(X, intents)
        
        print("✅ AI model trained successfully!")
    
    def predict_intent(self, user_input):
        """
        Predict the intent of user input.
        
        This method:
        1. Preprocesses the user input
        2. Converts to TF-IDF vector
        3. Predicts intent using trained model
        4. Returns intent and confidence score
        
        Args:
            user_input (str): What the user typed
            
        Returns:
            tuple: (intent, confidence_score)
        """
        # Preprocess the input text
        processed_text = self.preprocess_text(user_input)
        
        # Convert to TF-IDF vector
        X = self.vectorizer.transform([processed_text])
        
        # Predict intent
        intent = self.classifier.predict(X)[0]
        
        # Get confidence score (how sure the model is)
        confidence = self.classifier.predict_proba(X).max()
        
        return intent, confidence
    
    def get_response(self, intent):
        """
        Get a response for the predicted intent.
        
        This method:
        1. Looks up responses for the intent
        2. Randomly selects one response
        3. Returns a fallback if intent not found
        
        Args:
            intent (str): The predicted intent
            
        Returns:
            str: Bot response
        """
        # Get responses for this intent
        responses = self.intent_responses.get(intent, ["I'm not sure how to help with that."])
        
        # Randomly select one response
        return np.random.choice(responses)
    
    def log_conversation(self, user_input, predicted_intent, bot_response, confidence):
        """
        Log the conversation to the database.
        
        This method stores every interaction for analysis:
        - What the user said
        - What intent was predicted
        - How the bot responded
        - How confident the prediction was
        
        Args:
            user_input (str): What the user typed
            predicted_intent (str): Predicted intent
            bot_response (str): Bot's response
            confidence (float): Confidence score
        """
        # Try to log the conversation, but don't let it break the chat
        success = self.db.log_conversation(user_input, predicted_intent, bot_response, confidence)
        if not success:
            print("⚠️  Warning: Could not log conversation to database")
    
    def chat(self):
        """
        Main chat loop - the interactive part of the chatbot.
        
        This method:
        1. Displays welcome message
        2. Gets user input
        3. Predicts intent
        4. Generates response
        5. Logs conversation
        6. Continues until user quits
        """
        print("🤖 AI Chatbot with Database Integration")
        print("=" * 50)
        print("Type 'quit' to exit")
        print("-" * 50)
        
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for quit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Bot: Goodbye! 👋")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Predict intent and get response
            intent, confidence = self.predict_intent(user_input)
            response = self.get_response(intent)
            
            # Display response
            print(f"Bot: {response}")
            print(f"(Intent: {intent}, Confidence: {confidence:.2f})")
            
            # Log conversation to database
            # Convert numpy float to regular Python float for database compatibility
            confidence_float = float(confidence)
            self.log_conversation(user_input, intent, response, confidence_float)
    
    def close(self):
        """
        Close the database connection.
        
        Always call this when you're done with the chatbot
        to properly close the database connection.
        """
        self.db.close()

def main():
    """
    Main function to run the chatbot.
    
    This function:
    1. Creates a new chatbot instance
    2. Loads training data from database
    3. Trains the AI model
    4. Starts the chat loop
    5. Cleans up when done
    """
    print("🚀 Starting AI Chatbot...")
    
    # Create chatbot instance
    bot = DatabaseChatbot()
    
    try:
        # Load training data from database
        if not bot.load_training_data():
            print("❌ Failed to load training data!")
            return
        
        # Train the AI model
        bot.train()
        
        # Start chatting
        bot.chat()
        
    except KeyboardInterrupt:
        print("\n\n👋 Chatbot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Always close the database connection
        bot.close()
        print("🔌 Database connection closed")

# Run the chatbot when this file is executed directly
if __name__ == "__main__":
    main()