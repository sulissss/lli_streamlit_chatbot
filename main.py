import streamlit as st
import os
import re
from google import genai
from utils import render_text_with_latex
from llm import stream_response
from dotenv import load_dotenv
from mongodb import load_problem_sets

load_dotenv('.env')

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Webwork App", layout="wide")

# Access query parameters using the new API
query_params = st.query_params

page = query_params.get("page", "home")
id_ = query_params.get("id", None)


problem_sets = load_problem_sets()

# Routing logic
def show_home():
    st.title("🏠 Home Page")
    st.write("Welcome to the homepage!")
    st.link_button("Go to Continuity 1", url="?page=continuity&id=1")
    st.link_button("Go to Derivatives 1", url="?page=derivatives&id=1")

def show_pset(pset_name, id_):
    st.title(f"📘 {pset_name} Problem {id_}")
    # st.write(f"This is {pset_name} page with ID: {id_}")
    # st.link_button("Go to Home", url="?page=home")
    st.markdown("### Current Problem")
    with open(f"problem_sets/{pset_name}/problem_{id_}.txt", "r") as file:
        current_problem = file.read()
        current_problem = re.sub(r'\\\((.*?)\\\)', r'$\1$', current_problem)

    st.markdown(
        """
        <style>
        .gray-expander > div:first-child {
            background-color: #f5f5f5;
            border-radius: 0.5rem;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Expander for current problem
    with st.expander("📘 Click to view the problem", expanded=False):
        st.markdown(f'<div class="gray-expander">', unsafe_allow_html=True)
        render_text_with_latex(current_problem)
        st.markdown("</div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Enter your query..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # full_prompt = f"""Assume you are a teacher guiding a confused student toward the answer.
        # You must not directly provide the answer but help them find the right approach.

        # The question:
        # {current_problem}

        # Student's prompt:
        # {prompt}"""


        with st.chat_message("assistant"):
            # stream = client.models.generate_content_stream(
            #     model="gemini-2.0-flash", contents=[full_prompt]
            # )
            # for chunk in str:
            #     if chunk.text:
            response = st.write_stream(stream_response(prompt, current_problem))

        st.session_state.messages.append({"role": "assistant", "content": response})


# Render based on page
if page == "home":
    show_home()
elif page and id_ and type(page) == str:
    show_pset(str(page).capitalize(), id_)
else:
    st.error("Page not found.")