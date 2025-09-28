"""
Database Manager for AI Chatbot
===============================

This module handles all database operations for our chatbot.
It connects to PostgreSQL and provides methods to:
- Store training data (intents, patterns, responses)
- Log conversations for analysis
- Retrieve data for the chatbot

Author: Mohammed (SDET & AI Enthusiast)
"""

# Import required libraries
import psycopg2  # PostgreSQL adapter for Python
from psycopg2.extras import RealDictCursor  # Returns results as dictionaries instead of tuples

class DatabaseManager:
    """
    DatabaseManager class handles all database operations.
    
    This class encapsulates all the database functionality:
    - Connection management
    - Data insertion and retrieval
    - Error handling
    """
    
    def __init__(self):
        """
        Initialize the DatabaseManager.
        
        Sets up instance variables for database connection and cursor.
        These will be populated when we connect to the database.
        """
        self.connection = None  # Will hold the PostgreSQL connection
        self.cursor = None      # Will hold the database cursor for executing queries
    
    def connect(self):
        """
        Connect to the PostgreSQL database.
        
        This method:
        1. Establishes a connection to the local PostgreSQL server
        2. Creates a cursor for executing SQL commands
        3. Returns True if successful, False if failed
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create connection to PostgreSQL database
            # host="localhost" means the database is running on this machine
            # database="chatbot_db" is the name of our database
            # user="chummu" is the database user (your username)
            self.connection = psycopg2.connect(
                host="localhost",
                database="chatbot_db",
                user="chummu"
            )
            
            # Create a cursor that returns results as dictionaries
            # This makes it easier to access data by column name
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("✅ Connected to PostgreSQL database!")
            return True
            
        except Exception as e:
            # If connection fails, print the error and return False
            print(f"❌ Error connecting to database: {e}")
            return False
    
    def close(self):
        """
        Close the database connection.
        
        This method:
        1. Closes the cursor (stops executing queries)
        2. Closes the connection (disconnects from database)
        3. Frees up system resources
        
        Always call this when you're done with the database!
        """
        if self.cursor:
            self.cursor.close()  # Close the cursor first
        if self.connection:
            self.connection.close()  # Then close the connection
        print("🔌 Database connection closed")
    
    def insert_intent(self, tag, pattern, response):
        """
        Insert a new intent into the database.
        
        This method stores training data for our chatbot:
        - tag: The intent category (e.g., "greet", "weather")
        - pattern: Example user input (e.g., "hello", "what's the weather")
        - response: Bot's response (e.g., "Hello! How can I help?")
        
        Args:
            tag (str): Intent category
            pattern (str): Example user input
            response (str): Bot response
            
        Returns:
            bool: True if successful, False if failed
        """
        try:
            # SQL query to insert data into the intents table
            # %s are placeholders for the values we'll provide
            query = """
                INSERT INTO intents (tag, pattern, response) 
                VALUES (%s, %s, %s)
            """
            
            # Execute the query with our data
            # The tuple (tag, pattern, response) provides values for the %s placeholders
            self.cursor.execute(query, (tag, pattern, response))
            
            # Commit the transaction to save changes to the database
            self.connection.commit()
            return True
            
        except Exception as e:
            # If insertion fails, print error and return False
            print(f"❌ Error inserting intent: {e}")
            return False
    
    def get_all_intents(self):
        """
        Get all intents from the database.
        
        This method retrieves all training data from the intents table.
        The data is ordered by tag and id for consistent results.
        
        Returns:
            list: List of dictionaries containing intent data
        """
        try:
            # SQL query to select all data from intents table
            # ORDER BY ensures consistent ordering of results
            query = "SELECT * FROM intents ORDER BY tag, id"
            
            # Execute the query
            self.cursor.execute(query)
            
            # Fetch all results and return them
            return self.cursor.fetchall()
            
        except Exception as e:
            # If query fails, print error and return empty list
            print(f"❌ Error fetching intents: {e}")
            return []
    
    def log_conversation(self, user_input, predicted_intent, bot_response, confidence):
        """
        Log a conversation to the database.
        
        This method stores every conversation for analysis:
        - What the user said
        - What intent we predicted
        - How the bot responded
        - How confident the prediction was
        
        Args:
            user_input (str): What the user typed
            predicted_intent (str): Intent we predicted
            bot_response (str): How the bot responded
            confidence (float): Confidence score (0.0 to 1.0)
            
        Returns:
            bool: True if successful, False if failed
        """
        try:
            # Check if we have a valid connection
            if not self.connection or self.connection.closed:
                print("⚠️  Database connection lost, reconnecting...")
                if not self.connect():
                    return False
            
            # SQL query to insert conversation data
            query = """
                INSERT INTO conversations (user_input, predicted_intent, bot_response, confidence) 
                VALUES (%s, %s, %s, %s)
            """
            
            # Execute the query with conversation data
            self.cursor.execute(query, (user_input, predicted_intent, bot_response, confidence))
            
            # Commit the transaction
            self.connection.commit()
            return True
            
        except Exception as e:
            # If logging fails, rollback the transaction and print error
            try:
                self.connection.rollback()
            except:
                pass  # Ignore rollback errors
            
            print(f"❌ Error logging conversation: {e}")
            return False

# Test the database connection
# This code only runs when we run this file directly (not when importing)
if __name__ == "__main__":
    """
    Test section - runs when we execute: python database.py
    
    This creates a DatabaseManager, tests the connection,
    and then closes it properly.
    """
    print("🧪 Testing database connection...")
    
    # Create a new DatabaseManager instance
    db = DatabaseManager()
    
    # Try to connect
    if db.connect():
        print("✅ Database connection successful!")
        print("🎉 Ready to store chatbot data!")
    else:
        print("❌ Database connection failed!")
        print("💡 Make sure PostgreSQL is running and chatbot_db exists")
    
    # Always close the connection when done
    db.close()