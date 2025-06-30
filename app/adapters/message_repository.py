from sqlmodel import Session
from models.message import Message
from schemas.message import MessageCreate
from ports.message_port import MessagePort
from typing import List

class MessageRepository(MessagePort):
    def __init__(self, session: Session):
        self.session = session

    def create_messages(self, messages: List[MessageCreate]) -> int:
        db_messages = [
            Message(phone_number=m.phone_number, content=m.content)
            for m in messages
        ]
        self.session.add_all(db_messages)
        self.session.commit()
        return len(db_messages)
    
    
    def get_pending_messages(self):
        return self.session.query(Message).filter(Message.status == "pending").all()
