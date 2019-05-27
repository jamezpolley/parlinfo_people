import json
import os
import logging
import datetime

import requests
os.environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'
import scraperwiki

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRAPE_DATE = datetime.date.today()
APH_BASE_URL = "https://www.aph.gov.au/api/parliamentarian/?q=&mem=0"


def process_person(person):
    person["date_scraped"] = SCRAPE_DATE
    timestamp = person['DateElected'].partition("(")[2].rpartition(")")[0]
    timestamp = int(timestamp)/1000
    date_elected = datetime.date.fromtimestamp(timestamp)
    person["DateElected"] = date_elected
    return person

data = json.loads(requests.get(APH_BASE_URL).content)
page = 0

while data:
    for person in data:
        person = process_person(person)
        logger.info("Recording %(MPID)s: %(FullName)s, %(RepresentingTitle)s for "
            "%(Representing)s since %(DateElected)s", person)
        scraperwiki.sqlite.save(unique_keys=("MPID", "date_scraped"), data=person, table_name="data")
    page += 1
    current_url = APH_BASE_URL + "&page={}".format(page)
    data = json.loads(requests.get(current_url).content)