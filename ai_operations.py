import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", system_instruction="You are a cat. Your name is Neko.")

messages = []

import asyncio

def response(message):
    global messages
    response = llm.invoke(messages)
    messages.append(response)
    print(response)

while True:
    message = input("You: ")
    if message.lower() == "exit":
        break
    messages.append(message)
    response(message)
