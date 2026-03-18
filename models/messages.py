from pydantic import BaseModel, Field

class Message(BaseModel):
    sender : str = Field(min_length=1)
    to : str = Field(min_length=1)
    content : str = Field(min_length=1)

class OutboundMessage(Message):
    require_user_input: bool = Field(default=False)

class InboundMessage(Message):
    pass
     
