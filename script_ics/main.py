from ics import Calendar, Event
from flask import Flask
import requests, os, json, datetime

"""
IN ORDER TO AVOID TO MUCH REQUESTS DURING DEVELOPMENT, I'VE CREATED A JSON FILE WITH THE RESPONSE OF THE API

def create_calendar_json_file(data: str) -> None:
    with open("calendar_json_test.json", "w") as file:
        file.write(data)

def load_calendar_json_file() -> dict:
    with open("calendar_json_test.json", "r") as file:
        return file.read()

if not os.path.exists("calendar_json_test.json"):
    calendar_json_data: dict = requests.get(url).text
    create_calendar_json_file(calendar_json_data)
    calendar_json_data = json.loads(load_calendar_json_file())
else:
    calendar_json_data: dict = json.loads(load_calendar_json_file())
"""

"""
    List of keys for an event in the json file and equivalent in the ics file:
    - type 
    - params
    - dtstamp
    - start             -> begin
    - datetype
    - end               -> end
    - summary           -> name
    - location          -> location
    - description       -> description
    - uid               -> uid
    - created           -> created
    - lastmodified      -> last_modified
    - sequence
"""

URL: str = "http://descalendrier.jiveoff.fr/api/edt/209"
JSON_CALENDAR_API_RESPONSE: dict = json.loads(requests.get(URL).text)
DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%fZ"
SAVE_PATH: str = "../output/calendar.ics"

if not os.path.exists("output"):
    os.mkdir("output")

def create_event(event: dict) -> Event:
    new_event = Event()
    new_event.name = event["summary"]
    new_event.begin = datetime.datetime.strptime(event["start"], DATE_FORMAT)
    new_event.end = datetime.datetime.strptime(event["end"], DATE_FORMAT)
    new_event.description = event["description"]
    new_event.location = event["location"]
    new_event.created = datetime.datetime.strptime(event["created"], DATE_FORMAT)
    new_event.last_modified = datetime.datetime.strptime(event["lastmodified"], DATE_FORMAT)
    new_event.uid = event["uid"]
    return new_event

def add_events_to_calendar(calendar: Calendar, events: list) -> None:
    for event_uid in events:
        calendar.events.add(create_event(events[event_uid]))

def create_ics_file(calendar: Calendar) -> None:
    with open(SAVE_PATH, "w") as file:
        file.writelines(calendar)

def create_calendar(save_it: bool = False) -> Calendar:
    calendar = Calendar()
    add_events_to_calendar(calendar, JSON_CALENDAR_API_RESPONSE)
    if save_it:
        create_ics_file(calendar)
        return "Calendar created"
    return calendar

create_calendar(save_it=True)
