import dash_bootstrap_components as dbc
from dash import html, dcc
from layouts.components.footer import getFooter
from layouts.components.header import getHeader

multiple_reports_view_layout = dbc.Container([
    dcc.Store(id='report-data-store-multiple'),
    getHeader("Multiple Reports View"),
    dbc.Row(dbc.Col(html.H2("Univariate analysis", className="text-center"), width=12)),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='columns-selector',
            ),
            dbc.Row(
                dbc.Button(
                    "Single Reports View",
                    href="/single-report",
                    className="btn btn-light",
                    style={
                        "borderWidth": "0.2vh",
                        "borderStyle": "solid",
                        "borderRadius": "5px",
                        "borderColor": "Grey",
                    },
                ),
                style={"margin": "0 0 1vh 0", "padding": "0 0"},
            ),
            dbc.Row(
            dbc.Button(
                "Download CSV",
                id='download-btn',
                className="btn btn-light",
                style={
                    "borderWidth": "0.2vh",
                    "borderStyle": "solid",
                    "borderRadius": "5px",
                    "borderColor": "Grey",
                },
            ),
            style={"margin": "0 0 1vh 0", "padding": "0 0"},
            ),
            dcc.Download(id="download-csv"),
            dbc.Row(
                dbc.Button(
                    "Go Back",
                    href="/",
                    className="btn btn-light",
                    style={
                        "borderWidth": "0.2vh",
                        "borderStyle": "solid",
                        "borderRadius": "5px",
                        "borderColor": "Grey",
                    },
                ),
                style={"margin": "0", "padding": "0"},
            )
            ], width=3),
        dbc.Col(html.Div(id='report-stats'), width=9, style={"margin": "0", "padding": "0 2vw"})
        ], 
        style={"margin": "0", "padding": "0 0"}),
    dbc.Row(dbc.Col(html.H2("Multivariate analysis", className="text-center"), width=12)),
    dbc.Row(dbc.Col(dcc.Graph(id='report-graphics', style={'height': '75vh', 'width': '100%'}), width=12)),
    getFooter()
], fluid=True, style={"padding": "0", "margin": "0", "display": "flex", "flexDirection": "column", "minHeight": "100vh"},)