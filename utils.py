import streamlit as st
import re

def render_text_with_latex(content):
    content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)
    st.markdown(content)