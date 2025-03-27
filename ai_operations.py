import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from typing import List, Dict
from schemas.schema import ResponseSchema, CriticInfo, LTMInformations
from database.db import save_metadata, update_data
import json


load_dotenv()

API_KEY = os.getenv("API_KEY")
system_instruction = os.getenv("SYSTEM_INSTRUCTION")

output_parser = PydanticOutputParser(pydantic_object=ResponseSchema)


class AiOperations:
    # Initializes AiOperations by setting up the language model and message threads.
    def __init__(self) -> None:
        self.llm = GoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("API_KEY"),
            temperature=0.1
        )
        self.messages_thread: Dict[str, List[str]] = {}
        self.system_instruction = system_instruction
        self.user_instruction = ""

    # Processes the question using the language model and manages the session's message thread.
    def get_answer(self, question: str, session_id: str) -> str:
        if not session_id:
            return "Session ID is required"
        if session_id not in self.messages_thread:
            self.messages_thread[session_id] = []
            self.messages_thread[session_id].append(self.system_instruction)

        try:
            prompt = f"{question}\n\n {output_parser.get_format_instructions()}"
            self.messages_thread[session_id].append(prompt)
            output = self.llm.invoke(self.messages_thread[session_id])
            
            # Parse the output
            parsed_response = output_parser.parse(output)

            print(parsed_response.format_LTM()[0], parsed_response.format_LTM()[1])

            save_metadata(parsed_response.format_LTM()[1])
        except Exception as e:
            print(f"An error occurred: {e}")


        return str(parsed_response.format_LTM()[0])

    # Deletes the message thread associated with the given session id.
    def delete_session_thread(self, session_id: str) -> None:
        self.messages_thread.pop(session_id, None)

    # Updates the system instruction by appending the new instruction.
    def set_system_instruction(self, instruction: str) -> str:
        """
        Sets a system instruction for the given session by resetting the message thread with
        the provided system prompt.
        """
        self.system_instruction = self.system_instruction + "\n\n" + instruction 
        self.user_instruction = instruction

    # Retrieves the current system instruction set by the user.
    def get_system_instruction(self) -> str:
        return self.user_instruction
    
    # Retrieves the memory data.
    def get_memory(self) -> Dict[str, str]:
        return self.messages_thread
    