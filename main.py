import streamlit as st
import os
import re
import json
from google import genai
from utils import render_text_with_latex
from llm import stream_response
from dotenv import load_dotenv
# from mongodb import load_problem_sets

load_dotenv('.env')

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Webwork App", layout="wide")

# Access query parameters using the new API
query_params = st.query_params

page = query_params.get("page", "home")
id_ = query_params.get("id", None)


with open("problem_sets.json", "r") as file:
    problem_sets = json.loads(file.read())

with open("display_problem_sets.json", "r") as file:
    display_problem_sets = json.load(file)

# Routing logic
def show_home():
    st.title("🏠 Home Page")
    st.write("Welcome to the homepage!")
    st.link_button("Go to Rolle's Theorem", url="?page=rolles_theorem&id=1")
    st.link_button("Go to L' Hopital Rule", url="?page=lhopital_rule&id=1")
    st.link_button("Go to Optimization", url="?page=optimization&id=1")
    st.link_button("Go to Indefinite Integration", url="?page=indefinite_integration&id=1")
    

def show_pset(pset_name, id_):
    st.title(f"📘 {pset_name} Problem {id_}")
    st.markdown("### Current Problem")

    display_current_problem = re.sub(r'\\\((.*?)\\\)', r'$\1$', display_problem_sets[pset_name][f'problem_{id_}'])

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

    with st.expander("📘 Click to view the problem", expanded=True):
        st.markdown(f'<div class="gray-expander">', unsafe_allow_html=True)

        render_text_with_latex(display_current_problem)

        st.markdown("</div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your query..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        current_problem = problem_sets[pset_name][f'problem_{id_}']

        with st.chat_message("assistant"):
            response = st.write_stream(stream_response(prompt, current_problem))

        st.session_state.messages.append({"role": "assistant", "content": response})


# Render based on page
if page == "home":
    show_home()
elif page == "rolles_theorem":
    show_pset("Rolle's Theorem", id_)
elif page == "lhopital_rule":
    show_pset("L'Hopital Rule", id_)
elif page == "indefinite_integration":
    show_pset("Indefinite Integration", id_)
elif page and id_ and type(page) == str:
    show_pset(str(page).capitalize(), id_)
else:
    st.error("Page not found.")
