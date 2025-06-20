import pdfplumber
import os
import json
import csv
import pandas as pd
from alice_report_extraction import handle_alice_report
from short_report_extraction import handle_short_report
from readRemFile import readFile
from readRemPolyFile import readFile as readFilePoly


"""
Extracts relevant information from PDF files in the specified path.

Args:
    path (str): The path to the folder containing the PDF files. Defaults to "../data/pdfs/input".

Returns:
    list: A list containing dictionaries where the keys are the PDF file names and the values are the extracted relevant information.
"""
def extract_info_from_pdfs(path = "../data/pdfs/input"):

    folder_path = path
    pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

    data = []

    for pdf_file in pdf_files:
        
        
        relevant_info = None

        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"\n\n!!!!!! Extracting text from {pdf_path} !!!!!!! \n\n")

        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            first_word_first_page = first_page.extract_text().split("\n")[0].split(" ")[0]

            if("alice" in first_word_first_page.lower()): # Check if the first word of the first page is "Alice"
                relevant_info = handle_alice_report(pdf)
            elif("short report" in first_page.extract_text().lower()):
                relevant_info = handle_short_report(pdf)
            elif("polysomnography" in first_page.extract_text().lower()):
                relevant_info = readFile(pdf_path)
            elif("polygraphy" in first_page.extract_text().lower()):
                relevant_info = readFilePoly(pdf_path)
        data.append({pdf_file: relevant_info})

    return data


"""
Export data to JSON files.

Args:
data (list): A list of dictionaries containing the data to be exported.
output_directory (str): The directory where the JSON files will be saved.

Returns:
None
"""
def export_to_json(data, output_directory):
    print("Generating JSON files...\n")
    for item in data:
        for key, value in item.items():
            with open(f"{output_directory}/{key.split('.')[0]}.json", "w") as f:
                json.dump(value, f, indent=4)


"""
Export all the data to CSV files.

Args:
    data (list): A list of dictionaries containing the data to be exported.
    output_directory (str): The directory where the CSV file will be saved.

Returns:
    None
"""
def export_to_csv(data, output_directory):
    print("Generating CSV file...\n")
    all_data = pd.DataFrame()

    for item in data:
        for pdf_name, pdf_data in item.items():
            if pdf_data:  
                df = pd.json_normalize(pdf_data)
                df['SourcePDF'] = pdf_name
                
                columns = ['SourcePDF'] + [col for col in df.columns if col != 'SourcePDF']
                df = df[columns]
                
                all_data = pd.concat([all_data, df], ignore_index=True)
    
    output_path = f"{output_directory}/report_summary.csv"
    all_data.to_csv(output_path, index=False, encoding='utf-8-sig')


"""
Export the given data to JSON and CSV formats.

Args:
    data: The data to be exported.

Returns:
    None
"""
def export(data):
    output_directory_json = "../data/jsons"
    output_directory_csv = "../data/csvs"

    os.makedirs(output_directory_json, exist_ok=True)
    os.makedirs(output_directory_csv, exist_ok=True)

    export_to_json(data, output_directory_json)
    export_to_csv(data, output_directory_csv)


def main():
    data = extract_info_from_pdfs()
    export(data)
    return


if __name__ == "__main__":
    main()