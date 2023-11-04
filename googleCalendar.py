import json
import os
from datetime import datetime
from typing import List
from uuid import uuid4

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel

load_dotenv()

class GoogleEvent(BaseModel):
    id: str
    summary: str
    description: str
    startDateTime: datetime
    endDateTime: datetime

def load_credentials_from_env():
    credentials_json = os.getenv('GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY')
    if not credentials_json:
        raise ValueError('GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY environment variable is not set.')
    
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(credentials_json),
        scopes=['https://www.googleapis.com/auth/calendar'],
    )
    return credentials

def subscribe_to_google_calendar_push_notifications():
    credentials = load_credentials_from_env()
    calendar_api = build('calendar', 'v3', credentials=credentials)
    
    base_url = os.getenv('BASE_URL')
    if not base_url:
        raise ValueError('BASE_URL environment variable is not set.')
    
    webhook_url = f'{base_url}/google-calendar-events-webhook'

    event = {
        'id': uuid4().hex,
        'type': 'web_hook',
        'address': webhook_url
    }

    try:
        calendar_api.events().watch(
            calendarId=os.getenv('GOOGLE_CLOUD_CALENDAR_ID', 'primary'),
            body=event,
        )
        print(f'Event notifications set up successfully at: {event} calendarId={os.getenv("GOOGLE_CLOUD_CALENDAR_ID", "primary")}')
    except HttpError as error:
        print(f'Error setting up event notifications: {error}')
