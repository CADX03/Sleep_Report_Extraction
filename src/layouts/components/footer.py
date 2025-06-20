import dash_bootstrap_components as dbc
from dash import dcc, html

def getFooter():

    logos = [f"assets/logo-{i}.png" for i in range(1, 7)]
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [html.Img(src=logo, style={'height': '5vh', 'marginRight': '10px'}) for logo in logos],
                            style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-start', 'flexWrap': 'wrap', 'paddingLeft': '2vh'}
                        ),
                        width=6,
                        xs=12, sm=12, md=6,
                        style={'padding': '0', 'margin': '0'}
                    ),
                    dbc.Col(
                        html.Div(
                            "This work is financed by Component 5 - Capitalization and Business Innovation, integrated in the Resilience Dimension of the Recovery and Resilience Plan within the scope of the Recovery and Resilience Mechanism (MRR) of the European Union (EU), framed in the Next Generation EU, for the period 2021 - 2026, within project HfPT, with reference 41.",
                            style={'textAlign': 'left', 'overflow': 'hidden', 'textOverflow': 'ellipsis', 'fontSize': '1.5vh', 'paddingRight': '2vh'}
                        ),
                        width=6,
                        xs=12, sm=12, md=6,
                        style={'padding': '0', 'margin': '0'}
                    )
                ],
                style={'padding': '0', 'margin': '0'}
            )
        ],
        style={
            "marginTop": "auto",
            "width": "100%",
            "borderWidth": "0.2vh 0 0 0",
            "borderColor": "LightGrey",
            "borderStyle": "solid",
            "padding": "2vh 0",
            "color": "white",
            "backgroundColor": "#313638",
            "fontWeight": "bold",
        }
    )