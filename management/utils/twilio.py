import json
import logging
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from twilio.rest import Client
from supermarket.settings import OTP_TWILIO_FROM, OTP_TWILIO_ACCOUNT, OTP_TWILIO_AUTH

class MessageClient:
    def __init__(self):
        self.twilio_number = OTP_TWILIO_FROM
        self.twilio_client = Client(OTP_TWILIO_ACCOUNT, OTP_TWILIO_AUTH)

    def send_message(self, body, to):
        self.twilio_client.messages.create(
            body=body,
            to=to,
            from_=self.twilio_number,
        )