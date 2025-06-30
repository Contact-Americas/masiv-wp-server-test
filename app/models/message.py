from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str
    content: str
    status: str = Field(default="pending")
    response: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None