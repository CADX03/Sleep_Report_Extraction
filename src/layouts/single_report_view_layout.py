import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.exceptions import PreventUpdate
from layouts.components.footer import getFooter
from layouts.components.header import getHeader

single_report_view_layout = dbc.Container(
    [
        dcc.Store(id="report-data-store"),
        getHeader("Single Report View"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="report-selector",
                            style={"margin": "2vh 0", "padding": "0 0"},
                        ),
                        dbc.Row(
                            dbc.Button(
                                "Multiple Reports View",
                                href="/multiple-report",
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
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    html.Div(id="report-details"),
                    width=9,
                    style={"margin": "0", "padding": "0 2vw"},
                ),
            ],
            style={"margin": "0", "padding": "0 0"},
        ),
        getFooter(),
    ],
    fluid=True,
    style={"padding": "0", "margin": "0", "display": "flex", "flexDirection": "column", "minHeight": "100vh"},
)
