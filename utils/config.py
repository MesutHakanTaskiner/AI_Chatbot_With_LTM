"""
Configuration module for loading environment variables and setting up system configurations.

This module uses python-dotenv to load environment variables from a .env file.
It initializes global configurations such as system instructions and API keys required for the application.
"""

from dotenv import load_dotenv
import os 

# Load environment variables from a .env file into os.environ
load_dotenv()

# Global configuration for system instruction; used to initialize AiOperations
system_instruction = os.getenv("SYSTEM_INSTRUCTION")
# Alternative system instruction if needed for secondary purposes
system_instruction_2 = os.getenv("SYSTEM_INSTRUCTION_2")
# API key used for authentication with external services
API_KEY = os.getenv("API_KEY")

# Setting GEMINI_API_KEY environment variable for use in the application or external libraries
os.environ["GEMINI_API_KEY"] = API_KEY
