import feedparser
import urllib
from bs4 import BeautifulSoup
import pprint
from dateutil.parser import parse
import requests
import time
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

    url = "http://www.calendarwiz.com/calendars/rssfeeder.xml?crd=sfplanning&len=0&days=7000&events=1000&title=SF%20Planning%20Dept%20-%20Hearing%20Calendar&cat=all"

    feed = feedparser.parse(url)

    for item in feed["entries"]: 

        event_url = item['links'][0]["href"]
        print event_url
        r = requests.get(event_url)
        soup = BeautifulSoup(r.text, "html.parser")
        event_name = soup.find(id="titletag").get_text().rstrip()
        time_string= soup.find(id="event_date").p.get_text().split("|")

        if "-" in time_string[1]:
            time_string[1]=time_string[1][3:11]
        try:
            start_date_unaware= parse(time_string[0]+time_string[1])
        except ValueError:
            start_date_unaware= parse(time_string[0]+"09:00am")

        start_date = start_date_unaware.replace(tzinfo=pytz.UTC)
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
        e = CAL.events().insert(calendarId='qd1t88kvmodu780ra1t6n38ivk@group.calendar.google.com',
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

