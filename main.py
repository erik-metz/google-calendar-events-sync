import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from db import update_google_events
from googleCalendar import (Google_Calendar_Event, get_google_events,
                            subscribe_to_google_calendar_push_notifications)

load_dotenv()

app = FastAPI()
notification_channel=subscribe_to_google_calendar_push_notifications()

@app.post('/google-calendar-events-webhook/', response_model=Google_Calendar_Event)
async def webhook(event: Google_Calendar_Event):
    update_google_events(event)
    return event

@app.get('/')
async def root():
    return RedirectResponse(url=os.environ.get('REDIRECT_URL'))

@app.get('/events/')
async def get_events():
    raise HTTPException(status_code=401)
    return await get_google_events()

