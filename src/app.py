from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from layouts.initial_layout import initial_layout
from callbacks.page_navigation_callbacks import register_page_navigation_callbacks
from callbacks.file_upload_callbacks import register_file_upload_callbacks
from callbacks.single_report_view_callbacks import register_single_report_view_callbacks
from callbacks.multiple_report_view_callbacks import register_multiple_report_view_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.15.4/css/all.css"], suppress_callback_exceptions=True)

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={"padding": "0", "margin": "0"})
], fluid=True, style={"padding": "0", "margin": "0", "fontFamily": "Sans-serif"})

register_page_navigation_callbacks(app)
register_file_upload_callbacks(app)
register_single_report_view_callbacks(app)
register_multiple_report_view_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)  