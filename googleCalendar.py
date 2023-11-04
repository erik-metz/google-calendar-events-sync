import json
import os
from datetime import datetime
from typing import List
from uuid import uuid4

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel

load_dotenv()


def load_credentials_from_env():
    credentials_json = os.getenv('GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY')
    if not credentials_json:
        raise ValueError("GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY environment variable is not set.")
    
    credentials = json.loads(credentials_json)
    return credentials

# Create a Pydantic model for the GoogleEvent data
class GoogleEvent(BaseModel):
    id: str
    summary: str
    description: str
    startDateTime: datetime
    endDateTime: datetime


def subscribe_to_google_calendar_push_notifications():
    calendar_api = build('calendar', 'v3', credentials=load_credentials_from_env())
    webhook_url = f'{os.environ.get("BASE_URL")}/api/calendar-webhook'

    event = {
        'id': uuid4().hex,
        'type': 'web_hook',
        'address': webhook_url
    }

    def handle_notification_response(request_id, response, exception):
        if exception is not None:
            print(f'Error setting up event notifications: {exception}')
        else:
            print(f'Event notifications set up successfully: {response}')


    try:
        calendar_api.events().watch(
            calendarId='primary',  # Calendar ID
            body=event,
            callback=handle_notification_response
        )
    except HttpError as error:
        print(f'Error setting up event notifications: {error}')


# The rest of your code remains unchanged
