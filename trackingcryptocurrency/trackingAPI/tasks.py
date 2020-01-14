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
        values = row.find_all("div", class_="valuta")
        price = values[0].get_text().strip().replace("\n", "")
        # print(price)
        market_cap = values[1].get_text().strip().replace("\n", "")
        # print(market_cap)
        change = (
            row.find("div", class_="change")
            .find("span")
            .get_text()
            .strip()
            .replace("\n", "")
        )
        print(
            {
                "cryptocurrency": cryptocurrency,
                "price": price,
                "market_cap": market_cap,
                "change": change,
            }
        )

        # Add these objects in database
        Cryptocurrency.objects.create(
            cryptocurrency=cryptocurrency,
            price=price,
            market_cap=market_cap,
            change=change,
        )

        # Sleeping to avoid any errors
        sleep(3)


def update_currency():
    print("Updating data")
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
        values = row.find_all("div", class_="valuta")
        price = values[0].get_text().strip().replace("\n", "")
        # print(price)
        market_cap = values[1].get_text().strip().replace("\n", "")
        # print(market_cap)
        change = (
            row.find("div", class_="change")
            .find("span")
            .get_text()
            .strip()
            .replace("\n", "")
        )
        data = {
            "cryptocurrency": cryptocurrency,
            "price": price,
            "market_cap": market_cap,
            "change": change,
        }

        print(
            {
                "cryptocurrency": cryptocurrency,
                "price": price,
                "market_cap": market_cap,
                "change": change,
            }
        )
        # Update objects
        Cryptocurrency.objects.filter(cryptocurrency=cryptocurrency).update(**data)
        sleep(3)


crawl_currency()

while True:
    update_currency()
    sleep(15)
