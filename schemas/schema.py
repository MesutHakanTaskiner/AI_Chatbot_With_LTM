from pydantic import BaseModel, Field
from typing import List, Dict

# This model is intended to represent contextual information along with long-term memory scores.
# Currently, it only contains a single field 'context', but can be extended as needed.
class ContextAndLTMScores(BaseModel):
    # A string holding additional context information.
    context: str

# ResponseSchema defines the structure of responses returned by the AI language model.
# It includes both the main response and any supplementary context.
class ResponseSchema(BaseModel):
    # Main response from the language model.
    response: str = Field(description="Response from the language model")
    # Additional context or metadata about the conversation.
    context: str = Field(description="Context of the conversation")

    def format_LTM(self) -> str:
        """
        Formats the stored response and context for further processing or retrieval.
        
        Returns:
            tuple: A tuple containing the response and context.
        """
        return (self.response, self.context)
