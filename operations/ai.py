import os
from typing import List, Dict, Tuple
from utils.config import system_instruction
from mem0 import Memory
from litellm import completion
from schemas.schema import ResponseSchema
from langchain.output_parsers import PydanticOutputParser
from operations.memory import get_memories, update_memory, delete_memory
from utils.config import config

output_parser = PydanticOutputParser(pydantic_object=ResponseSchema)

class AiOperations:
    """
    Class to handle AI operations including generating answers,
    managing session messages, updating system instructions, and memory handling.
    """
    def __init__(self) -> None:
        """
        Initializes the AiOperations instance.
        
        - Sets up a dictionary for tracking message threads per session.
        - Loads system instructions from configuration.
        - Initializes an empty user instruction.
        - Prepares an empty list to store Memory object(s).
        """
        self.messages_thread: Dict[str, List[str]] = {}
        self.system_instruction = system_instruction
        self.user_instruction = ""
        
        self.memory = Memory.from_config(config)
            
    def get_answer(self, question: str, session_id: str, user_id: str = "default_user") -> Tuple[str, str]:
        """
        Processes a user's question and generates an answer using the language model.
        
        Steps:
        1. If no Memory object exists, create one using a predefined configuration.
        2. Validate the session_id and initialize a session thread if necessary.
        3. Retrieve relevant memories based on the question to add context.
        4. Construct a prompt that includes the question, formatting instructions, and user memories.
        5. Send the prompt to the language model and append both user and assistant messages to the session thread.
        6. Attempt to parse the assistant's response for extracting formatted answers and context.
        7. If this is the first message of the session, extract additional context.
        8. Add the complete message thread to the Memory object for future context retrieval.
        
        Parameters:
        - question (str): The user's question.
        - session_id (str): Identifier for the current session.
        - user_id (str): Identifier for the user (default is "default_user").
        
        Returns:
        - tuple: Contains the assistant's response as a string and an optional context string.
        """
        first_time = False
        context = ""
        if not session_id:
            return ("Session ID is required", "")
        if session_id not in self.messages_thread:
            self.messages_thread[session_id] = []
            # Start a new session with the initial system and user instructions.
            self.messages_thread[session_id].append({"role": "system", "content": self.system_instruction + "\n\n" + self.user_instruction})
            first_time = True

        relevant_memories = self.memory.search(query=question, user_id=user_id, limit=3)
        memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
        try:
            prompt = f"{question}\n\n {output_parser.get_format_instructions()} \n\n User Memories:\n{memories_str}"
            #print(f"Prompt: {prompt}")
            self.messages_thread[session_id].append({"role": "user", "content": prompt})
            response = completion(model="gemini/gemini-2.0-flash", messages=self.messages_thread[session_id])
            self.messages_thread[session_id].append({"role": "assistant", "content": response.choices[0].message.content})
            try:
                # Attempt to parse the model's output.
                parsed_response = output_parser.parse(response.choices[0].message.content)
            except Exception as e:
                print(f"Parsing error: {e}")
                parsed_response = type('DefaultResponse', (), {"format_LTM": lambda: (response.choices[0].message.content, "")})()
            if first_time:
                context = parsed_response.format_LTM()[1]
            # Store the conversation history in memory.
            self.memory.add(self.messages_thread[session_id], user_id=user_id)
        except Exception as e:
            print(f"An error occurred: {e}")
        return (str(parsed_response.format_LTM()[0]), context)

    def delete_session_thread(self, session_id: str) -> None:
        """
        Deletes the message thread for a given session.
        
        Parameters:
        - session_id (str): The identifier of the session to be deleted.
        """
        self.messages_thread.pop(session_id, None)

    def set_system_instruction(self, instruction: str) -> str:
        """
        Appends a new instruction to the existing system instruction and updates the user instruction.
        
        Parameters:
        - instruction (str): The new instruction to add.
        
        Returns:
        - str: The updated system instruction.
        """
        self.system_instruction = self.system_instruction + "\n\n" + instruction 
        self.user_instruction = instruction
        return self.system_instruction

    def get_system_instruction(self) -> str:
        """
        Retrieves the current user-specific system instruction.
        
        Returns:
        - str: The current user instruction.
        """
        return self.user_instruction

    def get_memory(self) -> Dict[str, str]:
        """
        Retrieves stored memory data.
        
        Iterates through memory results and collects memory texts.
        
        Returns:
        - list: A list of memory strings.
        """
        raw_data = get_memories(self.memory)
        data = []
        try:
            for i in raw_data["results"]:
                data.append(i["memory"])
        except Exception as e:
            print(f"Error retrieving memory: {e}")
            return {}
        return data

    def update_memory(self, update_data):
        """
        Updates a memory entry with new information.
        
        Parameters:
        - update_data (dict): A dictionary containing 'old_value' and 'new_value' keys for updating memory.
        
        Returns:
        - str: A message indicating success or failure of the memory update.
        """
        is_success = update_memory(self.memory, update_data)
        return is_success

    def delete_memory(self, delete_data):
        """
        Deletes a memory entry based on provided criteria.
        
        Parameters:
        - delete_data (dict): A dictionary containing the memory value to be deleted.
        
        Returns:
        - str: A message indicating the result of the deletion operation.
        """
        is_success = delete_memory(self.memory, delete_data)
        return is_success
