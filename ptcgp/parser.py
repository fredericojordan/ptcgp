__all__ = (
    "parse_card_by_id",
    "parse_card",
    "parse_all_cards",
)

import os
import typing

from . import constants
from . import objects
from . import utils


def parse_card_by_id(exp_name: str, card_id: str) -> objects.Card:
    exp_folder = os.path.join(constants.Constants.EXPANSIONS_FOLDER, exp_name)
    filepath = os.path.join(exp_folder, f"{card_id}.html")
    return parse_card(filepath)


def parse_card(filepath: str) -> objects.Card:
    html = utils.load_file(filepath)
    return objects.Card.from_html(html)


def parse_all_cards() -> typing.Iterator[objects.Card]:
    for dir_path, _dir_names, files in os.walk(constants.Constants.EXPANSIONS_FOLDER):
        if dir_path == constants.Constants.EXPANSIONS_FOLDER:
            continue

        for file in files:
            file_path = os.path.join(dir_path, file)
            try:
                yield parse_card(str(file_path))
            except Exception:
                print(f"failed to parse file {file_path}")
                raise


if __name__ == "__main__":
    for card in parse_all_cards():
        card.to_file()
