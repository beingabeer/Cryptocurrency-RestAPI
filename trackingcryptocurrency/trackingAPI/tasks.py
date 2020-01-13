import requests
from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup

from .models import Cryptocurrency


@shared_task
def crawl_currency():
    print("Crawling data and creating objects in database")
    r = requests.get("https://coinranking.com/", headers={"User-Agent": "Mozilla/5.0"})
    html = r.text
    bs = BeautifulSoup(html, "html.parser")

    rows = bs.find("tbody", class_="table__body").find_all("tr", class_="table__row")[
        0:5
    ]

    for row in rows:
        cryptocurrency = (
            row.find("span", class_="profile__name")
            .get_text()
            .strip()
            .replace("\n", "")
        )
        print(cryptocurrency)


crawl_currency()
