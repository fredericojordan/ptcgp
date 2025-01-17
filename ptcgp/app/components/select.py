__all__ = ("Select",)

import enum

import dash_mantine_components as dmc

from ... import utils


class Select(dmc.MultiSelect):
    def __init__(self, name: str, options: type[enum.StrEnum], *args, **kwargs):
        kwargs = {
            "id": f"select-{utils.kebab_case(name)}",
            "data": list(options),
            "placeholder": f"Select {name}...",
            "searchable": True,
            "clearable": True,
            **kwargs,
        }
        super().__init__(*args, **kwargs)
