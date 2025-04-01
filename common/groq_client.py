# common/groq_client.py
import os
from groq import Groq
from django.conf import settings


def get_groq_client():
    return Groq(api_key=settings.GROQ_API_KEY)
