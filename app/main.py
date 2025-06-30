from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from typing import List
from database import engine, DATABASE_URL, get_session
from models.message import Message
from utils.wait_for_db import wait_for_db_connection
from schemas.message import MessageCreate
from adapters.message_repository import MessageRepository
from services.message_service import MessageService
from tasks.send_message import send_whatsapp_message
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O reemplaza "*" por ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    wait_for_db_connection(DATABASE_URL)
    SQLModel.metadata.create_all(engine)

@app.post("/messages/bulk")
def create_bulk_messages(
    messages: List[MessageCreate],
    session: Session = Depends(get_session)
):
    repository = MessageRepository(session)
    service = MessageService(repository)
    count = service.bulk_insert(messages)
    return {"inserted": count}


@app.post("/messages/send-pending")
def send_pending_messages(session: Session = Depends(get_session)):
    repository = MessageRepository(session)
    pending_messages = repository.get_pending_messages()

    results = []
    for msg in pending_messages:
        status, response = send_whatsapp_message(msg.phone_number, msg.content)

        if status == 200:
            msg.status = "sent"
        else:
            msg.status = "failed"

        session.add(msg)
        results.append({
            "id": msg.id,
            "status": msg.status,
            "response": response
        })

    session.commit()
    return {"results": results}