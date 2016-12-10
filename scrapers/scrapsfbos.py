import feedparser
from bs4 import BeautifulSoup
from dateutil.parser import parse


url = "http://sfbos.org/events/feed"

feed = feedparser.parse( url )


for item in feed["items"]: 

    title = item["title"]
    event_details=item["summary_detail"]["value"]
    soup = BeautifulSoup(event_details, 'html.parser')
    event_datetime = parse(soup.span.string)
    print "TITLE:", title
    print "EVENT_TIME:", event_datetime
