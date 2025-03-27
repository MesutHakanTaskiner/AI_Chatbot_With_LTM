from pydantic import BaseModel, Field
from typing import List, Dict


class CriticalInfo(BaseModel):
    name: Dict[str, str]                      # Name of the user (first name, last name etc.)
    dates: Dict[str, str]                     # Dates (birth date, anniversary date etc.)
    profession: Dict[str, str]                # Profession of the user (doctor, engineer etc.)
    location: Dict[str, str]                  # Location of the user (city, country etc.)
    education: Dict[str, str]                 # Education of the user (school, college, university etc.)
    personal_details: Dict[str, str]          # More personal details of the user (hobbies, interests etc.)
    goals: Dict[str, str]                     # Goals of the user (career goals, personal goals etc.)
    special_details: Dict[str, str]           # Special details of the user (medical conditions, etc.)
    social_info: Dict[str, str]               # Social information of the user (social media handles etc.)
    additional_info: Dict[str, str]           # Additional information about the user
    


class ContextAndLTMScores(BaseModel):
    context: str

class LTMInformations(BaseModel):
    critical_informations: CriticalInfo

class ResponseSchema(BaseModel):
    response: str = Field(description="Response from the language model")
    ltm_informations: LTMInformations = Field(description="LTM information")
    context: str = Field(description="Context of the conversation")

    def format_LTM(self) -> str:
        memory = self.ltm_informations.critical_informations
        return (
            self.response, memory, self.context
        )