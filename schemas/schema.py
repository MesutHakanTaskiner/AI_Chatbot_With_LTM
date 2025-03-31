from pydantic import BaseModel, Field
from typing import List, Dict


class ContextAndLTMScores(BaseModel):
    context: str

class ResponseSchema(BaseModel):
    response: str = Field(description="Response from the language model")
    context: str = Field(description="Context of the conversation")

    def format_LTM(self) -> str:
        return (
            self.response, self.context
        )