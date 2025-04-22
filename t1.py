# import re
# import os

# # The full input text (paste it directly here or read from a file)
# input_text = """
# **Problem 1.** (1 point)

# Suppose that \(f (x) = x^2\) for all numbers \(x\). 

# Determine what
#   \(\dfrac{f (p) - 7744}{p - 88}\)
  
  
  
#   approaches as \(p\) approaches 88. 

# 2\(\times\)\mbox{\parbox[t]{5ex}{

# ---
# **Problem 2.** (1 point)

# Suppose that \(f (x) = \dfrac{1}{x}\) for all numbers \(x \neq 0\).

# Determine what
#   \(\dfrac{f (p) - 0.02}{p - 50}\)

# approaches as \(p\) approaches 50.

# \(\dfrac{-1}{?}\) where \(?=\)

# ---
# **Problem 3.** (1 point) *setIntroduction_to_Derivative/Intro_to_derivative_problem_6.pg*

# **Problem**

# Suppose that \(f (x) = \dfrac{1}{x^2}\) for all numbers \(x \neq 0\).

# Determine what
#   \(\dfrac{f (p) - 0.000260145681581686}{p - 62}\)
  
  
  
#   approaches as \(p\) approaches 62.

# \(\dfrac {-2}{?}\) where \(?=\)

# ---
# **Problem 4.** (1 point) \path|setIntroduction_to_Derivative/Intro_to_derivative_problem_7.pg|

# **Problem**

# Suppose that \(f (x) = x^{1/2}\) for all numbers \(x > 0\).

# Determine what
#   \(\frac{f (p) - 4.58257569495584 }{p - 21}\)
  
  
  
#   approaches as \(p\) approaches 21.

# \(\dfrac{1}{2\sqrt{ ? }}\) where  \(?=\) \mbox{\parbox[t]{3ex}{}}

# ---
# **Problem 5.** (1 point) *setIntroduction_to_Derivative/Intro_to_derivative_problem_8.pg*

# **Problem**

# Suppose that \(f (x) = x^{1/3}\) for all numbers \(x > 0\).

# Determine what
#   \(\frac{f (p) - 4.23582358425489}{p - 76}\)
  
  
  
#   approaches as \(p\) approaches 76.

 
# \(\dfrac {1} {3*76^?}\)

# where?=

# ---
# Okay, here's the re-formatted version of the LaTeX problem, aiming for increased readability:

# **Problem 6.** (1 point) (Problem source: setIntroduction_to_Derivative/Intro_to_derivative_problem_9.pg)

# ***

# **Problem**

# Suppose that \(f(x) = x^{2/3}\) for all numbers \(x > 0\).

# Determine what

#   \[\dfrac{f(p) - 8.08757939909006}{p - 23}\]

# approaches as \(p\) approaches 23.

# \[\dfrac {2} {3*23^?}\]

# where ? =  

# ---
# **Problem 7.** (1 point)

# **Problem**

# Suppose that \(f (x) = \frac {1}{x^{1/2}}\) for all numbers \(x > 0\).

# Determine what
#   \(\frac{f (p) - 0.113960576459638}{p - 77}\)
  
  
  
#   approaches as \(p\) approaches 77.

 
# \(\frac {-1} { 2 \times 77^?}\)

#  where?=

# ---
# **Problem 8.** (1 point)

# Suppose that \(f (x) = x^{n}\) for all numbers \(x\).

# If \(a\) is a number, determine what
#   \(\frac{f (p) - f (a)}{p - a}\)

# approaches as \(p\) approaches a.

# ---
# **Problem 9.** (1 point) *setIntroduction_to_Derivative/Intro_to_derivative_problem_13.pg*

# **Problem**

# Suppose that \(n\) is a positive integer and \(f (x) = {x^{1/n}}\) for all numbers \(x\).

# if \(a> 0\) is a number, determine what
#   \(\frac{f (p) - f (a)}{p - a}\)
  
  
  
#   approaches as \(p\) approaches a.

# \(\frac {1}{na^{?/n}}\)
#  where ? =

# ---
# **Problem 10.** (1 point)  (setIntroduction_to_Derivative/Intro_to_derivative_problem_14.pg)

# **Problem**

# Suppose that \(n\) is a positive integer and \(f (x) = \frac {1}{x^{1/n}}\) for all numbers \(x>0\).

# Find \(f ' (x)\).
  
  
  
#   .

# \(\frac {-1}{nx^{?/n}}\)
# where ? =

# ---
# **Problem 11.** (1 point)  (Problem source: *setIntroduction_to_Derivative/Intro_to_derivative_problem_15.pg*)

# ***

# **Midterm Exam Problem (Answer with steps is required on note book)**

# **Problem**

# Suppose that each of \(g\) and \(h\) is a function with domain all numbers and \(f\) is the function so that \(f (x) = g (x) + h (x)\). Suppose also that each of \(g\) and \(h\) has domain all numbers.

# Show that \(f' (x) = g' (x) + h' (x)\) for all numbers \(x\).

# HINT: USE Derivative by definition

# Enter 99 when done.

# ---
# **Problem 12.** (1 point)

# Problem

# Suppose that each of \(g\) and \(h\) is a function with domain all numbers and \(f\) is the function so that \(f (x) = g (x) - h (x)\). Suppose also that each of \(g\) and \(h\) has domain all numbers.

# Show that \(f' (x) = g' (x) - h' (x)\) for all numbers \(x\).

# HINT: USE Derivative by definition

# Enter 99 when done.

# ---
# **Problem 13.** (1 point)

# Suppose that \(f (x) = (x + 1) (x - 1)\) for all numbers \(x\).

# Find \(f'(x) =\)

# ---
# **Problem 14.** (1 point)

# Problem

# Suppose that \(f (x) = (x^2 + x + 1) (x^3 + x^2 + x + 1)\) for all numbers
# \(x\).

# Find \(f'(x)\)

# \(f'(x)=\)

# ---
# **Problem 15.** (1 point) setIntroduction_to_Derivative/Intro_to_derivative_problem_19.pg

# **Problem**

# Consider the function \(f (x) = |x|\) for all \(x\).

# \(\lim_{x \rightarrow 0^-} \frac{f (x) - f (0)}{x - 0}  =\)

# ---
# """

# # Use regex to split the text into problems and capture the problem number
# pattern = re.compile(r"\*\*Problem (\d+)\.\*\*")
# splits = pattern.split(input_text)

# # Create a folder to store the problem files
# os.makedirs("problems", exist_ok=True)

# # Iterate through the split content and write to separate files
# for i in range(1, len(splits), 2):
#     problem_number = splits[i]
#     problem_content = "**Problem " + problem_number + ".**" + splits[i + 1]
#     filename = f"problem_sets/Derivatives/problem_{problem_number}.txt"
    
#     with open(filename, "w", encoding="utf-8") as f:
#         f.write(problem_content)

# print("All problems written to individual files in the 'problems/' folder.")


# import streamlit as st

# from utils import render_text_with_latex

# current_problem = """\[H(x) = \begin{cases}
# {0} & \text{ if }  x \leq 0   \\
#  {1} & \text{ if }  x > 0.  
#              \end{cases}\]"""

# # st.markdown(f'<div class="gray-expander">', unsafe_allow_html=True)
# # render_text_with_latex(current_problem)
# # st.markdown("</div>", unsafe_allow_html=True)

# st.latex(r"""H(x) = \begin{cases}
# {0} & \text{ if }  x \leq 0   \\
#  {1} & \text{ if }  x > 0.  
#              \end{cases}\]""")

# import streamlit as st

# st.latex(r'''
# "\n\n**Problem**\n\nA function \\(f\\) is continuous at \\(a\\) if all of the following hold:\n\n1) \\(f(a)\\) exists\n2) \\(\\lim_{x \\rightarrow a} f(x)\\) exists\n3) \\(\\lim_{x \\rightarrow a} f(x) = f(a)\\)\n\nThe function is not continuous at \\(a\\) if any one of the conditions fails to hold.\n\nConsider the function \\(f\\) defined by\n\n\\[f(x) = \\begin{cases}\n0 & \\text{if } x \\leq 0 \\\\\n x^2 & \\text{if } x > 0\n\\end{cases}\\]\n\n..."
# ''')


# r'''
# f(x) = 
# \begin{cases}
# 0 & \text{if } x \leq 0 \\
# x^2 & \text{if } x > 0
# \end{cases}
# '''

import streamlit as st

# st.latex(r'''
# f(x) = \begin{cases}
# 0 & \text{if } x \leq 0 \\
# x^2 & \text{if } x > 0
# \end{cases}
# ''')

st.write(r"""
$$
\\text{Annual Cost} = \left(\frac{\text{Miles per Year}}{\text{Fuel Efficiency}}\right) \times \text{Price per Gallon}
$$
""")
st.write("""
$$
\\text{Annual Cost} = \\left(\\frac{\\text{Miles per Year}}{\\text{Fuel Efficiency}}\\right) \\times \\text{Price per Gallon}
$$
""")