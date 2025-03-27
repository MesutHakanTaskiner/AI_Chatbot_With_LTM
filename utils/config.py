from dotenv import load_dotenv
import os 

load_dotenv()

system_instruction = os.getenv("SYSTEM_INSTRUCTION")
API_KEY = os.getenv("API_KEY")