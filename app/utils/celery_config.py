from celery import Celery

celery_app = Celery(
    "whatsapp_sender",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.task_routes = {
    "tasks.send_message_task": {"queue": "whatsapp_queue"},
}
