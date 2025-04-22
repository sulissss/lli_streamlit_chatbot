import re
from google import genai

client = genai.Client(api_key="AIzaSyBjPiyQYO_c1t5Aexpw0qkeVatbr5o-jjM")

def stream_response(prompt, question_text):
    full_prompt = f"""Assume you are a teacher guiding a confused student toward the answer. Your goal is to continue doing so until they arrive at the right solution.
- Go step by step guiding the student until they reach the correct answer. Mention if they're right or wrong at each step.
- At any step in the process (even if it's the start of the conversation) if the student gives the right answer, you should congratulate them by saying "BINGO! You found the correct answer." and conclude the conversation.

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
