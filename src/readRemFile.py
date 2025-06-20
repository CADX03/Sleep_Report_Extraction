import pdfplumber
import pandas as pd
import json
import re
import os

"""
Extracts relevant information from the firstpage of Polysomnography RemLogic Report.

Args:
    filename (string): The path to the Polysomnography RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polysomnography RemLogic Report.
"""

def readRemLogicFileFirstPage(filename):
    # Extract text from PDF
    with pdfplumber.open(filename) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

    # Extract data using regex patterns
    data = {}
    data["DocType"] = "Polysomnography"

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
    if match:
        lights_off_date = match.group(1)
        data["ExamDate"] = lights_off_date
    elif match1:
        lights_off_date = match1.group(1)
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

    # Extract Sleep Efficiency
    match = re.search(r'Sleep Efficiency: ([\d,]+ %)', text)
    if match:
        data["Sleep Efficiency"] = match.group(1)
    else:
        data["Sleep Efficiency"] = "N/A %"
    
    # Extract "Apnea + Hypopnea (A+H)"
    match = re.search(r'Apnea \+ Hypopnea \(A\+H\): (\d+) ([\d,\.]+)\/ h', text)
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
    
    # Extract "Obstructive Apnea"
    match = re.search(r'Obstructive Apnea: (\d+) ([\d,\.]+)\/ h', text)
    if match:
        obstructive_apnea_count = match.group(1)
        obstructive_apnea_rate = match.group(2)
        data["Obstructive Apnea"] = f"{obstructive_apnea_count} {obstructive_apnea_rate} / h"
    else:
        data["Obstructive Apnea"] = "- -"

    # Extract "Central Apnea"
    match = re.search(r'Central Apnea: (\d+) ([\d,\.]+)\/ h', text)
    if match:
        central_apnea_count = match.group(1)
        central_apnea_rate = match.group(2)
        data["Central Apnea"] = f"{central_apnea_count} {central_apnea_rate} / h"
    else:
        data["Central Apnea"] = "- -"

    # Extract "Mixed Apnea"
    match = re.search(r'Mixed Apnea: (\d+) ([\d,\.]+)\/ h', text)
    if match:
        mixed_apnea_count = match.group(1)
        mixed_apnea_rate = match.group(2)
        data["Mixed Apnea"] = f"{mixed_apnea_count} {mixed_apnea_rate} / h"
    else:
        data["Mixed Apnea"] = "- -"

    # Extract "Hypopnea (All)"
    match = re.search(r'Hypopnea \(All\) (\d+) ([\d,\.]+)\/ h', text)
    if match:
        hypopnea_count = match.group(1)
        hypopnea_rate = match.group(2)
        data["Hypopnea (All)"] = f"{hypopnea_count} {hypopnea_rate} / h"
    else:
        data["Hypopnea (All)"] = "- -"
    
    # Extract "Obstructive Hypopnea"
    match = re.search(r'Obstructive Hypopnea: (\d+) ([\d,\.]+)\/ h', text)
    if match:
        obstructive_hypopnea_count = match.group(1)
        obstructive_hypopnea_rate = match.group(2)
        data["Obstructive Hypopnea"] = f"{obstructive_hypopnea_count} {obstructive_hypopnea_rate} / h"
    else:
        data["Obstructive Hypopnea"] = "- -"

    # Extract "Central Hypopnea"
    match = re.search(r'Central Hypopnea: (\d+) ([\d,\.]+)\/ h', text)
    if match:
        central_hypopnea_count = match.group(1)
        central_hypopnea_rate = match.group(2)
        data["Central Hypopnea"] = f"{central_hypopnea_count} {central_hypopnea_rate} / h"
    else:
        data["Central Hypopnea"] = "- -"

    # Extract "Mixed Hypopnea"
    match = re.search(r'Mixed Hypopnea: (\d+) ([\d,\.]+)\/ h', text)
    if match:
        mixed_hypopnea_count = match.group(1)
        mixed_hypopnea_rate = match.group(2)
        data["Mixed Hypopnea"] = f"{mixed_hypopnea_count} {mixed_hypopnea_rate} / h"
    else:
        data["Mixed Hypopnea"] = "- -"

    # Extract "Snore Time"
    match1 = re.search(r'Snore Time: (\d+,?\d*) minutes ([\d,\.]+)%', text)
    match = re.search(r"Snore\sTime:\s(\d{1,3},\d)minutes\s(\d{1,2},\d{1})%", text)
    if match:
        snore_time_minutes = match.group(1)
        snore_time_percentage = match.group(2)

        if ',' in snore_time_minutes:
            snore_time_minutes = snore_time_minutes.replace(',', '.')

        data["Snore Time"] = f"{snore_time_minutes} minutes {snore_time_percentage}%"
        data["SnoreDuration"] = snore_time_minutes
    elif match1:
        snore_time_minutes = match1.group(1)
        snore_time_percentage = match1.group(2)

        if ',' in snore_time_minutes:
            snore_time_minutes = snore_time_minutes.replace(',', '.')

        data["Snore Time"] = f"{snore_time_minutes} minutes {snore_time_percentage}%"
        data["SnoreDuration"] = snore_time_minutes
    else:
        data["Snore Time"] = "- minutes - %"
        data["SnoreDuration"] = "N/A"
    
    return data

"""
Extracts a page by their title of Polysomnography RemLogic Report.

Args:
    pdf_file (string): The path to the Polysomnography RemLogic Report.
    title (string): The Title of the page. 
Returns:
    page: The page with that title of Polysomnography RemLogic Report.
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
Extracts the lines the Apnea/Hypopnea Statistics Table of Polysomnography RemLogic Report.

Args:
    filename (string): The path to the Polysomnography RemLogic Report.
    start_line (int): The start Line. 
    end_line (int): The End Line.

Returns:
    list: The lines the Apnea/Hypopnea Statistics Table of Polysomnography RemLogic Report.
"""

def extract_lines_from_pdf(filename, start_line, end_line):
    lines = []
    page = extract_page_by_title(filename, 'Apnea/Hypopnea Statistics')
    text = page.extract_text()
    if text:
        lines.extend(text.split('\n'))
    
    # Ensure we only return the lines between start_line and end_line (1-based index)
    return lines[start_line-1:end_line]


"""
Extracts relevant information from the Apenea Table of Polysomnography RemLogic Report.

Args:
    filename (string): The path to the Polysomnography RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polysomnography RemLogic Report.
"""

def readFromApeneaTable(filename):
    text = extract_page_by_title(filename, 'Apnea/Hypopnea Statistics')

    lines = extract_lines_from_pdf(filename, 4, 11)
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
                "A or H/h": components[4]
            }
            data['HypopneasTotalNum'] =  components[2]
        else: 
            entry = {
                "Respiration": components[0],
                "Number": components[1],
                "A or H/h": components[3]
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
Extracts relevant information from the Middle of Polysomnography RemLogic Report.

Args:
    filename (string): The path to the Polysomnography RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polysomnography RemLogic Report.
"""

def readMiddleFile(filename):
    #Find page where I have Snoring Statistics
    page = extract_page_by_title(filename, 'Snoring Statistics')
    text = page.extract_text()

    data = {}

    # Extract "Relative Snoring Time"
    match = re.search(r'Relative Snoring Time: ([\d,\.]+) %', text)
    if match:
        relative_snoring_time = match.group(1)
        data["Relative Snoring Time"] = f"{relative_snoring_time} %"
    else:
        data["Relative Snoring Time"] = "- %"

    # Extract "Number of Snoring Episodes"
    match = re.search(r'Number of Snoring Episodes: ([\d,\.]+)', text)
    if match:
        number_snoring = match.group(1)
        data["Number of Snoring Episodes"] = f"{number_snoring}"
    else:
        data["Number of Snoring Episodes"] = "-"

    #Find page where I have SpO2 Statistics
    page = extract_page_by_title(filename, 'SpO2 Statistics')
    text = page.extract_text()

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
    match = re.search(r'Saturation < 90%: (\d+\,\d+ minutes) (\d+\,\d+ %)', text)
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

    #Find page where I have Cardiac Events
    page = extract_page_by_title(filename, 'Cardiac Events')
    text = page.extract_text()

    # Extract "Atrial Fibrillation"
    match = re.search(r'Atrial Fibrillation: (\d+)', text)
    if match:
        atrial_fibrillation_value = match.group(1)
        data["Atrial Fibrillation"] = f"{atrial_fibrillation_value}"
    else:
        data["Atrial Fibrillation"] = "-"
    
    return data

"""
Extracts the lines the Position Statistics Table of Polysomnography RemLogic Report.

Args:
    filename (string): The path to the Polysomnography RemLogic Report.

Returns:
    list: The lines the Position Statistics Table of Polysomnography RemLogic Report.
"""
def extract_lines_from_pdf_Position(filename):
    lines = []
    page = extract_page_by_title(filename, 'Position Statistics')
    text = page.extract_text()

    if text:
        lines.extend(text.split('\n'))
    
    # Find the line number that contains 'Position Statistics'
    for i, line in enumerate(lines):
        if 'Position Statistics' in line:
            position_line_number = i
            break
    else:
        return "Position Statistics not found in the text."

    # Ensure we only return the lines between start_line and end_line (1-based index)
    return lines[position_line_number+3:position_line_number+9]

"""
Extracts relevant information from the Position Statistics Table of Polysomnography RemLogic Report.

Args:
    filename (string): The path to the Polysomnography RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polysomnography RemLogic Report.
"""

def readPosStatisticsTable(filename):
    lines = extract_lines_from_pdf_Position(filename)
    data = {}
    data["position"] = []
    for line in lines:
        # Split the line into components
        components = line.split()
        
        entry = {
            "Position": components[0],
            "Index time": components[1],
            "A or H/h": components[3]
        }

        data["position"].append(entry)

    return data

"""
Extracts relevant information from the Comments of Polysomnography RemLogic Report.

Args:
    filename (string): The path to the Polysomnography RemLogic Report.

Returns:
    dict: A dictionary containing the relevant information extracted from the Polysomnography RemLogic Report.
"""

def readComments(filename):
    with pdfplumber.open(filename) as pdf:
        for page_number in [8, 9]:
            if page_number < len(pdf.pages):
                page = pdf.pages[page_number]
                text = page.extract_text()
                if "Pneumologista" in text:
                    index = text.find("Pneumologista")
                    index1 = text.find(",", 0, index)
                    extracted_text = text[index1+1:index].strip()
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
    data.update(readPosStatisticsTable(filename))
    data.update(readComments(filename))
    return data


#readFile('../159.pdf')

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

#json_to_csv('./json', 'RemLogicData.csv')
