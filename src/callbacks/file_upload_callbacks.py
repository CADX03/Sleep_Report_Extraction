from dash import Output, Input, State, html
from dash.exceptions import PreventUpdate
import base64
import os
from data_extraction import extract_info_from_pdfs, export
from callbacks.utils import get_report_data, medi_albertina_comment_analysis
import dash_bootstrap_components as dbc

def register_file_upload_callbacks(app):
    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True)
    def display_files(list_of_contents, list_of_names):
        if list_of_contents is None:
            raise PreventUpdate
        children = [html.Div(f"{name} ready to be processed.") for name in list_of_names]
        return children


    @app.callback(
        Output('url', 'pathname'),
        Output('loading', 'children'),
        Input('save-files-btn', 'n_clicks'),
        State('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True)
    def process_and_save_files(n_clicks, list_of_contents, list_of_names):
        if n_clicks is None or list_of_contents is None or list_of_names is None:
            raise PreventUpdate

        for content, filename in zip(list_of_contents, list_of_names):
            content_type, content_string = content.split(',')
            if 'application/pdf' in content_type:
                decoded = base64.b64decode(content_string)
                file_path = os.path.join('..', 'data', 'pdfs', 'input', filename)
                with open(file_path, 'wb') as f:
                    f.write(decoded)

        data = extract_info_from_pdfs("../data/pdfs/input")
        export(data)

        df = get_report_data()
        medi_albertina_comment_analysis(df)

        # Delete PDFs 
        for filename in list_of_names:
            os.remove(os.path.join('..', 'data', 'pdfs', 'input', filename))

        return '/single-report', None


