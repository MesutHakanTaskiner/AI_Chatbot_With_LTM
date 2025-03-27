from dotenv import load_dotenv
import os 

load_dotenv()

system_instruction = os.getenv("SYSTEM_INSTRUCTION")
system_instruction_2 = os.getenv("SYSTEM_INSTRUCTION_2")
API_KEY = os.getenv("API_KEY")
