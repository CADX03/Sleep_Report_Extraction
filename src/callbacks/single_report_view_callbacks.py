from dash import Output, Input, State, html, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from transformers import pipeline
import json
import plotly.express as px
import pandas as pd
from callbacks.utils import (
    get_report_data,
    load_entities,
    highlight_entities,
    format_categorized_data,
    categorize_report_data,
    generate_legend,
    generate_plots,
)
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML


def register_single_report_view_callbacks(app):

    @app.callback(Output("report-data-store", "data"), Input("url", "pathname"))
    def load_report_data(pathname):
        if pathname == "/single-report":
            df = get_report_data()
            return df.to_dict("records")
        else:
            raise PreventUpdate

    @app.callback(
        Output("report-selector", "options"), Input("report-data-store", "data")
    )
    def update_dropdown_options(data):
        if data is None:
            raise PreventUpdate
        df = pd.DataFrame(data)
        options = [{"label": name, "value": name} for name in df["SourcePDF"]]
        return options

    @app.callback(
        Output("report-details", "children"),
        Input("report-selector", "value"),
        State("report-data-store", "data"),
    )
    def update_report_details(report_name, data):
        if report_name is None or data is None:
            raise PreventUpdate

        df = pd.DataFrame(data)
        report_data = df[df["SourcePDF"] == report_name].iloc[0]

        comment = report_data["Comments"]
        entities = load_entities()
        report_entities = entities.get(report_name, [])

        annotated_text = highlight_entities(comment, report_entities)
        legend = generate_legend()



        #print(report_data["N1tts"], report_data["N2tts"], report_data["N3tts"], report_data["REMtts"])

        plots =  generate_plots(report_data)

        categorized_data = categorize_report_data(report_data)
        formatted_tables = format_categorized_data(categorized_data)

        children = [
            html.Div(
                [
                    html.H3(
                        report_name,
                        style={
                            "marginBottom": "2vh",
                            "paddingBottom": "2vh",
                            "boxShadow": "0px 0.5px 0.5px 0px rgba(0, 0, 0, 0.1)",
                        },
                    ),
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    DangerouslySetInnerHTML(annotated_text),
                                    style={"marginTop": "2vh", "marginBottom": "2vh"},
                                    width=8,
                                ),
                                dbc.Col(
                                    legend,
                                    style={
                                        "marginTop": "2vh",
                                        "marginBottom": "2vh",
                                        "margin-left": "5vh",
                                    },
                                    width=2,
                                ),
                            ]
                        )
                    ),
                    html.H4(
                        f"Sleep Efficiency: {report_data['SleepEfficiency']}%",
                        style={"marginTop": "2vh", "marginBottom": "4vh"},
                    ),
                    html.Div(plots, style={"marginTop": "2vh", "marginBottom": "2vh"}),
                    html.Div(
                        formatted_tables,
                        style={"marginTop": "2vh", "marginBottom": "2vh"},
                    ),
                ],
                style={
                    "overflowY": "scroll",
                    "maxHeight": "76vh",
                    "margin": "2vh 0",
                    "padding": "2vh",
                    "boxShadow": "0px 0px 0.5vh 0px rgba(0, 0, 0, 0.1)",
                    "borderRadius": "5px",
                },
            )
        ]
        return children
