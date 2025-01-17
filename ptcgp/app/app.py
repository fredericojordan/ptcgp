__all__ = ("app",)

import dash
import dash_mantine_components as dmc

dash._dash_renderer._set_react_version("18.2.0")  # noqa

app = dash.Dash(
    title="PTCGP Explorer",
    external_stylesheets=dmc.styles.ALL,
    use_pages=True,
)

app.layout = dmc.MantineProvider([dash.page_container])
app.server.static_folder = "assets"


if __name__ == "__main__":
    app.run(debug=True)
