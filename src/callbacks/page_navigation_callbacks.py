from dash import Output, Input
from layouts.initial_layout import initial_layout
from layouts.multiple_reports_view_layout import multiple_reports_view_layout
from layouts.single_report_view_layout import single_report_view_layout

def register_page_navigation_callbacks(app):
    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/multiple-report':
            return multiple_reports_view_layout
        if pathname == '/single-report':
            return single_report_view_layout
        else:
            return initial_layout
