__all__ = (
    "cards_urls",
    "download_all_cards",
    "download_card_html",
    "download_expansion_html",
    "download_expansions_html",
    "expansion_urls",
)

import enum
import http
import os
import typing

import requests
from bs4 import BeautifulSoup

from . import constants
from . import utils


class Urls(enum.StrEnum):
    BASE = "https://pocket.limitlesstcg.com"
    EXPANSIONS = f"{BASE}/cards/"


def download_expansions_html() -> str:
    res = requests.get(Urls.EXPANSIONS)

    if res.status_code != http.HTTPStatus.OK:
        raise Exception(res.status_code)

    filename = os.path.join(constants.Constants.HTML_FOLDER, "expansions.html")
    utils.mkdir(constants.Constants.HTML_FOLDER)
    with open(filename, "w", encoding="utf-8") as file:
        n = file.write(res.text)
        print(f"wrote {n} to {filename}")

    return res.text


def expansion_urls(text: str | None = None) -> typing.Iterator[str]:
    html_text = (
        text or utils.load_html_file("expansions.html") or download_expansions_html()
    )
    soup = BeautifulSoup(html_text, features="html.parser")
    data_table = soup.find("table", class_="data-table")
    routes = set(link.get("href") for link in data_table.find_all("a"))
    for route in sorted(routes):
        yield Urls.BASE + route


def download_expansion_html(exp_url: str) -> str:
    exp_name = exp_url.split("/")[-1]
    res = requests.get(exp_url)

    if res.status_code != http.HTTPStatus.OK:
        raise Exception(res.status_code)

    filename = os.path.join(constants.Constants.EXPANSIONS_FOLDER, f"{exp_name}.html")
    utils.mkdir(constants.Constants.EXPANSIONS_FOLDER)
    with open(filename, "w", encoding="utf-8") as file:
        n = file.write(res.text)
        print(f"wrote {n} to {filename}")

    return res.text


def cards_urls(exp_url: str) -> typing.Iterator[str]:
    exp_name = exp_url.split("/")[-1]
    html_text = utils.load_html_file(
        f"expansions/{exp_name}.html"
    ) or download_expansion_html(exp_url)

    soup = BeautifulSoup(html_text, features="html.parser")
    cards_table = soup.find("div", class_="card-search-grid")
    routes = set(link.get("href") for link in cards_table.find_all("a"))
    for route in sorted(routes):
        yield Urls.BASE + route


def download_card_html(card_url: str) -> str:
    res = requests.get(card_url)

    if res.status_code != http.HTTPStatus.OK:
        raise Exception(res.status_code)

    exp_name = card_url.split("/")[-2]
    card_id = card_url.split("/")[-1]
    exp_folder = os.path.join(constants.Constants.EXPANSIONS_FOLDER, exp_name)
    utils.mkdir(exp_folder)
    filename = os.path.join(exp_folder, f"{card_id}.html")
    with open(filename, "w", encoding="utf-8") as file:
        n = file.write(res.text)
        print(f"wrote {n} to {filename}")

    return res.text


def download_all_cards():
    for exp_url in expansion_urls():
        for card_url in cards_urls(exp_url):
            download_card_html(card_url)


if __name__ == "__main__":
    download_all_cards()
