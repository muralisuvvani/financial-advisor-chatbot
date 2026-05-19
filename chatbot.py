import os
from google import genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API Key
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini_study")

# Streamlit Page Config
st.set_page_config(
    page_title="Financial Advisor AI",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
<style>

/* Main Background */
.main {
    background-color: #0E1117;
    color: white;
}

/* Header Styling */
.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #3B82F6;
    text-align: center;
    margin-bottom: 10px;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 18px;
    margin-bottom: 35px;
}

/* User Chat Bubble */
.user-message {
    background-color: #1E293B;
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    color: white;
    font-size: 16px;
}

/* Bot Chat Bubble */
.bot-message {
    background-color: #111827;
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    color: #F9FAFB;
    font-size: 16px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Sidebar Text */
.sidebar-content {
    color: #E2E8F0;
    font-size: 15px;
}

/* Input Box */
.stChatInput input {
    background-color: #1E293B !important;
    color: white !important;
}

/* Remove Streamlit Header/Footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown(
    "<div class='main-title'>Financial Advisor AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>AI-powered financial guidance and budgeting assistance</div>",
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:

    st.markdown("## Features")

    st.markdown("""
    <div class='sidebar-content'>

    • Budget Planning  
    • Saving Strategies  
    • Investment Education  
    • Expense Management  
    • Financial Literacy  
    • Beginner-Friendly Guidance  

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class='sidebar-content'>
    This chatbot provides educational financial guidance only and should not be considered professional financial advice.
    </div>
    """, unsafe_allow_html=True)

    # Clear Chat Button
    if st.button("Clear Chat"):

        st.session_state.messages = []

        if "chat_session" in st.session_state:
            del st.session_state.chat_session

        st.rerun()

# Initialize Gemini Client
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

client = st.session_state.client

# System Prompt
SYSTEM_PROMPT = """
You are an intelligent AI Financial Advisor chatbot.

Your role is to help users understand personal finance in a simple, practical, and safe way.

Responsibilities:
- Explain budgeting
- Teach saving strategies
- Explain investments simply
- Help users improve financial habits
- Provide beginner-friendly financial education

Guidelines:
- Use clear and professional language
- Keep responses concise and informative
- Give practical examples when needed
- Avoid risky financial advice
- Never guarantee profits

Tone:
- Professional
- Helpful
- Educational
"""

# Create Chat Session
if "chat_session" not in st.session_state:

    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
            top_p=0.9
        )
    )

# Store Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":

            st.markdown(
                f"<div class='user-message'>{message['content']}</div>",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"<div class='bot-message'>{message['content']}</div>",
                unsafe_allow_html=True
            )

# User Input
user_input = st.chat_input(
    "Ask a financial question..."
)

# Handle User Message
if user_input:

    # Store User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display User Message
    with st.chat_message("user"):

        st.markdown(
            f"<div class='user-message'>{user_input}</div>",
            unsafe_allow_html=True
        )

    # Gemini Chat Session
    chat = st.session_state.chat_session

    # Loading Spinner
    with st.spinner("Generating response..."):

        response = chat.send_message(user_input)

        bot_reply = response.text

    # Store Bot Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

    # Display Bot Response
    with st.chat_message("assistant"):

        st.markdown(
            f"<div class='bot-message'>{bot_reply}</div>",
            unsafe_allow_html=True
        )