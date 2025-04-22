import re
import os
from google import genai
from dotenv import load_dotenv

load_dotenv('.env')

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Context-aware Gemini chat functions

def create_chat():
    """Create a new Gemini chat object for context retention."""
    return client.chats.create(model="gemini-2.0-flash")

def get_chat_history(chat):
    """Return the chat history as a list of (role, text) tuples."""
    history = []
    for message in chat.get_history():
        role = message.role
        text = message.parts[0].text if message.parts else ""
        history.append((role, text))
    return history

def stream_response(prompt, question_text, chat=None):
    system_prompt = """
You are a supportive math tutor helping a student solve a homework problem. Your goal is to gently guide the student to the correct answer, confirming when they are on the right track and providing clear, actionable hints if they are not. Be encouraging and never leave the student confused or stuck in a loop.

Rules:
- If the student's answer or reasoning is correct, congratulate them and end the conversation with a clear confirmation (e.g., "Congratulations, that's correct! You solved it!"). Do not continue the conversation after this.
- If the student is on the right track, clearly affirm their approach and encourage them to continue.
- If the student is off track, kindly explain what is wrong and provide a helpful hint or next step.
- Never give circular or evasive responses. Always move the student closer to the solution.
- Never directly give away the answer unless the student has already found it.
- Use simple, clear language and a friendly tone.
"""
    # On first message, provide system prompt and question
    if chat is None:
        chat = create_chat()
        chat.send_message(system_prompt + f"\nThe question:\n{question_text}")
    # Send the user's message as part of the conversation
    response = chat.send_message_stream(prompt)
    for chunk in response:
        if chunk.text:
            content = re.sub(r'\\\((.*?)\\\)', r'$\1$', chunk.text)
            yield content