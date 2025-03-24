import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", system_instruction="You are a cat. Your name is Neko.")

messages_thread = {}

def get_answer(question, session_id):
    if session_id is None:
        return "Session ID is required"
    
    if session_id not in messages_thread:
        messages_thread[session_id] = []

    messages_thread[session_id].append(question)

    response = llm.invoke(messages_thread[session_id])
    
    messages_thread[session_id].append(response)

    return str(response.content)

def delete_session_thread(session_id):
    messages_thread.pop(session_id, None)
