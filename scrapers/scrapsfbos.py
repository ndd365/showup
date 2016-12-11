import feedparser
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta
import pytz

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials


scopes = 'https://www.googleapis.com/auth/calendar'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scopes)

http_auth = credentials.authorize(Http())

CAL = build('calendar', 'v3', http=credentials.authorize(Http()))


class Event(object):

    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return self.name

def get_calendar_data():

    events = []

    url = "http://sfbos.org/events/feed"

    feed = feedparser.parse(url)



    for item in feed["items"]: 

        event_name = item["title"]

        event_details=item["summary_detail"]["value"]
        soup = BeautifulSoup(event_details, 'html.parser')
        start_date_unaware = parse(soup.span.string)
        start_date = start_date_unaware.replace(tzinfo=pytz.UTC)
        end_date = start_date + timedelta(hours=1)

        event = Event(event_name, start_date, end_date)
        print event
        events.append(event)
    return events

def sync_to_google_calendar(events):

    for event in events:
        GMT_OFF = '-07:00'      # PDT/MST/GMT-7

        start_date = event.start_date.isoformat()
        end_date = event.end_date.isoformat()


        gcal_event = {
            'summary': event.name,
            'start':  {'dateTime': start_date},
            'end':    {'dateTime': end_date},
            'attendees': [
                # {'email': 'friend1@example.com'},
                # {'email': 'friend2@example.com'},
            ],
        }

        print gcal_event
        e = CAL.events().insert(calendarId='tn9cl12g4s7l978r0iqk3ieppk@group.calendar.google.com',
                sendNotifications=True, body=gcal_event).execute()

        print e

def print_calendars():

    page_token = None

    while True:
        calendar_list = CAL.calendarList().list(pageToken=page_token).execute()

        for calendar_list_entry in calendar_list['items']:

            print calendar_list_entry

        page_token = calendar_list.get('nextPageToken')
        
        if not page_token:
            break

events = get_calendar_data()

sync_to_google_calendar(events)


