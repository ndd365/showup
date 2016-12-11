from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scopes = 'https://www.googleapis.com/auth/calendar'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scopes)

http_auth = credentials.authorize(Http())

CAL = build('calendar', 'v3', http=credentials.authorize(Http()))

def print_calendars():

    page_token = None

    while True:
        calendar_list = CAL.calendarList().list(pageToken=page_token).execute()

        for calendar_list_entry in calendar_list['items']:
            pprint.pprint(calendar_list_entry)

        page_token = calendar_list.get('nextPageToken')
        
        if not page_token:
            break

print_calendars()