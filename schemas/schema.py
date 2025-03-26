from pydantic import BaseModel, Field
from typing import List


class CriticInfo(BaseModel):
    name: List[str]
    dates: List[str]
    preferences: List[str]
    personal: List[str]
    goals: List[str]
    special_details: List[str]

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