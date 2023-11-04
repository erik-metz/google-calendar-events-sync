from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from googleCalendar import subscribe_to_google_calendar_push_notifications

app = FastAPI()
subscribe_to_google_calendar_push_notifications()

# Create a Pydantic model to define the expected data in the POST request
class Item(BaseModel):
    name: str
    description: str = None

# In-memory storage for demonstration purposes
items = []

# Define a POST endpoint to create an item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

# Define a GET endpoint to retrieve all items (for testing)
@app.get("/items/", response_model=list[Item])
async def read_items():
    return items

# Create a Pydantic model to define the expected data in the POST request
class Item(BaseModel):
    name: str
    description: str = None

# Define a POST endpoint to handle google calendar events
@app.post("/google-calendar-events-webhook/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item