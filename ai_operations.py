import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

GOOGLE_API_KEY = os.getenv("API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

system_instruction = os.getenv("SYSTEM_INSTRUCTION")

class AiOperations:
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.messages_thread: Dict[str, List[str]] = {}
        self.system_instruction = system_instruction
        self.user_instruction = ""

    def get_answer(self, question: str, session_id: str) -> str:
        if not session_id:
            return "Session ID is required"
        if session_id not in self.messages_thread:
            self.messages_thread[session_id] = []
            self.messages_thread[session_id].append(self.system_instruction)

        self.messages_thread[session_id].append(question)
        response = self.llm.invoke(self.messages_thread[session_id])
        self.messages_thread[session_id].append(response)
        return str(response.content)

    def delete_session_thread(self, session_id: str) -> None:
        self.messages_thread.pop(session_id, None)

    def set_system_instruction(self, instruction: str) -> str:
        """
        Sets a system instruction for the given session by resetting the message thread with
        the provided system prompt.
        """
        self.system_instruction = self.system_instruction + "\n\n" + instruction 
        self.user_instruction = instruction

    def get_system_instruction(self) -> str:
        return self.user_instruction