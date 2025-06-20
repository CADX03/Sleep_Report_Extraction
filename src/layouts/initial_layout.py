import dash_bootstrap_components as dbc
from layouts.components.footer import getFooter
from layouts.components.header import getHeader
from dash import dcc, html

initial_layout = dbc.Container(
    [
        getHeader("Sleep Report Analyzer"),
        dbc.Row(
            dbc.Col(
                html.P(
                    "This interactive tool allows you to upload and analyze sleep study reports in PDF format. Simply drag "
                    "and drop your files into the designated area or use the 'Select PDF Files' button to upload your "
                    "reports. After uploading, click on 'Process and Save Files' to generate insights into sleep patterns and "
                    "metrics. The analysis includes detailed visualizations and summaries, aiding in better understanding "
                    "and management of sleep health.",
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "height": "100%",
                    },
                    className="text-left"
                ),
                width=12,
                style={
                    "width": "50%",
                    "textAlign": "left",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "margin": "auto",
                    "cursor": "pointer",
                },
            ),
            style={"padding": "0", "margin": "2vh 0"},
        ),
        dbc.Row(
            dbc.Col(
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(
                        ["Drag and Drop or ", html.A("Select PDF Files")],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "height": "100%",
                        },
                    ),
                    style={
                        "width": "50%",
                        "height": "20vh",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "margin": "auto",
                        "cursor": "pointer",
                    },
                    multiple=True,
                    accept=".pdf",
                ),
                width=12,
            ),
            style={"padding": "0", "margin": "2vh 0", "height": "100%"},
        ),

        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    id="loading",
                    children=[dbc.Button("Process and Save Files", id="save-files-btn", className="btn btn-light", style={
                        "borderWidth": "0.2vh",
                        "borderStyle": "solid",
                        "borderRadius": "5px",
                        "borderColor": "Grey",
                    })],
                    type="graph",
                    fullscreen=True,
                ),
                width=6,
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                },
            ),
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "padding": "0",
                "margin": "0",
            },
        ),

        dbc.Row(
            dbc.Col(
                html.H4("Selected Files"),
                width=12,
                style={
                    "margin": "4vh 0 1vh 0",
                    "width": "50%",
                },
            ),
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "padding": "0",
                "margin": "0",
            },
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id="output-data-upload"),
                width=12,
                style={
                    "margin": "0",
                    "width": "50%",
                    "boxShadow": "inset 0 0 3px #313638",
                    "borderRadius": "5px",
                    "minHeight": "5vh",
                    "maxHeight": "20vh",
                    "overflow": "auto",
                },
            ),
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "padding": "0",
                "margin": "0 0 2vh 0",
            },
        ),
        getFooter(),
    ],
    fluid=True,
    style={"padding": "0", "margin": "0", "display": "flex", "flexDirection": "column", "minHeight": "100vh"},
)
