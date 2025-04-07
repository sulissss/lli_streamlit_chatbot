import streamlit as st
import os
import re
from google import genai
from utils import render_text_with_latex
from llm import stream_response
# from dotenv import load_dotenv
# from mongodb import load_problem_sets

# load_dotenv('.env')

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY])

st.set_page_config(page_title="Webwork App", layout="wide")

# Access query parameters using the new API
query_params = st.query_params

page = query_params.get("page", "home")
id_ = query_params.get("id", None)


# problem_sets = load_problem_sets()
problem_sets = {'Continuity': {'problem_1': '**Problem 1.** (1 point)\n\n**Problem**\n\nA continuous function is intuitively one whose graph can be drawn without lifting a pen off of the paper.\n\nMore mathematically, a function \\(f\\) is continuous at \\(a\\) if \\(f\\) is defined at \\(a\\) and the limit of \\(f\\) at \\(a\\) exists and if the limit value and the function value at \\(a\\) are equal.\n\nIf any of these three conditions fail to hold then \\(f\\) is not defined at \\(a\\).\n\nIt will be helpful to keep in mind that polynomial functions, sin and cos functions, their sums, differences, and products are continuous everywhere.\n\nQuotients of such functions are continuous wherever the denominator is not equal to zero.\n\nFor example, the function \\(f\\) defined by\n\n\\(f (x) = \\sin (x)\\) on the interval \\(I = [0, 2 \\pi]\\)\n\nis continuous everywhere.\n\n\\(f (x) = \\tan (x)\\) on the interval \\(I = [0, 2 \\pi]\\) is\n\n*   A. Discontinuous at \\(\\pi / 2\\) and \\(3 \\pi / 2\\) because it is not defined at those points.\n\n*   B. Continuous everywhere\n\n*   C. none of the above\n\n*Answer(s) submitted:*\n*   (incorrect)\n', 'problem_10': '**Problem 10.** \\footnotesize(1 point)\\normalsize\n\nEvaluate the following limits.\n\n(a)\n\\(\\displaystyle \\lim_{ x \\to \\infty } \\frac{8}{e^{x}-4}=\\)\n', 'problem_11': "**Problem 11.** (1 point)\n\nLet \\(f(x) =\n            \\begin{cases}\n              -\\frac{7}{x+1}, &\\text{if}\\ x< -1\\\\\n              3 x+8, &\\text{if}\\ x> -1\n              \\end{cases}\\)\n\nCalculate the following limits.  If the limit doesn't exist but it makes sense to call it \\(\\infty\\) enter **Infinity**, for \\(-\\infty\\) enter **-Infinity**; in other cases where the limit does not exist enter **DNE**.\n\n\\(\\displaystyle{\\lim_{x\\to -1^-}f(x)=}\\)\n", 'problem_12': '**Problem 12.** (1 point)\n\nThe slope of the tangent line to the graph of the function \\(y = 2 x^3\\) at the point \\((4 , 128)\\) is \\(\\text{lim}_{ x\\mapsto 4 } \\frac {2 x^3 -128 }{x- 4}\\). By trying values of \\(x\\) near \\(4\\), find the slope of the tangent line.\n', 'problem_13': '**Problem 13.** (1 point)\n\nConsider the following limit:\n\\[\\lim_{x\\to 3}\\frac{18 - 3 x - |x^2 - 6 x|}{|x^2- 36| - 27}\\]\nWe can simplify this limit by rewriting it as an expression without absolute values as follows:\n\n\\(\\lim_{x\\to 3}\\)\n', 'problem_14': '**Problem 14.** (1 point)\n\nLet\n\\[f(x) = \\begin{cases}\\displaystyle{b-2x}&\\text{if}\\ x < -1\\cr\n\\displaystyle{-\\frac{6}{x-b}}&\\text{if}\\ x \\ge -1.\\end{cases}\\]\nFind the two values of \\(b\\) for which \\(f\\) is\na continuous function at \\(-1\\).\n\nThe one with the greater absolute value is\n\\(b=\\)\\mbox{\\parbox[t]{7.5ex}{}}\n', 'problem_15': '**Problem 15.** (1 point)\n\nA function is said to have a **horizontal asymptote** if either the limit at infinity exists or the limit at negative infinity exists.\n\nShow that each of the following functions has a horizontal asymptote by calculating the given limit.\n\n\\( \\displaystyle{ \\lim_{x\\to\\infty}\\frac{-13 x}{8+2 x}= } \\)\n', 'problem_2': '**Problem 2.** (1 point)\n\n**Problem**\n\nA function \\(f\\) is continuous at \\(a\\) if all of the following hold:\n\n  1) \\(f (a)\\) exists\n\n  2) \\(\\lim_{x \\rightarrow a} f (x)\\) exists\n\n  3) \\(\\lim_{x \\rightarrow a} f (x) = f (a)\\)\n\nThe function is not continuous at \\(a\\) if any one of the conditions fails to hold.\n\nConsider the function \\(f\\) defined by\n\n\\[f(x) = \\begin{cases}\n{0} & \\text{ if }  x \\leq 0   \\\\\n {x^2} & \\text{ if }  x > 0.\n             \\end{cases}\\]\n\nThen\n\n*   A. \\(f (0)\\) does not exist\n*   B.  \\(f (0)\\) exists\n\n*   A.  \\(\\lim_{x \\rightarrow 0} f (x)\\) exists\n*   B. \\(\\lim_{x \\rightarrow 0} f (x)\\) does not exist\n\n*   A. \\(\\lim_{x \\rightarrow 0} f (x)\\) does not exist\n*   B. \\(\\lim_{x \\rightarrow 0} f(x)\\) exists but \\(\\lim_{x \\rightarrow 0} f (x) \\neq f (0)\\)\n*   C.   \\(\\lim_{x \\rightarrow 0} f (x) = f (0)\\)\n\n*   A.  \\(f\\) is continuous at 0\n*   B.  \\(f\\) is not continuous at 0\n\n*Answer(s) submitted:*\n*\n\n*\n\n*\n\n*\n(incorrect)\n', 'problem_3': '**Problem 3.** (1 point)\n\n**Problem**\n\nConsider the function\n\n\\[H(x) = \\begin{cases}\n{0} & \\text{ if }  x \\leq 0   \\\\\n {1} & \\text{ if }  x > 0.  \n             \\end{cases}\\]\n\nThen\n\n*   A.  \\(H (x)\\) is discontinuous at \\(x = 0\\) and continuous at \\(x = 1\\)\n*   B. \\(H (x)\\) is continuous at \\(x = 0\\) and discontinuous at \\(x = 1\\)\n*   C.  \\(H (x)\\) is continuous at \\(x = 0\\) and \\(x = 1\\)\n*   D. \\(H (x)\\) is discontinuous at \\(x = 0\\) and discontinuous at \\(x = 1\\)\n*   E. None of the above\n\n*Answer(s) submitted:*\n(incorrect)\n', 'problem_4': '**Problem 4.** (1 point)\n\n**Problem**\n\nIf \\(f\\) and \\(g\\) are functions with \\(f\\) continuous at \\(a\\) and \\(g\\) continuous at \\(f (a)\\) then the composite function \\(g \\circ f\\) is continuous at \\(a\\).\n\nLet \\(f (x) = \\sin (x)\\) and \\(g (x) = 1 / x\\).\n\nConsider the composition \\((g \\circ f) (x) = g (f (x))\\)\n\nThe composition \\(g \\circ f\\) is continuous for all \\(x\\) except\n\n* A.  \\(x = 0\\)\n* B. \\(x = 0, \\pm \\pi, \\pm 2 \\pi, \\ldots\\)\n* C.  \\(x = \\pi\\)\n* D. none of the above\n\n*Answer(s) submitted:*\n\n(incorrect)\n', 'problem_5': '**Problem 5.** (1 point)\n\nDefine a function \\(G : \\mathbb{R} \\rightarrow \\mathbb{R}\\) by\n\n\\[G(x) = \\begin{cases}\n\\sqrt x & \\text{ for } x \\neq 18   \\\\\n {c} & \\text{ for } x = 18.  \n             \\end{cases}\\] \n\nWhat value should \\(c\\) be so that \\(G\\) is continuous at 18 ?\n', 'problem_6': '**Problem 6.** **(1 point)**\n\nEstimate the following limit by substituting smaller and smaller values of \\(h\\).\n\n\\(\\lim\\limits_{h \\rightarrow 0} \\frac{4^h-1   }{h} =\\)\n\\mbox{\\parbox[t]{4ex}{}}\n', 'problem_7': '**Problem 7.** (1 point)\n\nConsider the function \\(f(x) = 4 x^3 + 3 x^2 + 5\\). For what values of \\(k\\) does the Intermediate Value Theorem tell us that there is a \\(c\\) in the interval \\([0,1]\\) such that \\(f(c) = k\\)?\n', 'problem_8': '**Problem 8.** (1 point)\n\nIf \\(\\displaystyle{\\lim_{x\\rightarrow a} f(x)=0}\\) and \n\\(\\displaystyle{\\lim_{x\\rightarrow a} g(x)=0}\\), then \n\\(\\displaystyle{\\lim_{x\\rightarrow a} \\frac{f(x)}{g(x)}}\\)\n \n\n*   A. is equal to one. \n*   B. is equal to \\(\\infty\\). \n*   C. must exist. \n*   D. does not exist. \n*   E. cannot be determined because there is not enough information. \n\n\nIn the answer box below, explain your reasoning for the choice you made above. \n\nUse complete sentences and correct grammar, \nspelling, and punctuation. Be specific and \ndetailed. Write as if you were explaining the \nanswer to someone else in class. \n\n\n[Space for answer]\n', 'problem_9': '**Problem 9.** *(1 point)*\n\nEvaluate the following limits without using a calculator. Enter *DNE* if the limit does not exist.\n\n(a) \\(\\displaystyle \\lim_{x \\to - 1^{+}} (x+6) \\frac{|x+1|}{x+1} =\\)\n'}, 'Derivatives': {'problem_1': '**Problem 1.** (1 point)\n\nSuppose that \\(f (x) = x^2\\) for all numbers \\(x\\). \n\nDetermine what\n  \\(\\dfrac{f (p) - 7744}{p - 88}\\)\n  \n  \n  \n  approaches as \\(p\\) approaches 88. \n\n2\\(\times\\)\\mbox{\\parbox[t]{5ex}{\n\n---\n', 'problem_10': "**Problem 10.** (1 point)  (setIntroduction_to_Derivative/Intro_to_derivative_problem_14.pg)\n\n**Problem**\n\nSuppose that \\(n\\) is a positive integer and \\(f (x) = \x0crac {1}{x^{1/n}}\\) for all numbers \\(x>0\\).\n\nFind \\(f ' (x)\\).\n  \n  \n  \n  .\n\n\\(\x0crac {-1}{nx^{?/n}}\\)\nwhere ? =\n\n---\n", 'problem_11': "**Problem 11.** (1 point)  (Problem source: *setIntroduction_to_Derivative/Intro_to_derivative_problem_15.pg*)\n\n***\n\n**Midterm Exam Problem (Answer with steps is required on note book)**\n\n**Problem**\n\nSuppose that each of \\(g\\) and \\(h\\) is a function with domain all numbers and \\(f\\) is the function so that \\(f (x) = g (x) + h (x)\\). Suppose also that each of \\(g\\) and \\(h\\) has domain all numbers.\n\nShow that \\(f' (x) = g' (x) + h' (x)\\) for all numbers \\(x\\).\n\nHINT: USE Derivative by definition\n\nEnter 99 when done.\n\n---\n", 'problem_12': "**Problem 12.** (1 point)\n\nProblem\n\nSuppose that each of \\(g\\) and \\(h\\) is a function with domain all numbers and \\(f\\) is the function so that \\(f (x) = g (x) - h (x)\\). Suppose also that each of \\(g\\) and \\(h\\) has domain all numbers.\n\nShow that \\(f' (x) = g' (x) - h' (x)\\) for all numbers \\(x\\).\n\nHINT: USE Derivative by definition\n\nEnter 99 when done.\n\n---\n", 'problem_13': "**Problem 13.** (1 point)\n\nSuppose that \\(f (x) = (x + 1) (x - 1)\\) for all numbers \\(x\\).\n\nFind \\(f'(x) =\\)\n\n---\n", 'problem_14': "**Problem 14.** (1 point)\n\nProblem\n\nSuppose that \\(f (x) = (x^2 + x + 1) (x^3 + x^2 + x + 1)\\) for all numbers\n\\(x\\).\n\nFind \\(f'(x)\\)\n\n\\(f'(x)=\\)\n\n---\n", 'problem_15': '**Problem 15.** (1 point) setIntroduction_to_Derivative/Intro_to_derivative_problem_19.pg\n\n**Problem**\n\nConsider the function \\(f (x) = |x|\\) for all \\(x\\).\n\n\\(\\lim_{x \nightarrow 0^-} \x0crac{f (x) - f (0)}{x - 0}  =\\)\n\n---\n', 'problem_2': '**Problem 2.** (1 point)\n\nSuppose that \\(f (x) = \\dfrac{1}{x}\\) for all numbers \\(x \neq 0\\).\n\nDetermine what\n  \\(\\dfrac{f (p) - 0.02}{p - 50}\\)\n\napproaches as \\(p\\) approaches 50.\n\n\\(\\dfrac{-1}{?}\\) where \\(?=\\)\n\n---\n', 'problem_3': '**Problem 3.** (1 point) *setIntroduction_to_Derivative/Intro_to_derivative_problem_6.pg*\n\n**Problem**\n\nSuppose that \\(f (x) = \\dfrac{1}{x^2}\\) for all numbers \\(x \neq 0\\).\n\nDetermine what\n  \\(\\dfrac{f (p) - 0.000260145681581686}{p - 62}\\)\n  \n  \n  \n  approaches as \\(p\\) approaches 62.\n\n\\(\\dfrac {-2}{?}\\) where \\(?=\\)\n\n---\n', 'problem_4': '**Problem 4.** (1 point) \\path|setIntroduction_to_Derivative/Intro_to_derivative_problem_7.pg|\n\n**Problem**\n\nSuppose that \\(f (x) = x^{1/2}\\) for all numbers \\(x > 0\\).\n\nDetermine what\n  \\(\x0crac{f (p) - 4.58257569495584 }{p - 21}\\)\n  \n  \n  \n  approaches as \\(p\\) approaches 21.\n\n\\(\\dfrac{1}{2\\sqrt{ ? }}\\) where  \\(?=\\) \\mbox{\\parbox[t]{3ex}{}}\n\n---\n', 'problem_5': '**Problem 5.** (1 point) *setIntroduction_to_Derivative/Intro_to_derivative_problem_8.pg*\n\n**Problem**\n\nSuppose that \\(f (x) = x^{1/3}\\) for all numbers \\(x > 0\\).\n\nDetermine what\n  \\(\x0crac{f (p) - 4.23582358425489}{p - 76}\\)\n  \n  \n  \n  approaches as \\(p\\) approaches 76.\n\n \n\\(\\dfrac {1} {3*76^?}\\)\n\nwhere?=\n', 'problem_6': '**Problem 6.** (1 point) (Problem source: setIntroduction_to_Derivative/Intro_to_derivative_problem_9.pg)\n\n***\n\n**Problem**\n\nSuppose that \\(f(x) = x^{2/3}\\) for all numbers \\(x > 0\\).\n\nDetermine what\n\n  \\[\\dfrac{f(p) - 8.08757939909006}{p - 23}\\]\n\napproaches as \\(p\\) approaches 23.\n\n\\[\\dfrac {2} {3*23^?}\\]\n\nwhere ? =  \n\n---\n', 'problem_7': '**Problem 7.** (1 point)\n\n**Problem**\n\nSuppose that \\(f (x) = \x0crac {1}{x^{1/2}}\\) for all numbers \\(x > 0\\).\n\nDetermine what\n  \\(\x0crac{f (p) - 0.113960576459638}{p - 77}\\)\n  \n  \n  \n  approaches as \\(p\\) approaches 77.\n\n \n\\(\x0crac {-1} { 2 \times 77^?}\\)\n\n where?=\n\n---\n', 'problem_8': '**Problem 8.** (1 point)\n\nSuppose that \\(f (x) = x^{n}\\) for all numbers \\(x\\).\n\nIf \\(a\\) is a number, determine what\n  \\(\x0crac{f (p) - f (a)}{p - a}\\)\n\napproaches as \\(p\\) approaches a.\n\n---\n', 'problem_9': '**Problem 9.** (1 point) *setIntroduction_to_Derivative/Intro_to_derivative_problem_13.pg*\n\n**Problem**\n\nSuppose that \\(n\\) is a positive integer and \\(f (x) = {x^{1/n}}\\) for all numbers \\(x\\).\n\nif \\(a> 0\\) is a number, determine what\n  \\(\x0crac{f (p) - f (a)}{p - a}\\)\n  \n  \n  \n  approaches as \\(p\\) approaches a.\n\n\\(\x0crac {1}{na^{?/n}}\\)\n where ? =\n\n---\n'}}

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
