from celery import shared_task

from .utils import send


@shared_task
def send_a_message_to_email(user_email: str, user_name: str) -> None:
    send(user_email, user_name)
