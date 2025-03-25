import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

GOOGLE_API_KEY = os.getenv("API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

class AiOperations:
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.messages_thread: Dict[str, List[str]] = {}

    def get_answer(self, question: str, session_id: str) -> str:
        if not session_id:
            return "Session ID is required"
        if session_id not in self.messages_thread:
            self.messages_thread[session_id] = []
        self.messages_thread[session_id].append(question)
        response = self.llm.invoke(self.messages_thread[session_id])
        self.messages_thread[session_id].append(response)
        return str(response.content)

    def delete_session_thread(self, session_id: str) -> None:
        self.messages_thread.pop(session_id, None)

    def set_system_instruction(self, session_id: str, instruction: str) -> str:
        """
        Sets a system instruction for the given session by resetting the message thread with
        the provided system prompt.
        """
        self.messages_thread[session_id] = [f"system: {instruction}"]
        return f"System instruction set for session {session_id}"
