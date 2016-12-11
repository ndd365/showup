import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta

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

def get_calendar_data(month, year):

    events = []

    url = "http://sfmayor.org/events/calendar/month/%d-%.02d" % (year, month)

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    tags = soup.find_all("div", class_="view-item-calendar")

    for tag in tags:


        event_name = tag.find_all(class_="field-content")[0].text
        event_datetime_str = tag.find_all(class_="date-display-single")[0].attrs['content']

        if( event_name != "The Mayor has no public events."):
            print event_name
            print event_datetime_str

            start_date = parse(event_datetime_str)
            end_date = start_date + timedelta(hours=1)
            event = Event(event_name, start_date, end_date)

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
