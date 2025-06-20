import pdfplumber
import pandas as pd
import json
import re
import os

"""
Extracts relevant information from the firstpage of Polygraphy RemLogic Report.

Args:
    filename (string): The path to the Polygraphy RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polygraphy RemLogic Report.
"""

def readRemLogicFileFirstPage(filename):
    # Extract text from PDF
    with pdfplumber.open(filename) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

    # Extract data using regex patterns
    data = {}
    data["DocType"] = "Polygraphy"

    # Extract "Total Recording Time"
    match = re.search(r'\( (\d+) minutes \)', text)
    if match:
        total_recording_time = match.group(1)
        data["TimeInBed"] = total_recording_time

    # Extract "ID"
    match = re.search(r'ID: (\d+)', text)
    if match:
        idi = match.group(1)
        data["ID"] = f"{idi}"

    # Extract Date of Exam
    match = re.search(r'Lights Off Clock Time: (\d{2}-\d{2}-\d{4}) \d{2}:\d{2}', text)
    match1 = re.search(r"Lights\sOff\sClock\sTime:\s(\d{2}-\d{2}-\d{4})\s(\d{1,2}:\d{2})", text)
    match2 = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    if match:
        lights_off_date = match.group(1)
        data["ExamDate"] = lights_off_date
    elif match1:
        lights_off_date = match1.group(1)
        data["ExamDate"] = lights_off_date
    elif match2:
        lights_off_date = match2.group(1)
        data["ExamDate"] = lights_off_date
    
    # Extract "Age"
    match = re.search(r'Age: (\d+) year\(s\)', text)
    if match:
        data["Age"] = match.group(1)
    else:
        data["Age"] = "N/A"

    # Extract "Gender"
    match = re.search(r'Gender: (\w+)', text)
    if match:
        data["Gender"] = match.group(1)

    # Extract "Height"
    match = re.search(r'Height: ([\d,]+) m', text)
    if match:
        height = match.group(1)
        if ',' in height:
            height = height.replace(',', '.')
        data["Height"] = height
    else:
        data["Height"] = "N/A"

    # Extract "Weight"
    match = re.search(r'Weight: ([\d,]+) kg', text)
    if match:
        weight = match.group(1)
        if ',' in weight:
            weight = weight.replace(',', '.')
        data["Weight"] = weight
    else:
        data["Weight"] = "N/A"

    # Extract "BMI"
    match = re.search(r'BMI: ([\d,]+)', text)
    if match:
        data["BMI"] = match.group(1)
    else:
        data["BMI"] = "N/A"
    
    # Extract "Index Time"
    match = re.search(r"Index Time:\s*(\d{1,3},\d)\s*minutes", text)
    if match:
        index_time = match.group(1)
        data["Index Time"] = f"{index_time} minutes"
    else:
        data["Index Time"] = "N/A"

    # Extract "Apnea + Hypopnea (A+H)"
    match = re.search(r"Apnea \+ Hypopnea \(A\+H\):\s*(\d+)\s+(\d{1,3},\d)\s*/\s*h", text)
    if match:
        apnea_hypopnea_count = match.group(1)
        apnea_hypopnea_rate = match.group(2)

        if ',' in apnea_hypopnea_rate:
            apnea_hypopnea_rate = apnea_hypopnea_rate.replace(',', '.')

        data["Apnea + Hypopnea (A+H)"] = f"{apnea_hypopnea_count} {apnea_hypopnea_rate} / h"
        data["AHI"] = apnea_hypopnea_count 
        data["AHI.TTS"] = apnea_hypopnea_rate
    else:
        data["Apnea + Hypopnea (A+H)"] = "- -"
        data["AHI"] = "N/A" 
        data["AHI.TTS"] = "N/A"

    # Extract "Supine A+H"
    match = re.search(r"Supine A\+H:\s*(\d+)\s+(\d{1,3},\d)\s*/\s*h", text)
    if match:
        supine_count = match.group(1)
        supine_rate = match.group(2)
        data["Supine A+H"] = f"{supine_count} {supine_rate} / h"
    else:
        data["Supine A+H"] = "- -"

    # Extract "Non-Supine A+H"
    match = re.search(r"Non-Supine A\+H:\s*(\d+)\s+(\d{1,3},\d)\s*/\s*h", text)
    match1 = re.search(r"Non-Supine A\+H:\s*(\d+)\s*-\s*/\s*h", text)
    if match:
        non_supine_count = match.group(1)
        non_supine_rate = match.group(2)
        data["Non-Supine A+H"] = f"{non_supine_count} {non_supine_rate} / h"
    elif match1:
        non_supine_count = match1.group(1)
        data["Non-Supine A+H"] = f"{non_supine_count} - / h"
    else:
        data["Non-Supine A+H"] = "- -"

    # Extract "RDI"
    match = re.search(r'RDI: ([\d,]+)', text)
    if match:
        data["RDI"] = match.group(1)
    else:
        data["RDI"] = "N/A"

    # Extract "Supine Time"
    match = re.search(r"Supine Time:\s*(\d{1,3},\d)\s*minutes\s*(\d{1,3},\d)\s*%", text)
    if match:
        supine_time_count = match.group(1)
        supine_time_rate = match.group(2)
        data["Supine Time"] = f"{supine_time_count} minutes {supine_time_rate} %"
    else:
        data["Supine Time"] = "- -"
    
    # Extract "Non-Supine Time"
    match = re.search(r"Non-Supine Time:\s*(\d{1,3},\d)\s*minutes\s*(\d{1,3},\d)\s*%", text)
    if match:
        non_supine_time_count = match.group(1)
        non_supine_time_rate = match.group(2)
        data["Non-Supine Time"] = f"{non_supine_time_count} minutes {non_supine_time_rate} %"
    else:
        data["Non-Supine Time"] = "- -"

    # Extract "Upright Time"
    match = re.search(r"Upright Time:\s*(\d{1,3},\d)\s*minutes\s*(\d{1,3},\d)\s*%", text)
    if match:
        upright_time_count = match.group(1)
        upright_time_rate = match.group(2)
        data["Upright Time"] = f"{upright_time_count} minutes {upright_time_rate} %"
    else:
        data["Upright Time"] = "- -"

    # Extract "Movement Time"
    match = re.search(r"Movement Time:\s*(\d{1,3},\d)\s*minutes\s*(\d{1,3},\d)\s*%", text)
    if match:
        movement_time_count = match.group(1)
        movement_time_rate = match.group(2)
        data["Movement Time"] = f"{movement_time_count} minutes {movement_time_rate} %"
    else:
        data["Movement Time"] = "- -"

    # Extract "Average Oxygen Saturation"
    match = re.search(r"Average Oxygen Saturation:\s*(\d{1,3},\d)\s*%", text)
    if match:
        average_oxygen_rate = match.group(1)
        data["Average Oxygen Saturation"] = f"{average_oxygen_rate} %"
    else:
        data["Average Oxygen Saturation"] = "- %"

    # Extract "Oxygen Desaturation Events (OD)"
    match = re.search(r"Oxygen Desaturation Events \(OD\):\s*(\d+)\s+(\d{1,3},\d)\s*/\s*h", text)
    if match:
        od_count = match.group(1)
        od_rate = match.group(2)
        data["Oxygen Desaturation Events"] = f"{od_count} {od_rate} / h"
    else:
        data["Oxygen Desaturation Events"] = "- -"

    # Extract "Snore Time"
    match = re.search(r"Snore Time:\s*(\d{1,3},\d)\s*minutes\s*(\d{1,3},\d)\s*%", text)
    if match:
        snore_time_minutes = match.group(1)
        snore_time_percentage = match.group(2)

        if ',' in snore_time_minutes:
            snore_time_minutes = snore_time_minutes.replace(',', '.')

        data["Snore Time"] = f"{snore_time_minutes} minutes {snore_time_percentage}%"
        data["SnoreDuration"] = snore_time_minutes
    else:
        data["Snore Time"] = "- minutes - %"
        data["SnoreDuration"] = "N/A"

    # Extract "RDI"
    match = re.search(r'Number of Snoring Episodes: ([\d,]+)', text)
    if match:
        data["Number of Snoring Episodes"] = match.group(1)
    else:
        data["Number of Snoring Episodes"] = "N/A"

    # Extract "Autonomic Arousal"
    match = re.search(r"Autonomic Arousal \s*(\d+)\s+(\d{1,3},\d)\s*/\s*h", text)
    if match:
        autonomic_count = match.group(1)
        autonomic_rate = match.group(2)
        data["Autonomic Arousal"] = f"{autonomic_count} {autonomic_rate} / h"
    else:
        data["Autonomic Arousal"] = "- -"
    
    return data

"""
Extracts a page by their title of Polygraphy RemLogic Report.

Args:
    pdf_file (string): The path to the Polygraphy RemLogic Report.
    title (string): The Title of the page. 
Returns:
    page: The page with that title of Polygraphy RemLogic Report.
"""

def extract_page_by_title(pdf_file, title):
    with pdfplumber.open(pdf_file) as pdf:
        # Iterate through each page
        for page in pdf.pages:
            # Extract text from the current page
            text = page.extract_text()
            
            # Check if the title is in the extracted text
            if title in text:
                return page  # Return the page object if title found
    
    return None  # Return None if title not found

"""
Extracts the lines the Apnea/Hypopnea Statistics Table of Polygraphy RemLogic Report.

Args:
    filename (string): The path to the Polygraphy RemLogic Report.

Returns:
    list: The lines the Apnea/Hypopnea Statistics Table of Polygraphy RemLogic Report.
"""
def extract_lines_from_pdf_Position(filename):
    lines = []
    page = extract_page_by_title(filename, 'Apnea/Hypopnea Statistics')
    text = page.extract_text()

    if text:
        lines.extend(text.split('\n'))
    
    # Find the line number that contains 'Position Statistics'
    for i, line in enumerate(lines):
        if 'Apnea/Hypopnea Statistics' in line:
            position_line_number = i
            break
    else:
        return "Position Statistics not found in the text."

    # Ensure we only return the lines between start_line and end_line (1-based index)
    return lines[position_line_number+3:position_line_number+12]


"""
Extracts relevant information from the Apenea Table of Polygraphy RemLogic Report.

Args:
    filename (string): The path to the Polygraphy RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polygraphy RemLogic Report.
"""

def readFromApeneaTable(filename):
    lines = extract_lines_from_pdf_Position(filename)
    data = {}
    data["apenea"] = []
    for idx, line in enumerate(lines):
        # Split the line into components
        components = line.split()
        
        # Ensure the line has enough components to avoid IndexError
        if len(components) == 9:
            entry = {
                "Respiration": components[0] + " " + components[1],
                "Number": components[2],
                "Mean [seconds]": components[7]
            }
            data['HypopneasTotalNum'] =  components[2]
        elif len(components) == 7:
            entry = {
                "Respiration": components[0],
                "Number": components[1],
                "Mean [seconds]": components[5]
            }
        else: 
            entry = {
                "Respiration": components[0],
                "Number": components[1],
                "Mean [seconds]": components[6]
            }
        if (idx == 0):
            data['ApneasTotal'] = components[1]
        elif (idx == 1):
            data['ObstructiveApneasNum'] = components[1]
        elif (idx == 2):
            data['CentralApneasNum'] = components[1]
        elif (idx == 3):
            data['MixedApneasNum'] = components[1]

        data["apenea"].append(entry)

    return data

"""
Extracts relevant information from the Middle of Polygraphy RemLogic Report.

Args:
    filename (string): The path to the Polygraphy RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polygraphy RemLogic Report.
"""

def readMiddleFile(filename):
    #Find page where I have SpO2 Statistics
    page = extract_page_by_title(filename, 'SpO2 Statistics')
    text = page.extract_text()

    data = {}

    # Extract "Lowest Oxygen Saturation"
    match = re.search(r'Lowest Oxygen Saturation: ([\d,\.]+) %', text)
    if match:
        lower_oxygen_saturation = match.group(1)

        if ',' in lower_oxygen_saturation:
            lower_oxygen_saturation = lower_oxygen_saturation.replace(',', '.')

        data["SaO2min"] = lower_oxygen_saturation
    else:
        data["SaO2min"] = "N/A"

    # Extract "Saturation < 90%"
    match = re.search(r'Saturation < 90%: (\d+\,\d+) minutes (\d+\,\d+ %)', text)
    match1 = re.search(r"Saturation\s<\s90%:\s(\d+)\sminutes\s(\d{1,2},\d{1})\s%", text)
    if match:
        saturation_minutes = match.group(1)
        saturation_percentage = match.group(2)

        if ',' in saturation_minutes:
            saturation_minutes = saturation_minutes.replace(',', '.')

        data["Saturation < 90%"] = f"{saturation_minutes} minutes {saturation_percentage}%"
        data["Desaturation<90%"] = saturation_minutes
    elif match1:
        saturation_minutes = match1.group(1)
        saturation_percentage = match1.group(2)

        if ',' in saturation_minutes:
            saturation_minutes = saturation_minutes.replace(',', '.')

        data["Saturation < 90%"] = f"{saturation_minutes} minutes {saturation_percentage}%"
        data["Desaturation<90%"] = saturation_minutes
    else:
        data["Saturation < 90%"] = "- - %"
        data["Desaturation<90%"] = "N/A"

    return data

"""
Extracts relevant information from the Comments of Polygraphy RemLogic Report.

Args:
    filename (string): The path to the Polygraphy RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polygraphy RemLogic Report.
"""

def readComments(filename):
    with pdfplumber.open(filename) as pdf:
        for page_number in [5]:
            if page_number < len(pdf.pages):
                page = pdf.pages[page_number]
                text = page.extract_text()
                if "Pneumologista" in text:
                    index = text.find("Pneumologista")
                    index1 = text.find("Em conclusão", 0, index)
                    extracted_text = text[index1:index].strip()
                    break
        else:
            extracted_text = "No comments"
    data = {}

    data["Comments"] = extracted_text
    return data



def readFile(filename):
    data = {}
    data.update(readRemLogicFileFirstPage(filename))
    data.update(readFromApeneaTable(filename))
    data.update(readMiddleFile(filename))
    data.update(readComments(filename))
    return data

#readFile("../1009803_DOM_22_05_17.pdf")

def json_to_csv(json_directory, output_csv):
    """
    Convert multiple JSON files in a directory to a single CSV file.

    Parameters:
    json_directory (str): The directory containing the JSON files.
    output_csv (str): The path to the output CSV file.
    """

    # List all JSON files in the directory
    json_files = [pos_json for pos_json in os.listdir(json_directory) if pos_json.endswith('.json')]

    # Initialize an empty list to hold the data
    data_list = []

    # Iterate over the list of JSON files
    for json_file in json_files:
        file_path = os.path.join(json_directory, json_file)
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            # Normalize the JSON data and append it to the list
            data_list.append(pd.json_normalize(json_data))

    # Concatenate all dataframes into a single dataframe
    combined_df = pd.concat(data_list, ignore_index=True)

    # Save the combined dataframe to a CSV file
    combined_df.to_csv(output_csv, index=False)

    print(f"All JSON files have been successfully combined and saved to {output_csv}.")

#json_to_csv('./jsonPoly', 'RemLogicPolyData.csv')