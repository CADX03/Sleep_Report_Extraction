import dash_bootstrap_components as dbc
from dash import dcc, html


def getHeader(page_title):
    return dbc.Row(
        dbc.Col(
            html.H1(f"{page_title}"),
            width=12,
            style={
                "width": "100%",
                "borderWidth": "0 0 0.2vh 0",
                "borderColor": "LightGrey",
                "borderStyle": "solid",
                "padding": "2vh 2vh",
                "color": "white",
                "backgroundColor": "#313638",
                "fontWeight": "bold",
            },
        ),
        style={"padding": "0", "margin": "0", "fontWeight": "bold"},
    )
