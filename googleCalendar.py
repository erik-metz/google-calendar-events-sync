import json
import os
from datetime import datetime, timedelta
from typing import Dict
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import HTTPException
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

class Google_Calendar_Event(BaseModel):
    address: str
    expiration: str
    id: str
    kind: str
    params: Dict[str, str]
    payload: bool
    resourceId: str
    resourceUri: str
    token: str
    type: str

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


async def get_google_events():
    credentials = load_credentials_from_env()
    calendar_api = build('calendar', 'v3', credentials=credentials)


    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
    max_date = tomorrow + timedelta(days=14)

    params = {
        'calendarId': os.getenv('GOOGLE_CLOUD_CALENDAR_ID', 'primary'),
        'timeMin': today.isoformat() + 'Z',
        'timeMax': max_date.isoformat() + 'Z'
    }
    
    try:
        events_result = calendar_api.events().list(**params).execute() 
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        return events_result 
    except Exception as e:
        print(f'An error occurred: {e}')
        raise HTTPException(status_code=501, detail='Please try again later')
