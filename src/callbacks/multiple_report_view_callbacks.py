from dash import Output, Input, State, html, dcc, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
from callbacks.utils import get_report_data, univariate_analysis, format_categorized_data

def format_stat(value):
    return "No results" if math.isnan(value) else value

def register_multiple_report_view_callbacks(app):
    
    @app.callback(
        Output('report-data-store-multiple', 'data'),
        Input('url', 'pathname')
    )
    def load_report_data(pathname):
        if pathname == '/multiple-report':
            df = get_report_data()
            return df.to_dict('records')
        else:
            raise PreventUpdate
        
    @app.callback(
        Output("download-csv", "data"),
        Input("download-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def generate_csv(n_clicks):
        return dcc.send_file("../data/csvs/report_summary.csv")

    @app.callback(
        Output('columns-selector', 'options'),
        Input('report-data-store-multiple', 'data')
    )
    def update_dropdown_options(data):
        if data is None:
            raise PreventUpdate
        else:
            df = pd.DataFrame(data)
            """
            numeric_columns = df.select_dtypes(include='number').columns
            numeric_columns = [col for col in numeric_columns if col not in ['Type', 'ID']]
            """
            numeric_columns = [
                "TimeInBed",
                "Age",
                "Height",
                "Weight",
                "AHI",
                "AHI.TTS",
                "SnoreDuration",
                "CentralApneasNum",
                "HypopneasTotalNum",
                "MixedApneasNum",
                "ApneasTotal",
                "ObstructiveApneasNum",
                "SaO2min",
                "Desaturation<90%"
            ]
            options = [{'label': col, 'value': col} for col in numeric_columns]
            return options
        
    @app.callback(
        Output('report-stats', 'children'),
        Input('columns-selector', 'value'),
        Input('report-data-store-multiple', 'data')
    )
    def update_report_details(column_name, data):
        if column_name is None:
            raise PreventUpdate
        if data is None:
            raise PreventUpdate
        df = pd.DataFrame(data)
        stats = univariate_analysis(df, column_name)

        # Define color sequence
        color_discrete_sequence = ["#af80f9", "#ff76d6", "#ff81a7", "#ffa47b", "#ffcf63", "#f9f871"]

        # Customize Histogram
        histogram_fig = go.Figure(data=[go.Histogram(
            x=df[column_name],
            marker=dict(color=color_discrete_sequence[0])  # Using the first color
        )])
        histogram_fig.update_layout(
            title=f"Histogram of {column_name}",
            xaxis_title=column_name,
            yaxis_title='Frequency',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black')
        )

        # Customize Density Plot using Plotly Express
        density_fig = px.density_contour(df, x=column_name, color_discrete_sequence=color_discrete_sequence)
        density_fig.update_traces(contours_coloring="fill")
        density_fig.update_layout(
            title=f"Density Plot of {column_name}",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black')
        )

        # Customize Bar Chart
        bar_fig = go.Figure(data=[go.Bar(
            x=df.index,
            y=df[column_name],
            marker=dict(color=color_discrete_sequence[5])  # Using the second color
        )])
        bar_fig.update_layout(
            title=f"Bar Chart of {column_name}",
            xaxis_title="Index",
            yaxis_title=column_name,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black')
        )
        table = html.Div([
            html.Table(
                # Header
                [html.Tr([html.Th("Statistic"), html.Th("Value")])] +
                
                # Body
                [html.Tr([html.Td(stat), html.Td(format_stat(value))]) for stat, value in stats.items()],
                
                style={'width': '50%', 'borderCollapse': 'collapse', 'float': 'left'},
                # Style the table cells
                # Add any other styles you need here
            )
        ])

        children = [
            html.Div([
                html.H4(f"Statistics for {column_name}"),
                dbc.Row([
                    html.Div([
                        table
                    ])
                ]),
                
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=histogram_fig, style={'height': '300px', 'width': '100%'}),
                            body=True,
                            style={'margin-bottom': '15px'}
                        ),
                        width=12, sm=6
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=density_fig, style={'height': '300px', 'width': '100%'}),
                            body=True,
                            style={'margin-bottom': '15px'}
                        ),
                        width=12, sm=6
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=bar_fig, style={'height': '300px', 'width': '100%'}),
                            body=True,
                            style={'margin-bottom': '15px'}
                        ),
                        width=12, sm=6
                    )
                ])
            ])
        ]
        return children
    @app.callback(
        Output('report-graphics', 'figure'),
        Input('report-data-store-multiple', 'data')
    )
    def multivariate_analysis_grafic(data):
        if data is None:
            raise PreventUpdate
        df = pd.DataFrame(data)
        numeric_columns = [
                "TimeInBed",
                "Age",
                "Height",
                "Weight",
                "AHI",
                "AHI.TTS",
                "SnoreDuration",
                "CentralApneasNum",
                "HypopneasTotalNum",
                "MixedApneasNum",
                "ApneasTotal",
                "ObstructiveApneasNum",
                "SaO2min",
                "Desaturation<90%"
            ]
        corr = df[numeric_columns].corr()
        fig = px.imshow(corr, 
                    labels=dict(x="Features", y="Features", color="Correlation"), 
                    x=corr.columns, 
                    y=corr.columns, 
                    text_auto=True, 
                    aspect="auto")
        return fig


        