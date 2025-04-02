from pydantic import BaseModel, Field
from typing import List, Dict, Optional


# ResponseSchema defines the structure of responses returned by the AI language model.
# It includes both the main response and any supplementary context.
class ResponseSchema(BaseModel):
    # Main response from the language model.
    response: str = Field(description="Response from the language model")
    # Additional context or metadata about the conversation.
    conversation_context_summary: Optional[str] = Field(description="Context of the conversation")

    def format_LTM(self) -> str:
        """
        Formats the stored response and context for further processing or retrieval.
        
        Returns:
            tuple: A tuple containing the response and context.
        """
        return (self.response, self.conversation_context_summary)
