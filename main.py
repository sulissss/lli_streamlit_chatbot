from google import genai
from mongodb import *
import re
import streamlit as st
import os

# Initialize the Gemini client with your API key

# Choose the generative model
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Define the question in a readable format
# question_text = (
#     "### Current Question\n"
#     "Suppose that $f(x) = x^2$ for all numbers $x$.\n\n"
#     "Determine what:\n"
#     "$$\\frac{f(p) - 7744}{p - 88}$$\n"
#     "approaches as $p$ approaches 88."
# )

# Function to stream responses from Gemini
def stream_response(prompt, question_text):
    full_prompt = f"""Assume you are a teacher guiding a confused student toward the answer.
You must not directly provide the answer but help them find the right approach.

The question:
{question_text}

Student's prompt:
{prompt}"""
    response_stream = client.models.generate_content_stream(
        model="gemini-2.0-flash", contents=[full_prompt]
    )
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

# ---------------------------------
# Function to call the LLM to clean problem text
def clean_problem_text(latex_problem):
    prompt = (
        "Convert the following LaTeX problem into a more readable format, "
        "using a friendlier font and formatting while preserving all wording and math expressions exactly as given:\n\n"
        f"{latex_problem}"
    )
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text

# ---------------------------------
# Function to extract problems from LaTeX code and clean them using the LLM
def extract_problems(latex_code):
    pattern = r"({\\bf Problem.*?)(?=\\hrule)"
    raw_problems = re.findall(pattern, latex_code, re.DOTALL)
    cleaned_problems = []
    for p in raw_problems:
        p = p.strip()
        cleaned = clean_problem_text(p)
        cleaned_problems.append(cleaned)
    return cleaned_problems

# ---------------------------------
# Load problem sets from MongoDB into session state (if not already loaded)
if "problem_sets_db" not in st.session_state:
    st.session_state.problem_sets_db = load_problem_sets()

# ---------------------------------
# Sidebar: Admin Login Section
st.sidebar.header("Admin Login")
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if authenticate_admin(username_input, password_input):
            st.session_state.admin_logged_in = True
            st.sidebar.success("Logged in as admin.")
        else:
            st.sidebar.error("Invalid credentials.")

# If admin is logged in, show the upload panel
if st.session_state.admin_logged_in:
    st.sidebar.subheader("Upload Problem Set")
    pset_name_input = st.sidebar.text_input("Enter Problem Set Name for Upload", key="upload_pset_name")
    uploaded_file = st.sidebar.file_uploader("Upload Problem Set File (hardcopy.tex)", type=["tex"], key="upload_file")
    if st.sidebar.button("Upload Problem Set", key="upload_btn"):
        if pset_name_input and uploaded_file:
            latex_code = uploaded_file.read().decode("utf-8")
            problems = extract_problems(latex_code)
            save_problem_set(pset_name_input, problems)
            st.session_state.problem_sets_db[pset_name_input] = problems
            st.sidebar.success(f"Uploaded problem set '{pset_name_input}' with {len(problems)} problems.")
        else:
            st.sidebar.error("Please provide a problem set name and upload a file.")

# ---------------------------------
# Sidebar: Select a Problem Set and a Problem from the DB
if st.session_state.problem_sets_db:
    selected_pset = st.sidebar.selectbox("Select Problem Set", list(st.session_state.problem_sets_db.keys()))
    st.session_state.current_pset = selected_pset
    problems = st.session_state.problem_sets_db[selected_pset]

    if problems:
        problem_number = st.sidebar.selectbox("Select Problem", [f"Problem {idx}" for idx in range(1, len(problems)+1)])
        problem_number = int(problem_number[8:])
        st.session_state.current_problem = problems[problem_number-1]
    else:
        st.sidebar.write("No problems found in this problem set.")
else:
    st.sidebar.write("No problem sets available. Please ask an admin to upload one.")


def render_text_with_latex(content):
    # Replace escaped LaTeX parentheses with inline LaTeX format
    content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)
    
    # Render the entire string as Markdown (preserves inline LaTeX formatting)
    st.markdown(content)

# ---------------------------------
# Main Chat Interface
st.title("WebWork Chatbot for Math 101")

if "current_problem" in st.session_state:
    current_problem = st.session_state.current_problem
    st.markdown("### Current Problem")
    # st.latex(current_problem)
    # if "$" in current_problem or "\\(" in current_problem:
    #     st.latex(rf"""{current_problem}""")
    # else:
    #     st.markdown(current_problem)
    render_text_with_latex(current_problem)

    
    # Separate chat history per problem
    if "chat_history_db" not in st.session_state:
        st.session_state.chat_history_db = {}
    key = f"{st.session_state.current_pset}::{current_problem}"
    if key not in st.session_state.chat_history_db:
        st.session_state.chat_history_db[key] = []
    chat_history = st.session_state.chat_history_db[key]
    
    # Display previous chat messages
    for message in chat_history:
        with st.chat_message(message["role"]):
            if "$" in message["content"] or "\\(" in message["content"]:
                st.latex(message["content"])
            else:
                st.markdown(message["content"])
    
    # Chat input for a new query
    if prompt := st.chat_input("Enter your query"):
        with st.chat_message("user"):
            st.markdown(prompt)
        chat_history.append({"role": "user", "content": prompt})
        
        # Placeholder for AI response
        ai_message_placeholder = st.chat_message("ai")
        response_placeholder = ai_message_placeholder.empty()
        
        full_response = ""
        for streamed_response in stream_response(prompt, current_problem):
            full_response += streamed_response
            response_placeholder.markdown(full_response)
        
        with ai_message_placeholder:
            if "$" in full_response or "\\(" in full_response:
                st.latex(full_response)
            else:
                st.markdown(full_response)
        chat_history.append({"role": "ai", "content": full_response})
else:
    st.write("Please select a problem set and a problem from the sidebar.")
