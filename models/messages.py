from pydantic import BaseModel, Field

class OutboundMessage(BaseModel):
    sender : str = Field(min_length=1)
    to : str = Field(min_length=1)
    message : str = Field(min_length=1)
    require_user_input: bool 
     
