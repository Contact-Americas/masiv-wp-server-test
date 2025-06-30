from abc import ABC, abstractmethod
from typing import List
from schemas.message import MessageCreate

class MessagePort(ABC):
    @abstractmethod
    def create_messages(self, messages: List[MessageCreate]) -> int:
        """Crea múltiples mensajes en la base de datos"""
        pass
