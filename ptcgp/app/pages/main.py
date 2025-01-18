__all__ = ("layout",)

import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go

from ptcgp import constants, objects
from ptcgp.app.components import Select

dash.register_page(__name__, path="/")

carousel = dmc.Carousel(
    children=[],
    id="carousel-cards",
    withIndicators=True,
    slideSize={"base": "100%", "sm": "50%", "md": "33.333333%", "lg": "20%"},
    slideGap={"base": "sm", "sm": "md"},
    dragFree=True,
    loop=True,
    align="start",
    height=500,
    p=50,
)

card_filters = dmc.Group(
    [
        Select("color", constants.Color),
        Select("rarity", constants.Rarity),
        Select("card type", constants.CardType),
        Select("weakness", constants.Color),
        dmc.Select(
            data=list(constants.Ability),
            id="select-ability",
            placeholder="Select ability...",
            clearable=True,
        ),
        Select("evolution stage", constants.EvolutionStage),
        Select("expansion", constants.Expansion),
        dmc.Button(
            children="Clear all",
            id="clear-filters-btn",
            color="gray",
            variant="light",
        ),
    ]
)


layout = dash.html.Div(
    [
        dash.dcc.Store(id="cards-store", data=[]),
        dash.html.H1(
            children="Pokémon TCG Pocket Explorer", style={"textAlign": "center"}
        ),
        dmc.Center(card_filters),
        carousel,
        dmc.Center(dash.html.H4(id="card-count", children="")),
        dash.html.Div(id="graph", children=[]),
    ]
)


@dash.callback(
    dash.Output("carousel-cards", "children"),
    dash.Output("card-count", "children"),
    dash.Input("cards-store", "data"),
    prevent_initial_call=True,
)
def display_cards(data: list[dict]):
    return [
        dmc.CarouselSlide(objects.Card.model_validate(c).as_ui()) for c in data
    ], f"{len(data)} matching cards"


@dash.callback(
    dash.Output("graph", "children"),
    dash.Input("cards-store", "data"),
    prevent_initial_call=True,
)
def make_graph(data: list[dict]):
    graph_data = []
    if len(data) > 0:
        cards = pd.DataFrame(data)
        life_counts = cards.life.value_counts()
        dmg_counts = cards.dmg.value_counts()
        graph_data = [
            go.Bar(name="Life", x=life_counts.index, y=life_counts.values),
            go.Bar(name="Dmg", x=dmg_counts.index, y=dmg_counts.values),
        ]

    fig = go.Figure(data=graph_data)
    fig.update_layout(paper_bgcolor="#333", template="plotly_dark")
    return dmc.Container(children=[dash.dcc.Graph(figure=fig)])


@dash.callback(
    dash.Output("cards-store", "data"),
    dash.Input("select-color", "value"),
    dash.Input("select-rarity", "value"),
    dash.Input("select-card-type", "value"),
    dash.Input("select-weakness", "value"),
    dash.Input("select-ability", "value"),
    dash.Input("select-evolution-stage", "value"),
    dash.Input("select-expansion", "value"),
)
def filter_cards(
    color_values: list[str],
    rarity_values: list[str],
    card_types: list[str],
    weaknesses: list[str],
    ability: str,
    stages: list[str],
    expansions: list[str],
) -> list[dict]:
    cards = objects.ALL_CARDS_DF

    if color_values:
        cards = cards[cards.color.isin(color_values)]
    if rarity_values:
        cards = cards[cards.rarity.isin(rarity_values)]
    if card_types:
        cards = cards[cards.card_type.isin(card_types)]
    if weaknesses:
        cards = cards[cards.weakness.isin(weaknesses)]
    if ability is not None:
        cards = (
            cards[cards.ability.notnull()]
            if ability == constants.Ability.WITH_ABILITY
            else cards[cards.ability.isnull()]
        )
    if stages:
        cards = cards[cards.stage.isin(stages)]
    if expansions:
        cards = cards[cards.expansion.isin(expansions)]

    return cards.to_dict("records")


dash.clientside_callback(
    """function (n) { return [[], [], [], [], null, [], []]; }""",
    dash.Output("select-color", "value"),
    dash.Output("select-rarity", "value"),
    dash.Output("select-card-type", "value"),
    dash.Output("select-weakness", "value"),
    dash.Output("select-ability", "value"),
    dash.Output("select-evolution-stage", "value"),
    dash.Output("select-expansion", "value"),
    dash.Input("clear-filters-btn", "n_clicks"),
    prevent_initial_call=True,
)
