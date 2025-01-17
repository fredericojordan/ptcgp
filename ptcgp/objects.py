__all__ = (
    "Ability",
    "Attack",
    "Card",
)

import os

import bs4
import dash_mantine_components as dmc
import pydantic

from . import constants
from . import utils


class Attack(pydantic.BaseModel):
    name: str
    cost: str
    effect: str | None = None
    damage: int | None = None
    damage_min: int | None = None
    damage_mult: int | None = None

    @classmethod
    def from_soup(cls, soup: bs4.Tag) -> "Attack":
        atk_parts = soup.find("p", class_="card-text-attack-info").text.split()

        args = {
            "cost": soup.find("p", class_="card-text-attack-info")
            .find("span", class_="ptcg-symbol")
            .text,
            "name": atk_parts[1],
            "effect": soup.find("p", class_="card-text-attack-effect").text.strip(),
        }

        try:
            dmg = atk_parts[-1]
            if "+" in dmg:
                args["damage_min"] = int(dmg.strip("+"))
            elif "x" in dmg:
                args["damage_mult"] = int(dmg.strip("x"))
            else:
                args["damage"] = int(dmg)
        except:
            pass

        return cls.model_validate(args)


class Ability(pydantic.BaseModel):
    name: str
    effect: str

    @classmethod
    def from_soup(cls, soup: bs4.Tag) -> "Ability":
        args = {
            "name": soup.find("p", class_="card-text-ability-info")
            .text.split("Ability: ")[-1]
            .strip(),
            "effect": soup.find("p", class_="card-text-ability-effect").text.strip(),
        }

        return cls.model_validate(args)


class Card(pydantic.BaseModel):
    id: str
    expansion: str
    image: str
    name: str
    card_type: constants.CardType
    artist: str
    attacks: list[Attack] = pydantic.Field(default_factory=list)

    rarity: constants.Rarity | None = None
    color: constants.Color | None = None
    life: int | None = None
    ability: Ability | None = None
    weakness: constants.Color | None = None
    retreat_cost: int | None = None

    @property
    def index_str(self) -> str:
        return f"{self.expansion}_{int(self.id):03}"

    @classmethod
    def get_color(cls, title: list[str]) -> constants.Color | None:
        for member in title:
            if member in constants.Color:
                return constants.Color(member)

    @classmethod
    def get_type(cls, soup: bs4.Tag) -> constants.CardType:
        for card_type in constants.CardType:
            if card_type in soup.text:
                return constants.CardType(card_type)

    @classmethod
    def get_rarity(cls, soup: bs4.Tag) -> constants.Rarity:

        if "Crown Rare" in soup.text:
            return constants.Rarity.CROWN
        else:
            for rarity in [
                constants.Rarity.EX,
                constants.Rarity.RARE,
                constants.Rarity.UNCOMMON,
                constants.Rarity.COMMON,
                constants.Rarity.IMMERSIVE,
                constants.Rarity.FULL_ART_RARE,
                constants.Rarity.FULL_ART,
            ]:
                if rarity in soup.text:
                    return rarity

    @classmethod
    def from_html(cls, html: str) -> "Card":
        soup = bs4.BeautifulSoup(html, features="html.parser")
        profile = soup.find("div", class_="card-profile")
        details = profile.find("div", class_="card-details")
        title = " ".join(
            details.find("p", class_="card-text-title").text.split()
        ).split(" - ")
        print_info = soup.find("div", class_="card-prints-current")
        card_id = (
            print_info.find("div", class_="prints-current-details")
            .find_all("span")[1]
            .text.split()[0]
            .strip("#")
        )

        args = {
            "id": card_id,
            "expansion": print_info.img.get("alt"),
            "image": profile.find("div", class_="card-image").img.get("src"),
            "name": details.find("span", class_="card-text-name").text,
            "card_type": cls.get_type(details.find("p", class_="card-text-type")),
            "rarity": cls.get_rarity(print_info),
            "color": cls.get_color(title),
            "artist": details.find("div", class_="card-text-artist").a.text.strip(),
            "attacks": [],
        }

        if weakness_retreat := details.find("p", class_="card-text-wrr"):
            _, weakness, _, retreat_cost = weakness_retreat.text.split()
            if weakness != "none":
                args["weakness"] = weakness
            args["retreat_cost"] = retreat_cost

        for attack in details.find_all("div", class_="card-text-attack"):
            args["attacks"].append(Attack.from_soup(attack))

        if ability := details.find("div", class_="card-text-ability"):
            args["ability"] = Ability.from_soup(ability)

        try:
            args["life"] = int(title[-1].strip(" HP"))
        except:
            pass

        return cls.model_validate(args)

    def to_file(self):
        utils.mkdir(constants.Constants.JSON_FOLDER)
        filename = f"{self.index_str}.json"
        filepath = os.path.join(constants.Constants.JSON_FOLDER, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            n = file.write(self.model_dump_json(indent=2))
            print(f"wrote {n} to {filepath}")

    def as_ui(self):
        return dmc.Image(src=self.image, alt=self.name, fit="scale-down", h=500)
