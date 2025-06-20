from transformers import pipeline
from dash import html, dcc
import dash_bootstrap_components as dbc
import json
import pandas as pd
import plotly.express as px

nominal_cols = ['SourcePDF', 'Comments', 'DocType', 'ExamDate', 'Device', 'ID', 'Race', 'Occupation', 'Technician', 'RecordingType']

entity_colors = {
    "Diagnostico": "#F09EA7",
    "Sintoma": "#F6CA94",
    "Medicamento": "#FAFABE",
    "Dosagem": "#C1EBC0",
    "ProcedimentoMedico": "#C7CAFF",
    "SinalVital": "#CDABEB",
    "Progresso": "#F6C2F3"
}

def medi_albertina_comment_analysis(df):
    ner_pipeline = pipeline('ner', model='portugueseNLP/medialbertina_pt-pt_900m_NER', aggregation_strategy='average')

    entities = {}
    
    for index, row in df.iterrows():
        if row['Comments'] != pd.NaT:
            entities[row['SourcePDF']] = ner_pipeline(row['Comments'])
            entities[row['SourcePDF']] = [entity for entity in entities[row['SourcePDF']] if entity['entity_group'] != 'Resultado']

            # Convert scores to string for serialization
            for entity in entities[row['SourcePDF']]:
                entity['score'] = str(entity['score'])
                entity['start'] = str(entity['start'])
                entity['end'] = str(entity['end'])

    with open('entities.json', 'w', encoding='utf-8') as f:
        json.dump(entities, f, ensure_ascii=False, indent=4)

def clean_data(df):
    df = df.replace('---', pd.NaT)
    fix_data_types(df)
    handle_missing_values(df)
    return df
    
def fix_data_types(df):
    df['ExamDate'] = pd.to_datetime(df['ExamDate'], format='%d-%m-%Y')
    
    # Convert all columns to numeric if possible
    for col in df.columns:
        if col not in nominal_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

def handle_missing_values(df):
    # All body position stats columns have missing values replace with 0 (no events or time spent in that position)
    for col in df.columns:
        if 'Position' in col:
            df[col] = df[col].fillna(0)

    # For now we'll replace missing values with the mean, futurely maybe we can try imputing with a model (though we don't have a lot of data rn)
    for col in df.columns:
        if col not in nominal_cols:
            df[col] = df[col].fillna(df[col].mean())

def get_report_data():
    csv_file_path = '../data/csvs/report_summary.csv'
    df = pd.read_csv(csv_file_path)
    df = clean_data(df)
    return df

def load_entities():
    json_file_path = 'entities.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        entities = json.load(file)
    return entities

def highlight_entities(text, entities):
    # Sort entities by start index in reverse order so we can replace the text without messing up the indexes by adding characters to the text
    entities_sorted = sorted(entities, key=lambda e: int(e['start']), reverse=True)
    for entity in entities_sorted:
        start, end = int(entity["start"]) + 1, int(entity["end"])
        word = text[start:end]
        color = entity_colors.get(entity["entity_group"], "lightgrey")
        highlighted_word = f'<span style="background-color: {color}; font-weight: bold;">{word}</span>'
        text = text[:start] + highlighted_word + text[end:]
    return text

def generate_legend():
    legend_items = []
    for entity, color in entity_colors.items():
        legend_items.append(
            dbc.Row([
                dbc.Col(html.Div(style={"backgroundColor": color, "width": "4vh", "height": "4vh"}), width=3),
                dbc.Col(html.Span(entity), width=7, align="right")
            ], align="center")
        )
    return legend_items

def univariate_analysis(df, column_name):
    data = df[column_name]
    
    # Calculate statistics
    mean_val = data.mean()
    median_val = data.median()
    min_val = data.min()
    max_val = data.max()
    kurtosis_val = data.kurtosis()
    skewness_val = data.skew()
    std_dev = data.std()
    variance = data.var()

    return {
        'Mean': mean_val,
        'Median': median_val,
        'Min': min_val,
        'Max': max_val,
        'Kurtosis': kurtosis_val,
        'Skewness': skewness_val,
        'Standard Deviation': std_dev,
        'Variance': variance
    }

def categorize_report_data(report_data):
    #! The order matters, if a key matches multiple themes, it will be placed in the first theme that matches
    themes = {
        'Patient Information': ["Age", "Gender", "Weight", "Height", "Occupation", "BMI"],
        'Sleep Events': ["Apneas", "Hypopneas", "Apnea", "AHI", "RDI", "Awakenings"],
        'Heart Stats': ["Heart", "Fibrilation"],
        'Oxygen Stats': ["O2", "Desat"],
        'Position Stats': ["Position", "PLM", "Legs"],
        'Snore Stats': ["Snore", "Snoring"],
        'Sleep Phases': ["REM", "Phase", "tts", "TTS", "TimeInBed"],   
    }
    
    categorized_data = {theme: {} for theme in themes}
    categorized_data['Study Info'] = {}

    for key, value in report_data.items():
        if key in ["SourcePDF", "Comments", "SleepEfficiency"]:
            continue
        placed = False
        for theme, keywords in themes.items():
            if any(keyword in key for keyword in keywords):
                if value == None:
                    value = "N/A"
                if isinstance(value, float):
                    value = f"{value:.2f}"
                categorized_data[theme][key] = value
                placed = True
                break
        if not placed:
            if value == None:
                value = "N/A"
            if isinstance(value, float):
                value = f"{value:.2f}"
            categorized_data['Study Info'][key] = value
    
    return categorized_data

def format_categorized_data(categorized_data):
    tables = []
    for theme, data in categorized_data.items():
        table_header = [html.Thead(html.Tr([
            html.Th("Variable", style={'width': '55%'}), 
            html.Th("Value", style={'width': '45%'})
            ]))]
        rows = []
        sorted_items = sorted(data.items())
        for key, value in sorted_items:
            rows.append(html.Tr([html.Td(key), html.Td(value)]))
        table_body = [html.Tbody(rows)]
        table = dbc.Table(table_header + table_body, bordered=True)
        tables.extend([html.H4(theme, className="table-title"), table])
    return tables

def generate_plots(data):   
    record = data

    # Pie chart for sleep phases
    pie_fig = px.pie(values=[record["N1tts"], record["N2tts"], record["N3tts"], record["REMtts"]], 
                     names=['N1tts', 'N2tts', 'N3tts', 'REMtts'])

    # Bar chart for types of apneas and hypopneas
    apnea_types_fig = px.bar(x=['CentralApneasNum', 'CentralHypopneasNum', 'MixedApneasNum', 'MixedHypopneasNum', 
                                'ObstructiveApneasNum', 'ObstructiveHypopneasNum'],
                             y=[record[key] for key in ['CentralApneasNum', 'CentralHypopneasNum', 'MixedApneasNum', 
                                                        'MixedHypopneasNum', 'ObstructiveApneasNum', 'ObstructiveHypopneasNum']],
                             labels={'x': 'Type', 'y': 'Count'},
                             color_discrete_sequence=["#af80f9", "#ff76d6", "#ff81a7", "#ffa47b", "#ffcf63", "#f9f871"])

    # Data preparation for apneas by position
    apnea_data_per_position = {
        "Position": ["Back", "Back", "Back", "Non Back", "Non Back", "Non Back"],
        "Type": ["AC", "AM", "AO", "AC", "AM", "AO"],
        "Apneas": [record[key] for key in ['BackPositionNumAC', 'BackPositionNumAM', 'BackPositionNumAO', 
                                           'NonBackPositionNumAC', 'NonBackPositionNumAM', 'NonBackPositionNumAO']]
    }
    position_df = pd.DataFrame(apnea_data_per_position)
    position_fig = px.bar(position_df, x='Position', y='Apneas', color='Type',
                          color_discrete_map={"AC": "#af80f9", "AM": "#d5a6ff", "AO": "#f4ccff"})

    # Data preparation for hypopneas by position
    hypopnea_data_per_position = {
        "Position": ["Back", "Back", "Back", "Non Back", "Non Back", "Non Back"],
        "Type": ["HC", "HM", "HO", "HC", "HM", "HO"],
        "Hypopneas": [record[key] for key in ['BackPositionNumHC', 'BackPositionNumHM', 'BackPositionNumHO', 
                                              'NonBackPositionNumHC', 'NonBackPositionNumHM', 'NonBackPositionNumHO']]
    }
    hypopneas_df = pd.DataFrame(hypopnea_data_per_position)
    hypopneas_fig = px.bar(hypopneas_df, x='Position', y='Hypopneas', color='Type',
                           color_discrete_map={"HC": "#af80f9", "HM": "#d5a6ff", "HO": "#f4ccff"})

    # Cards for displaying figures
    cards = [
        dbc.Card(dbc.CardBody([html.H5("Sleep Phases", className="card-title"), dcc.Graph(figure=pie_fig)])),
        dbc.Card(dbc.CardBody([html.H5("Types of Apneas and Hypopneas", className="card-title"), dcc.Graph(figure=apnea_types_fig)])),
        dbc.Card(dbc.CardBody([html.H5("Apneas by Position", className="card-title"), dcc.Graph(figure=position_fig)])),
        dbc.Card(dbc.CardBody([html.H5("Hypopneas by Position", className="card-title"), dcc.Graph(figure=hypopneas_fig)]))
    ]

    return html.Div([
        dbc.Row([dbc.Col(cards[0], width=12, lg=6), dbc.Col(cards[1], width=12, lg=6)], className='mb-4'),
        dbc.Row([dbc.Col(cards[2], width=12, lg=6), dbc.Col(cards[3], width=12, lg=6)])
    ])