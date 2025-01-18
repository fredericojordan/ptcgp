__all__ = ("layout",)

import dash
import dash_mantine_components as dmc
import plotly.express as px

from ptcgp import objects

dash.register_page(__name__, path_template="/card/<card_str>")


def stats_graph(card: objects.Card):
    fig = px.line_polar(
        card.stats,
        r="r",
        theta="theta",
        line_close=True,
        range_r=[0, 5],
        template="plotly_dark",
        color_discrete_sequence=[card.rgb],
    )
    fig.update_traces(fill="toself")
    fig.update_layout(paper_bgcolor="#333")
    return dash.dcc.Graph(figure=fig)


def layout(card_str: str | None = None, **kwargs):
    if not card_str:
        return dmc.Text("No card selected.")

    card = objects.Card.from_file(f"{card_str}.json")
    stats = dmc.Group(
        [
            dmc.Image(src=card.image, alt=card.name, fit="scale-down", h=500),
            # details_stack,
            stats_graph(card),
        ]
    )
    return dmc.Center(stats, py=30)
