import re
from google import genai

client = genai.Client(api_key="AIzaSyBjPiyQYO_c1t5Aexpw0qkeVatbr5o-jjM")

def stream_response(prompt, question_text):
    full_prompt = f"""Assume you are a teacher guiding a confused student toward the answer.
- If the student mentions the right answer, then respond with BINGO! You found the correct answer.
- You must not directly provide the answer but help them find the right approach.
- If the student is headed in the right direction, then tell them that they are correct.

The question:
{question_text}

Student's prompt:
{prompt}"""
    response_stream = client.models.generate_content_stream(
        model="gemini-2.0-flash", contents=[full_prompt]
    )
    for chunk in response_stream:
        if chunk.text:
            content = re.sub(r'\\\((.*?)\\\)', r'$\1$', chunk.text)
            yield content
            # yield chunk.text
