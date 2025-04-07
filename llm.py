from google import genai

client = genai.Client(api_key="AIzaSyBjPiyQYO_c1t5Aexpw0qkeVatbr5o-jjM")

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