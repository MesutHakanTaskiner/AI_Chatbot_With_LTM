import os
from typing import List, Dict
from utils.config import system_instruction
from mem0 import Memory
from litellm import completion
from schemas.schema import ResponseSchema
from langchain.output_parsers import PydanticOutputParser

output_parser = PydanticOutputParser(pydantic_object=ResponseSchema)

class AiOperations:
    # Initializes AiOperations by setting up the language model and message threads.
    def __init__(self) -> None:
        self.messages_thread: Dict[str, List[str]] = {}
        self.system_instruction = system_instruction
        self.user_instruction = ""
        self.memory: List[str] = []

    # Processes the question using the language model and manages the session's message thread.
    def get_answer(self, question: str, session_id: str, user_id: str = "default_user") -> str:
        if len(self.memory) == 0:
            config = {
                "llm": {
                    "provider": "litellm",
                    "config": {
                        "model": "gemini/gemini-2.0-flash",
                        "temperature": 0.2,
                        "max_tokens": 1500,
                    }
                },
                "embedder": {
                    "provider": "gemini",
                    "config": {
                        "model": "models/text-embedding-004",
                    }
                },
                "vector_store": {
                    "provider": "qdrant",
                    "config": {
                        "embedding_model_dims": 768,
                        "path": os.getcwd() + "/qdrant",
                    }
                },
                "history_db_path": "history.db"
            }

            self.memory.append(Memory.from_config(config))
            memory = self.memory[0]
        else:
            memory = self.memory[0]


        first_time = False
        context = ""
        if not session_id:
            return "Session ID is required"
        if session_id not in self.messages_thread:
            self.messages_thread[session_id] = []
            self.messages_thread[session_id].append({"role": "system", "content": self.system_instruction})
            first_time = True

        relevant_memories = memory.search(query=question, user_id=user_id, limit=3)
        memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
        print(f"Relevant memories: {relevant_memories}")
        print(f"Memories string: {memories_str}")

        print(f"First time: {self.messages_thread[session_id]}")
        try:
            prompt = f"{question}\n\n {output_parser.get_format_instructions()} \n\n User Memories:\n{memories_str}" 

            print(f"Prompt: {prompt}")

            self.messages_thread[session_id].append({"role": "user", "content": prompt})
            response = completion(model="gemini/gemini-2.0-flash", messages=self.messages_thread[session_id])
            self.messages_thread[session_id].append({"role": "assistant", "content": response.choices[0].message.content})

            try:
                # Parse the output
                parsed_response = output_parser.parse(response.choices[0].message.content)
            except Exception as e:
                print(f"Parsing error: {e}")
            

            if first_time:
                context = parsed_response.format_LTM()[1]

            print(f"Response: {parsed_response.format_LTM()[0]}")
            print(f"Context: {parsed_response.format_LTM()[1]}")

            memory.add(self.messages_thread[session_id], user_id=user_id)

        except Exception as e:
            print(f"An error occurred: {e}")
    
        return (str(parsed_response.format_LTM()[0]), context)

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
        data = get_ltm_data_from_db()
        return data

    # Updates memory for a given key with a new value.
    def update_memory(self, data):
        is_succes = update_ltm_data(data)
        if is_succes:
            return "Memory updated successfully"
        return "Memory not found"

    # Deletes memory for a given key.
    def delete_memory(self, data):
        is_success = delete_ltm_data(data)

        if is_success:
            return "Memory deleted successfully"
        return "Memory not found"
    
    def agent_response(self, response: str) -> str:
        print("Agent response", response)
