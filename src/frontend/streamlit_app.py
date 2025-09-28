"""
AI Chatbot Web Frontend
=======================

This Streamlit app provides a beautiful web interface for the AI chatbot.
Features:
- Interactive chat interface
- Real-time responses
- Intent visualization
- Confidence scores
- Chat history
- Database integration

Author: Mohammed (SDET & AI Enthusiast)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import sys
import os

# Add the current directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import DatabaseManager
from ml.main import DatabaseChatbot

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: auto;
        text-align: right;
    }
    .bot-message {
        background-color: #f5f5f5;
        margin-right: auto;
    }
    .confidence-bar {
        height: 8px;
        background-color: #e0e0e0;
        border-radius: 4px;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #ff4444, #ffaa00, #00aa00);
        transition: width 0.3s ease;
    }
    .intent-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.25rem;
    }
    .intent-greet { background-color: #e8f5e8; color: #2e7d32; }
    .intent-bye { background-color: #fff3e0; color: #f57c00; }
    .intent-weather { background-color: #e3f2fd; color: #1976d2; }
    .intent-personal { background-color: #f3e5f5; color: #7b1fa2; }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    
    This function sets up the initial state for the chat interface,
    including chat history, bot instance, and other UI elements.
    """
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'bot' not in st.session_state:
        st.session_state.bot = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'intent_stats' not in st.session_state:
        st.session_state.intent_stats = {}

def load_chatbot():
    """
    Load and initialize the chatbot.
    
    This function:
    1. Creates a new DatabaseChatbot instance
    2. Loads training data from the database
    3. Trains the machine learning model
    4. Stores the bot in session state
    
    Returns:
        bool: True if successful, False if failed
    """
    if st.session_state.bot is None:
        with st.spinner("🤖 Loading AI Chatbot..."):
            try:
                # Create chatbot instance
                bot = DatabaseChatbot()
                
                # Load training data from database
                if not bot.load_training_data():
                    st.error("❌ Failed to load training data from database!")
                    return False
                
                # Train the AI model
                bot.train()
                
                # Store in session state
                st.session_state.bot = bot
                st.success("✅ Chatbot loaded successfully!")
                return True
                
            except Exception as e:
                st.error(f"❌ Error loading chatbot: {e}")
                return False
    
    return True

def get_intent_color(intent):
    """
    Get color class for intent badge.
    
    Args:
        intent (str): The intent name
        
    Returns:
        str: CSS class name for styling
    """
    color_map = {
        'greet': 'intent-greet',
        'bye': 'intent-bye',
        'weather': 'intent-weather',
        'personal': 'intent-personal'
    }
    return color_map.get(intent, 'intent-greet')

def display_chat_message(message, is_user=True, intent=None, confidence=None):
    """
    Display a chat message with proper styling.
    
    Args:
        message (str): The message text
        is_user (bool): True if user message, False if bot message
        intent (str): The predicted intent (for bot messages)
        confidence (float): The confidence score (for bot messages)
    """
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Bot message with intent and confidence
        intent_html = ""
        if intent:
            intent_class = get_intent_color(intent)
            intent_html = f'<span class="intent-badge {intent_class}">{intent}</span>'
        
        confidence_html = ""
        if confidence is not None:
            confidence_percent = int(confidence * 100)
            confidence_html = f"""
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: {confidence_percent}%"></div>
            </div>
            <small>Confidence: {confidence_percent}%</small>
            """
        
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>Bot:</strong> {message}<br>
            {intent_html}
            {confidence_html}
        </div>
        """, unsafe_allow_html=True)

def update_intent_stats(intent):
    """
    Update intent statistics for visualization.
    
    Args:
        intent (str): The intent name
    """
    if intent in st.session_state.intent_stats:
        st.session_state.intent_stats[intent] += 1
    else:
        st.session_state.intent_stats[intent] = 1

def create_intent_chart():
    """
    Create a pie chart showing intent distribution.
    
    Returns:
        plotly.graph_objects.Figure: The pie chart figure
    """
    if not st.session_state.intent_stats:
        return None
    
    # Prepare data for the chart
    intents = list(st.session_state.intent_stats.keys())
    counts = list(st.session_state.intent_stats.values())
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=intents,
        values=counts,
        hole=0.3,
        marker_colors=['#e8f5e8', '#fff3e0', '#e3f2fd', '#f3e5f5']
    )])
    
    fig.update_layout(
        title="Intent Distribution",
        font=dict(size=12),
        showlegend=True,
        height=300
    )
    
    return fig

def create_confidence_chart():
    """
    Create a bar chart showing confidence scores over time.
    
    Returns:
        plotly.graph_objects.Figure: The bar chart figure
    """
    if not st.session_state.chat_history:
        return None
    
    # Extract confidence scores from chat history
    confidences = [entry['confidence'] for entry in st.session_state.chat_history if entry.get('confidence')]
    
    if not confidences:
        return None
    
    # Create bar chart
    fig = go.Figure(data=[go.Bar(
        x=list(range(len(confidences))),
        y=confidences,
        marker_color=['#ff4444' if c < 0.5 else '#ffaa00' if c < 0.8 else '#00aa00' for c in confidences]
    )])
    
    fig.update_layout(
        title="Confidence Scores Over Time",
        xaxis_title="Message Number",
        yaxis_title="Confidence Score",
        height=300
    )
    
    return fig

def main():
    """
    Main function to run the Streamlit app.
    
    This function:
    1. Sets up the page layout
    2. Initializes the chatbot
    3. Handles user interactions
    4. Displays analytics and statistics
    """
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.markdown('<h1 class="main-header">🤖 AI Chatbot</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for controls and analytics
    with st.sidebar:
        st.header("📊 Analytics")
        
        # Load chatbot
        if st.button("🔄 Reload Chatbot"):
            st.session_state.bot = None
            st.rerun()
        
        # Intent statistics
        if st.session_state.intent_stats:
            st.subheader("Intent Distribution")
            intent_chart = create_intent_chart()
            if intent_chart:
                st.plotly_chart(intent_chart, use_container_width=True)
        
        # Confidence scores
        if st.session_state.chat_history:
            st.subheader("Confidence Scores")
            confidence_chart = create_confidence_chart()
            if confidence_chart:
                st.plotly_chart(confidence_chart, use_container_width=True)
        
        # Database connection status
        st.subheader("Database Status")
        try:
            db = DatabaseManager()
            if db.connect():
                st.success("✅ Connected")
                db.close()
            else:
                st.error("❌ Disconnected")
        except:
            st.error("❌ Error")
    
    # Load chatbot if not already loaded
    if not load_chatbot():
        st.stop()
    
    # Main chat interface
    st.subheader("💬 Chat with the AI")
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(
            message['content'],
            message['is_user'],
            message.get('intent'),
            message.get('confidence')
        )
    
    # Chat input (must be outside of columns)
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            'content': user_input,
            'is_user': True,
            'timestamp': datetime.now()
        })
        
        # Get bot response
        with st.spinner("🤔 Thinking..."):
            try:
                # Predict intent and get response
                intent, confidence = st.session_state.bot.predict_intent(user_input)
                response = st.session_state.bot.get_response(intent)
                
                # Log conversation to database
                confidence_float = float(confidence)
                st.session_state.bot.log_conversation(user_input, intent, response, confidence_float)
                
                # Add bot response to history
                st.session_state.messages.append({
                    'content': response,
                    'is_user': False,
                    'intent': intent,
                    'confidence': confidence_float,
                    'timestamp': datetime.now()
                })
                
                # Update statistics
                update_intent_stats(intent)
                
                # Add to chat history for analytics
                st.session_state.chat_history.append({
                    'user_input': user_input,
                    'intent': intent,
                    'confidence': confidence_float,
                    'timestamp': datetime.now()
                })
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        # Rerun to update the display
        st.rerun()
    
    # Quick Actions Section
    st.markdown("---")
    st.subheader("🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👋 Say Hello", use_container_width=True):
            st.session_state.messages.append({
                'content': "hello",
                'is_user': True,
                'timestamp': datetime.now()
            })
            st.rerun()
    
    with col2:
        if st.button("🌤️ Ask About Weather", use_container_width=True):
            st.session_state.messages.append({
                'content': "what's the weather",
                'is_user': True,
                'timestamp': datetime.now()
            })
            st.rerun()
    
    with col3:
        if st.button("👤 Ask About You", use_container_width=True):
            st.session_state.messages.append({
                'content': "tell me about you",
                'is_user': True,
                'timestamp': datetime.now()
            })
            st.rerun()
    
    with col4:
        if st.button("👋 Say Goodbye", use_container_width=True):
            st.session_state.messages.append({
                'content': "goodbye",
                'is_user': True,
                'timestamp': datetime.now()
            })
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.intent_stats = {}
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ by Mohammed | Powered by Streamlit & PostgreSQL</p>
        <p>TF-IDF + Naive Bayes | Supervised Learning</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
