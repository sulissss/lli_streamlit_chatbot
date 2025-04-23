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

# Routing logic
def show_home():
    st.title("🏠 Home Page")
    st.write("Welcome to the homepage!")
    st.link_button("Go to Rolle's Theorem", url="?page=rolles_theorem&id=1")
    st.link_button("Go to L' Hopital Rule", url="?page=lhopital_rule&id=1")
    st.link_button("Go to Optimization", url="?page=optimization&id=1")
    st.link_button("Go to Indefinite Integration", url="?page=indefinite_integration&id=1")
    

def show_pset(pset_name, id_):
    st.title(f"📘 {pset_name}: Problem {id_}")

    # --- Extract variable values from query parameters ---
    # e.g., value_a=5 -> {'a': '5'}
    variable_values = {}
    for key, value in query_params.items():
        if key.startswith("value_"):
            var_name = key[len("value_"):]
            # query_params values are lists, take the first
            if isinstance(value, list):
                variable_values[var_name] = value[0]
            else:
                variable_values[var_name] = value

    # --- Replace all $<var> in the problem text with their values ---
    raw_problem = problem_sets[pset_name][f'problem_{id_}']
    def substitute_vars(text, values):
        def replacer(match):
            var = match.group(1)
            return str(values.get(var, match.group(0)))
        return re.sub(r'\$(\w+)', replacer, text)

    # Use a single variable for both display and LLM input, allow user editing
    problem_key = f'{pset_name}_{id_}'
    if f'edited_problem_{problem_key}' not in st.session_state:
        # First time: use the substituted text
        st.session_state[f'edited_problem_{problem_key}'] = substitute_vars(raw_problem, variable_values)
    edited_problem_text = st.session_state[f'edited_problem_{problem_key}']

    # Dropdown (expander) for editing the problem statement
    with st.expander("✏️ Edit Problem Statement", expanded=False):
        new_text = st.text_area("Edit the problem text below. Changes will affect both display and chatbot:", value=edited_problem_text, height=200, key=f"edit_area_{problem_key}")
        if st.button("Confirm", key=f"confirm_btn_{problem_key}"):
            st.session_state[f'edited_problem_{problem_key}'] = new_text
            st.success("Problem text updated for this session!")
        st.info("Edits are session-only and will not persist if you reload the app.")

    # Always use the latest edited text for LLM and display
    problem_text = st.session_state[f'edited_problem_{problem_key}']
    problem_text = re.sub(r'\\\((.*?)\\\)', r'$\1$', problem_text)

    st.markdown("### Current Problem")
    # st.markdown("Note: If your answer contains a negative number, then do not leave any space between the negative sign and the number. For example, -x should not be written as - x.")
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
    with st.expander("\U0001F4D8 Click to hide the problem", expanded=True):
        st.markdown(f'<div class="gray-expander">', unsafe_allow_html=True)
        render_text_with_latex(problem_text)
        st.markdown("</div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Use st.write to avoid markdown bullet interpretation
            st.write(message["content"])

    if prompt := st.chat_input("Enter your query..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = st.write_stream(stream_response(prompt, problem_text))

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
