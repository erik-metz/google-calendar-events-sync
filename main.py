import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from db import update_google_events
from googleCalendar import (Google_Calendar_Event, get_google_events,
                            subscribe_to_google_calendar_push_notifications)

load_dotenv()

app = FastAPI()
subscribe_to_google_calendar_push_notifications()

@app.get('/')
async def root():
    return RedirectResponse(url=os.environ.get('REDIRECT_URL'))

# # Create a Pydantic model to define the expected data in the POST request
# class Item(BaseModel):
#     name: str
#     description: str = None

# # In-memory storage for demonstration purposes
# items = []

# # Define a POST endpoint to create an item
# @app.post('/items/', response_model=Item)
# async def create_item(item: Item):
#     items.append(item)
#     return item

# # Define a GET endpoint to retrieve all items (for testing)
# @app.get('/items/', response_model=List[Item])
# async def read_items():
#     return items



@app.get('/events/')
async def get_events():
    return await get_google_events()

# Define a POST endpoint to handle google calendar events
@app.post('/google-calendar-events-webhook/', response_model=Google_Calendar_Event)
async def webhook(event: Google_Calendar_Event):
    update_google_events(event)
    return event