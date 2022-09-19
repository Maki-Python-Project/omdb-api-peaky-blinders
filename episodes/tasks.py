from rest_framework.response import Response
from rest_framework import status
from celery import shared_task

from .models import Episode


@shared_task()
def parse_data():
    pass
