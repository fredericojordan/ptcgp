__all__ = (
    "dash_options",
    "kebab_case",
    "load_file",
    "load_html_file",
    "mkdir",
)

import enum
import os

from constants import Constants


def load_html_file(filename: str) -> str | None:
    filepath = os.path.join(Constants.HTML_FOLDER, filename)
    return load_file(filepath)


def load_file(filepath: str) -> str | None:
    try:
        with open(filepath, encoding="utf-8") as file:
            return file.read()
    except:
        return None


def mkdir(path: str):
    try:
        os.mkdir(path)
    except:
        pass


def dash_options(enumeration: type[enum.StrEnum]):
    return [
        {"label": str(member.name), "value": str(member.value)}
        for member in list(enumeration)
    ]


def kebab_case(input_str: str) -> str:
    return input_str.lower().replace("_", "-").replace(" ", "-")
