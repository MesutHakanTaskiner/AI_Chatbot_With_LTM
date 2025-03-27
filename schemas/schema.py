from pydantic import BaseModel, Field
from typing import List


class CriticInfo(BaseModel):
    name: List[str]                      # Name of the user (first name, last name etc.)
    dates: List[str]                     # Dates (birth date, anniversary date etc.)
    profession: List[str]                # Profession of the user (doctor, engineer etc.)
    location: List[str]                  # Location of the user (city, country etc.)
    preferences: List[str]               # Preferences of the user (food, music, etc.)
    personal_details: List[str]          # More personal details of the user (hobbies, interests etc.)
    goals: List[str]                     # Goals of the user (career goals, personal goals etc.)
    special_details: List[str]           # Special details of the user (medical conditions, etc.)
    additional_info: List[str]           # Additional information about the user


class LTMInformations(BaseModel):
    critic_informations: CriticInfo

class ResponseSchema(BaseModel):
    response: str = Field(description="Response from the language model")
    ltm_informations: LTMInformations = Field(description="LTM information")

    def format_LTM(self) -> str:
        memory = self.ltm_informations.critic_informations
        return (
            self.response, memory
        )