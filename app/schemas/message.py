from pydantic import BaseModel

class MessageCreate(BaseModel):
    phone_number: str
    content: str