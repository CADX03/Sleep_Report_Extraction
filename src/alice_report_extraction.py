from utils import *

"""
Extracts relevant information from an Alice sleep report PDF.

Args:
    pdf (PDF object): The PDF object representing the Alice sleep report.

Returns:
    dict: A dictionary containing the relevant information extracted from the sleep report.
"""
def handle_alice_report(pdf):
    relevant_info = {}

    # Information missing from the report
    relevant_info["DocType"] = "Alice"
    relevant_info["ApneasDuration"] = "---"
    relevant_info["HypopneasDuration"] = "---"
    relevant_info["MixedApneasDuration"] = "---"
    relevant_info["MixedHypopneasNum"] = "---"
    relevant_info["ObstructiveApneasDuration"] = "---"
    relevant_info["ObstructiveHypopneasNum"] = "---"
    relevant_info["AtrialFibrilation"] = "---"
    relevant_info["BackPositionNumHC"] = "---"
    relevant_info["BackPositionNumHM"] = "---"
    relevant_info["BackPositionNumHO"] = "---"
    relevant_info["NonBackPositionNumHC"] = "---"
    relevant_info["NonBackPositionNumHM"] = "---"
    relevant_info["NonBackPositionNumHO"] = "---"
    relevant_info["CentralApneasDuration"] = "---"
    relevant_info["CentralHypopneasNum"] = "---"
    relevant_info["HeartRate_average"] = "---"
    relevant_info["HeartRate_highest"] = "---"
    relevant_info["HeartRate_lowest"] = "---"

    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()

        if("RELATÓRIO DE ANÁLISE" in text):

            ID = text.split("ID do paciente: ")[1].split(",")[0]
            exam_date = text.split("Iniciado : ")[1].split(" às")[0]

            gender = text.split("Sexo : ")[1].split("Iniciado")[0]
            patient_info_line = text.split("Idade do paciente : ")[1].split("\n")[0]
            patient_age = patient_info_line.split(" anos")[0]
            duration = patient_info_line.split(" Duração : ")[1].split("(")[1].split(" min")[0]
            recording_type = text.split("Tipo : ")[1].split("\n")[0]
            report_notes = text.split("Idade do paciente : ")[1].split("\n", 1)[1].split("Pneumologista,")[0]
            IMC = text.split("IMC: ")[1].split(";")[0] if ("IMC" in report_notes) else "---"
            device = f"Alice Sleepware{text.split('Sleepware')[1].split(')')[0]}" if ("Sleepware" in text) else "---"
            weight = text.split("Peso: ")[1].split(" ")[0] if ("Peso: " in text) else "---"
            height = text.split("Altura: ")[1].split(" ")[0] if ("Altura: " in text) else "---"
            occupation = text.split("Profissão: ")[1].split("\n")[0] if ("Profissão: " in text) else "---"

            #grab text from "Polissonografia revista" to the end of the current page
            polysomnography_review = "Polissonografia revista" + text.split("Polissonografia revista")[1].split("\n\n")[0] if ("Polissonografia revista" in text) else "---"   

            names = text.split("Cardiopneumologista,\n")[1].split("\n")[0] if ("Cardiopneumologista" in text) else "---"

            if names != "---":
                number_of_names = int(len(names.split(" "))/2)
                technician = ""

                for i in range(number_of_names):
                    technician += names.split(" ")[number_of_names + i] + " "
            else:
                technician = "---"

            relevant_info["ID"] = ID
            relevant_info["ExamDate"] = exam_date
            relevant_info["Age"] = patient_age
            relevant_info["Gender"] = gender
            relevant_info["Weight"] = weight
            relevant_info["Height"] = height
            relevant_info["Occupation"] = occupation
            relevant_info["Type"] = recording_type
            relevant_info["TimeInBed"] = duration
            relevant_info["Comments"] = report_notes
            relevant_info["AASMCriteria"] = polysomnography_review  
            relevant_info["Device"] = device
            relevant_info["BMI"] = IMC
            relevant_info["Technician"] = technician

            """
            print(f"ID: {ID}\n")
            print(f"Exam date: {exam_date}\n")
            print(f"Patient age: {patient_age}\n")    
            print(f"Duration: {duration}\n")
            print(f"Weigth: {weight}\n")
            print(f"Height: {height}\n")
            print(f"Occupation: {occupation}\n")
            print(f"Type: {recording_type}\n")
            print(f"Report notes: {report_notes}\n")
            print(f"Polysomnography review: {polysomnography_review}\n")
            print(f"Device: {device}\n")
            print(f"IMC: {IMC}\n")
            print(f"Technician: {technician}\n")
            """

        if("DADOS DO SONO 1" in text):

            first_table = tables[0]

            tts_duration = text.split("TTS : ")[1].split("\n")[0]
            rem_duration = text.split("REM : ")[1].split("\n")[0]
            nrem_duration = text.split("NREM : ")[1].split("\n")[0]
            sleep_efficiency = text.split("Eficiência do sono 1 :")[1].split("%")[0]
            rem_latency = first_table[5][2]
            phase_2_latency = first_table[3][2]


            relevant_info["TTS"] = extract_floats(tts_duration)[0]
            relevant_info["REMduration"] = extract_floats(rem_duration)[0]
            relevant_info["NREMduration"] = extract_floats(nrem_duration)[0]
            relevant_info["REMlatency"] = extract_floats(rem_latency)[0]
            relevant_info["SleepEfficiency"] = extract_floats(sleep_efficiency)[0]
            relevant_info["Phase2Latency"] = extract_floats(phase_2_latency)[0]

            """
            print(f"TTS duration: {relevant_info['TTS']}\n")
            print(f"REM duration: {relevant_info['REMduration']}\n")
            print(f"NREM duration: {relevant_info['NREMduration']}\n")
            print(f"REM latency: {relevant_info['REMlatency']}\n")
            print(f"Sleep efficiency: {relevant_info['SleepEfficiency']}\n")
            print(f"Phase 2 latency: {relevant_info['Phase2Latency']}\n")
            """

        if("DADOS DO SONO 2" in text):
            first_table = tables[0]

            N1_tts = first_table[4][5]
            N2_tts = first_table[5][5]
            N3_tts = first_table[6][5]

            rem_tts = first_table[3][5]

            relevant_info["N1tts"] = extract_floats(N1_tts)[0]
            relevant_info["N2tts"] = extract_floats(N2_tts)[0]
            relevant_info["N3tts"] = extract_floats(N3_tts)[0]
            relevant_info["REMtts"] = extract_floats(rem_tts)[0]

            """
            print(f"N1 TTS: {N1_tts}\n")
            print(f"N2 TTS: {N2_tts}\n")
            print(f"N3 TTS: {N3_tts}\n")
            print(f"REM TTS: {rem_tts}\n")
            """

        if("EVENTOS RESPIRATÓRIOS 3" in text):        

            first_table = tables[0]
            third_table = tables[2]

            AHI = first_table[1][6]
            AHI_TTS = first_table[7][6]

            apneas_total = first_table[1][4]
            apneas_total_index = first_table[7][4]

            central_apneas_num = first_table[1][1]

            hypopneas_total = first_table[1][5]
            hypopneas_total_index = first_table[7][5]

            mixed_apneas_num = first_table[1][3]

            obstructive_apneas_num = first_table[1][2]

            RDI = third_table[2][3]

            relevant_info["AHI"] = extract_floats(AHI)[0]
            relevant_info["AHI.TTS"] = extract_floats(AHI_TTS)[0]
            relevant_info["ApneasTotal"] = extract_floats(apneas_total)[0]
            relevant_info["ApneasTotalIndex"] = extract_floats(apneas_total_index)[0]
            relevant_info["CentralApneasNum"] = extract_floats(central_apneas_num)[0]
            relevant_info["HypopneasTotalNum"] = extract_floats(hypopneas_total)[0]
            relevant_info["HypopneasTotalIndex"] = extract_floats(hypopneas_total_index)[0]
            relevant_info["MixedApneasNum"] = extract_floats(mixed_apneas_num)[0]
            relevant_info["ObstructiveApneasNum"] = extract_floats(obstructive_apneas_num)[0]
            relevant_info["RDI"] = extract_floats(RDI)[0]

            """
            print(f"AHI: {AHI}\n")
            print(f"AHI.TTS: {AHI_TTS}\n")
            print(f"Apneas Total: {apneas_total}\n")
            print(f"Apneas Total Index: {apneas_total_index}\n")
            print(f"Central Apneas Num: {central_apneas_num}\n")
            print(f"Hypopneas Total Num: {hypopneas_total}\n")
            print(f"Hypopneas Total Index: {hypopneas_total_index}\n")
            print(f"Mixed Apneas Num: {mixed_apneas_num}\n")
            print(f"Obstructive Apneas Num: {obstructive_apneas_num}\n")
            print(f"RDI: {RDI}\n")
            """


        if("RESUMO DA OXIMETRIA" in text):

            #pdfplumber treats the "Evolução da oximetria" plot as a (sometimes many) table(s) when it exists, 
            #so we must use negative indexes to always target the last table
            first_table = tables[-2]
            second_table = tables[-1]

            dessaturation_under_90 = first_table[9][8]
            dessat_index= second_table[4][4]
            dessat_num = second_table[3][4]
            SaO2_mean = second_table[2][4]
            
            SaO2_min = text.split("Mínimo dos níveis mín. de SpO2 do evento resp. (%) : ")[1].split("\n")[0]

            relevant_info["Desaturation<90%"] = extract_floats(dessaturation_under_90)[0]
            relevant_info["DesaturationIndex"] = extract_floats(dessat_index)[0]
            relevant_info["OxygenDesaturationEvents"] = extract_floats(dessat_num)[0]
            relevant_info["SaO2mean"] = extract_floats(SaO2_mean)[0]
            relevant_info["SaO2min"] = extract_floats(SaO2_min)[0]
            
            """
            print(f"dessaturation under 90%: {relevant_info['Desaturation<90%']}\n")
            print(f"dessaturation index: {relevant_info['DesaturationIndex']}\n")
            print(f"O2 dessat events: {relevant_info['OxygenDesaturationEvents']}\n")
            print(f"média dos níveis mín. de spo2 do evento resp: {relevant_info['SaO2mean']}\n")
            print(f"mínimo dos níveis mín. de spo2 do evento resp: {relevant_info['SaO2min']}\n")
            """
        
        if("Resumo de despertares respiratórios" in text):
            
            first_table = tables[0]
            apnea_arousals = first_table[7][7]
            apnea_arousals_index = first_table[7][8]
            
            relevant_info["ApneaArousals"] = apnea_arousals
            relevant_info["ApneaArousalsIndex"] = apnea_arousals_index

            """
            print(f"Apnea arousals: {apnea_arousals}\n")
            print(f"Apnea arousals index: {apnea_arousals_index}\n")
            """

        if("RESUMO DE MOVIMENTOS DE PERNAS" in text):

            legs_movement_num = text.split("Movimentos de pernas ")[1].split(" ")[0]
            legs_movement_index = text.split("Movimentos de pernas ")[1].split(" ")[1].split("\n")[0]

            relevant_info["LegsMovementNum"] = legs_movement_num
            relevant_info["LegsMovementIndex"] = legs_movement_index

            """
            print(f"Legs movement num: {legs_movement_num}\n")
            print(f"Legs movement index: {legs_movement_index}\n")
            """

        if("Número total de episódios MPM" in text):

            PLM_num = text.split("Número total de episódios MPM : ")[1].split("\n")[0] if len(text.split("Número total de episódios MPM : ")) > 1 else "---"
            
            relevant_info["PLM_Num"] = PLM_num
            
            """
            print(f"PLM num: {PLM_num}\n")
            """
            
        if("Tempo total com MPM" in text):

            PLM_duration = text.split("Tempo total com MPM : ")[1].split("min")[0]

            relevant_info["PLM_Duration"] = PLM_duration

            """
            print(f"PLM duration: {PLM_duration}\n")
            """

        if("Índice de episódios MPM (nº/h)"):

            PLM_index = text.split("Índice de episódios MPM (nº/h) : ")[1].split("\n")[0] if len(text.split("Índice de episódios MPM (nº/h) : ")) > 1 else "---"
            
            relevant_info["PLM_Index"] = PLM_index
            
            """
            print(f"PLM index: {PLM_index}\n")
            """

        if("Índice de despertares" in text):

            awakenings_index =  extract_floats(text.split("Índice de despertares : ")[1].split("\n")[0])[0]

            relevant_info["AwakeningsIndex"] = awakenings_index
            
            """
            print(f"Awakenings index: {awakenings_index}\n")
            """

        if("RESUMO DE RONCO" in text):

            total_snore_eps = text.split("Número total de episódios de ronco : ")[1].split("\n")[0]
            total_snoring_time = text.split("Duração total com ronco : ")[1].split("min")[0]

            relevant_info["SnoreNum"] = total_snore_eps
            relevant_info["SnoreDuration"] = total_snoring_time

            """
            print(f"Total snore episodes: {total_snore_eps}\n")
            print(f"Total snoring time: {total_snoring_time}\n")
            """

        if("Distribuição da posição corporal (PTS)" in text):

            first_table = tables[0]
            back_position_duration = str(safe_float(first_table[4][2]) + safe_float(first_table[5][2]) + safe_float(first_table[7][2]))
            non_back_position_duration = str(safe_float(first_table[1][2]) + safe_float(first_table[2][2]) + safe_float(first_table[3][2]) + safe_float(first_table[6][2]) + safe_float(first_table[8][2]))
            
            relevant_info["BackPositionDuration"] = back_position_duration
            relevant_info["NonBackPositionDuration"] = non_back_position_duration

            """
            print(f"Back position duration: {back_position_duration}\n")
            print(f"Non back position duration: {non_back_position_duration}\n")
            """

        if("Distribuição de despertares respiratórios da posição do corpo (TTS)" in text):
            
            first_table = tables[0]
            back_position_num_a = str(safe_float(first_table[5][7]) + safe_float(first_table[6][7]) + safe_float(first_table[8][7]))
            back_position_num_ac = str(safe_float(first_table[5][1]) + safe_float(first_table[6][1]) + safe_float(first_table[8][1]))
            back_position_num_am = str(safe_float(first_table[5][5]) + safe_float(first_table[6][5]) + safe_float(first_table[8][5]))
            back_position_num_ao = str(safe_float(first_table[5][3]) + safe_float(first_table[6][3]) + safe_float(first_table[8][3]))
            back_position_num_h = str(safe_float(first_table[5][9]) + safe_float(first_table[6][9]) + safe_float(first_table[8][9]))

            non_back_position_num_a = str(safe_float(first_table[2][7]) + safe_float(first_table[3][7]) + safe_float(first_table[4][7]) + safe_float(first_table[7][7]) + safe_float(first_table[9][7]))
            non_back_position_num_ac = str(safe_float(first_table[2][1]) + safe_float(first_table[3][1]) + safe_float(first_table[4][1]) + safe_float(first_table[7][1]) + safe_float(first_table[9][1]))
            non_back_position_num_am = str(safe_float(first_table[2][5]) + safe_float(first_table[3][5]) + safe_float(first_table[4][5]) + safe_float(first_table[7][5]) + safe_float(first_table[9][5]))
            non_back_position_num_ao = str(safe_float(first_table[2][3]) + safe_float(first_table[3][3]) + safe_float(first_table[4][3]) + safe_float(first_table[7][3]) + safe_float(first_table[9][3]))
            non_back_position_num_h = str(safe_float(first_table[2][9]) + safe_float(first_table[3][9]) + safe_float(first_table[4][9]) + safe_float(first_table[7][9]) + safe_float(first_table[9][9]))

            relevant_info["BackPositionNumA"] = back_position_num_a
            relevant_info["BackPositionNumAC"] = back_position_num_ac
            relevant_info["BackPositionNumAM"] = back_position_num_am
            relevant_info["BackPositionNumAO"] = back_position_num_ao
            relevant_info["BackPositionNumH"] = back_position_num_h

            relevant_info["NonBackPositionNumA"] = non_back_position_num_a
            relevant_info["NonBackPositionNumAC"] = non_back_position_num_ac
            relevant_info["NonBackPositionNumAM"] = non_back_position_num_am
            relevant_info["NonBackPositionNumAO"] = non_back_position_num_ao
            relevant_info["NonBackPositionNumH"] = non_back_position_num_h

            """
            print(f"Back position num A: {back_position_num_a}\n")
            print(f"Back position num AC: {back_position_num_ac}\n")
            print(f"Back position num AM: {back_position_num_am}\n")
            print(f"Back position num AO: {back_position_num_ao}\n")
            print(f"Back position num H: {back_position_num_h}\n")

            print(f"Non back position num A: {non_back_position_num_a}\n")
            print(f"Non back position num AC: {non_back_position_num_ac}\n")
            print(f"Non back position num AM: {non_back_position_num_am}\n")
            print(f"Non back position num AO: {non_back_position_num_ao}\n")
            print(f"Non back position num H: {non_back_position_num_h}\n")
            """

    return relevant_info
