from dotenv import load_dotenv
from google import genai
import streamlit as st
import os

load_dotenv('keys.env')

# Initialize the Gemini client with your API key

# Choose the generative model
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Define the question in a readable format
question_text = (
    "### Current Question\n"
    "Suppose that $f(x) = x^2$ for all numbers $x$.\n\n"
    "Determine what:\n"
    "$$\\frac{f(p) - 7744}{p - 88}$$\n"
    "approaches as $p$ approaches 88."
)

# Function to stream responses token by token
def stream_response(prompt):
    prompt = f"""Assume you are a teacher guiding a confused student toward the answer. 
                You must not directly provide the answer but help them find the right approach.
                
                The question: {question_text}
                
                Student's prompt: {prompt}"""
    
    response_stream = client.models.generate_content_stream(
        model="gemini-2.0-flash", contents=[prompt]
    )
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

st.title("Welcome to the Chatbot for Calculus with AI!")

# Display the current question at the top
st.markdown(question_text)

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages from the session history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "$" in message["content"] or "\\(" in message["content"]:
            st.latex(message["content"])
        else:
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Enter your query"):
    # Display the user's message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add the user's message to the session history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Create a placeholder for the AI's response
    ai_message_placeholder = st.chat_message("ai")
    response_placeholder = ai_message_placeholder.empty()

    # Stream AI's response and update in real-time
    full_response = ""
    for streamed_response in stream_response(prompt):
        full_response += streamed_response
        response_placeholder.markdown(full_response)

    # Detect LaTeX and render properly
    with ai_message_placeholder:
        if "$" in full_response or "\\(" in full_response:
            st.latex(full_response)
        else:
            st.markdown(full_response)

    # Add the AI's full response to the session history
    st.session_state.messages.append({"role": "ai", "content": full_response})