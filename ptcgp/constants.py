__all__ = (
    "Ability",
    "CardType",
    "Color",
    "Constants",
    "Expansion",
    "Rarity",
)

import enum
import os


class Constants:
    HTML_FOLDER = os.path.join(os.path.dirname(__file__), "html")
    EXPANSIONS_FOLDER = os.path.join(HTML_FOLDER, "expansions")
    JSON_FOLDER = os.path.join(os.path.dirname(__file__), "json")


class Color(enum.StrEnum):
    GRASS = "Grass"
    FIRE = "Fire"
    WATER = "Water"
    LIGHTNING = "Lightning"
    PSYCHIC = "Psychic"
    FIGHTING = "Fighting"
    DARKNESS = "Darkness"
    METAL = "Metal"
    DRAGON = "Dragon"
    COLORLESS = "Colorless"


class CardType(enum.StrEnum):
    POKEMON = "Pokémon"
    ITEM = "Item"
    SUPPORTER = "Supporter"


class Rarity(enum.StrEnum):
    COMMON = "◊"
    UNCOMMON = "◊◊"
    RARE = "◊◊◊"
    EX = "◊◊◊◊"
    FULL_ART = "☆"
    FULL_ART_RARE = "☆☆"
    IMMERSIVE = "☆☆☆"
    CROWN = "🜲"


class Expansion(enum.StrEnum):
    GENETIC_APEX = "A1"
    MYTHICAL_ISLAND = "A1a"
    PROMO_A = "P-A"


class Ability(enum.StrEnum):
    WITH_ABILITY = "With ability"
    WITHOUT_ABILITY = "Without ability"
