from typing import List
from schemas.message import MessageCreate
from tasks.send_message import send_whatsapp_message
from ports.message_port import MessagePort

class MessageService:
    def __init__(self, repository: MessagePort):
        self.repository = repository

    def bulk_insert(self, messages: List[MessageCreate]) -> int:
        count = self.repository.create_messages(messages)
        for m in messages:
            send_whatsapp_message(m.phone_number, m.content)
        return count
