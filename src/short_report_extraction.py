from utils import *


"""
Extracts relevant information from short report PDF.

Args:
    pdf (PDF object): The PDF object representing the short report.

Returns:
    dict: A dictionary containing the relevant information extracted from the short report.
"""
def handle_short_report(pdf):
    relevant_info = {}

    relevant_info["DocType"] = "ShortReport"
    relevant_info["Device"] = "Acquisition Scoreset"
    relevant_info["ApneasDuration"] = "---"
    relevant_info["AtrialFibrilation"] = "---"
    relevant_info["CentralApneasDuration"] = "---"
    relevant_info["DesaturationIndex"] = "---"
    relevant_info["HeartRate_highest"] = "---"
    relevant_info["HeartRate_lowest"] = "---"
    relevant_info["HypopneasDuration"] = "---"
    relevant_info["MixedApneasDuration"] = "---"
    relevant_info["ObstructiveApneasDuration"] = "---"
    relevant_info["OxygenDesaturationEvents"] = "---"
    relevant_info["PLM_Duration"] = "---"
    relevant_info["PLM_Index"] = "---"
    relevant_info["PLM_Num"] = "---"

    for page in pdf.pages:

        text = page.extract_text()
        tables = page.extract_tables()

        if "study id" in text.lower():

            exam_date = text.split("Study Date ")[1].split("\n")[0]
            ID = text.split("Study ID ")[1].split(" ")[0]

            age = text.split(" Age ")[1].split(" ")[0]
            ht = text.split(" CM ")[1].split(" ")[0]
            wt = text.split(" KG ")[1].split(" ")[0]
            sex = text.split(" Sex ")[1].split(" ")[0]
            race = text.split(" Race ")[1].split(" ")[0]
            BMI = text.split(" BMI ")[1].split(" ")[0]
            occupation = text.split(" Occupation ")[1].split("\n")[0]

            technician = text.split("Tested By ")[1].split("\n")[0]

            time_in_bed = text.split("Time In Bed ")[1].split(" ")[0]
            tts_duration = text.split("Total Sleep Time ")[1].split(" ")[0]
            rem_duration = text.split(" REM ")[1].split(" ")[0]
            nrem_duration = text.split(" NREM ")[1].split(" ")[0]

            sleep_eff = text.split("Sleep Efficiency ")[1].split(" ")[0]

            relevant_info["ExamDate"] = exam_date
            relevant_info["ID"] = ID
            relevant_info["Age"] = age.replace(",", ".").strip()
            relevant_info["Height"] = ht.replace(",", ".").strip()
            relevant_info["Weight"] = wt.replace(",", ".").strip()
            relevant_info["Gender"] = sex
            relevant_info["Race"] = race
            relevant_info["BMI"] = BMI.replace(",", ".").strip()
            relevant_info["Occupation"] = occupation
            relevant_info["Technician"] = technician
            relevant_info["TimeInBed"] = time_in_bed.replace(",", ".").strip()
            relevant_info["TTS"] = tts_duration.replace(",", ".").strip()
            relevant_info["REMduration"] = rem_duration.replace(",", ".").strip()
            relevant_info["NREMduration"] = nrem_duration.replace(",", ".").strip()
            relevant_info["SleepEfficiency"] = sleep_eff.replace(",", ".").strip()
            
            print(f"Exam date: {exam_date}\n")
            print(f"ID: {ID}\n")
            print(f"Age: {age}\n")  
            print(f"Height: {ht}\n")
            print(f"Weight: {wt}\n")
            print(f"sex: {sex}\n")
            print(f"race: {race}\n")
            print(f"BMI: {BMI}\n")
            print(f"Occupation: {occupation}\n")
            print(f"Technician: {technician}\n")
            print(f"Time in bed: {time_in_bed}\n")
            print(f"TTS duration: {tts_duration}\n")
            print(f"REM duration: {rem_duration}\n")
            print(f"NREM duration: {nrem_duration}\n")
            print(f"Sleep Efficiency: {sleep_eff}\n")

        if "arousals + awakenings" in text.lower():

            awakenings_index = text.split("Arousals + Awakenings ")[1].split(" ")[1].split("\n")[0]

            relevant_info["AwakeningsIndex"] = awakenings_index.replace(",", ".").strip()

            print(f"Awakenings index: {awakenings_index}\n")

        if "percent stage to spt" in text.lower():
            
            N1_tts =  text.split("Percent Stage to SPT ")[1].split(" ")[2]
            N2_tts =  text.split("Percent Stage to SPT ")[1].split(" ")[3]
            N3_tts =  text.split("Percent Stage to SPT ")[1].split(" ")[4]
            rem_tts = text.split("Percent Stage to SPT ")[1].split(" ")[5]
            rem_latency = text.split("Latency To Stage ")[1].split(" ")[5]
            phase_2_lantency = text.split("Latency To Stage ")[1].split(" ")[2]
            
            relevant_info["N1tts"] = N1_tts.replace(",", ".").strip()
            relevant_info["N2tts"] = N2_tts.replace(",", ".").strip()
            relevant_info["N3tts"] = N3_tts.replace(",", ".").strip()
            relevant_info["REMtts"] = rem_tts.replace(",", ".").strip()
            relevant_info["REMLatency"] = rem_latency.replace(",", ".").strip()
            relevant_info["Phase2Latency"] = phase_2_lantency.replace(",", ".").strip()

            print(f"N1 TTS: {N1_tts}\n")
            print(f"N2 TTS: {N2_tts}\n")
            print(f"N3 TTS: {N3_tts}\n")
            print(f"REM TTS: {rem_tts}\n")  
            print(f"REM latency: {rem_latency}\n")
            print(f"Phase 2 latency: {phase_2_lantency}\n")

        if "non rem, pre rx statistics" in text.lower():
            pre_treatment = text.split("Non REM, Pre Rx Statistics")[1]

            back_position_num_ac = str(safe_float(pre_treatment.split("Apneas")[1].split(" ")[4]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[4]))
            back_position_num_am = str(safe_float(pre_treatment.split("Apneas")[1].split(" ")[5]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[5]))
            back_position_num_ao = str(safe_float(pre_treatment.split("Apneas")[1].split(" ")[6]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[6]))

            back_position_num_hc = str(safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[4]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[4]))
            back_position_num_hm = str(safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[5]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[5]))
            back_position_num_ho = str(safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[6]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[6]))

            non_back_position_num_ac = str(safe_float(pre_treatment.split("Apneas")[1].split(" ")[1]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[1]))
            non_back_position_num_am = str(safe_float(pre_treatment.split("Apneas")[1].split(" ")[2]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[2]))
            non_back_position_num_ao = str(safe_float(pre_treatment.split("Apneas")[1].split(" ")[3]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[3]))

            non_back_position_num_hc = str(safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[1]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[1]))
            non_back_position_num_hm = str(safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[2]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[2]))
            non_back_position_num_ho = str(safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[3]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[3]))

            central_apneas_num = str(
                safe_float(pre_treatment.split("Apneas")[1].split(" ")[1]) + safe_float(pre_treatment.split("Apneas")[1].split(" ")[4])
                + safe_float(pre_treatment.split("Apneas")[2].split(" ")[1]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[4])
                )   
            
            central_hypopneas_num = str(
                safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[1]) + safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[4])
                + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[1]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[4])
                )
            
            mixed_apneas_num = str(
                safe_float(pre_treatment.split("Apneas")[1].split(" ")[2]) + safe_float(pre_treatment.split("Apneas")[1].split(" ")[5])
                + safe_float(pre_treatment.split("Apneas")[2].split(" ")[2]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[5])
                )
            
            mixed_hypopneas_num = str(
                safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[2]) + safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[5])
                + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[2]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[5])
                )
            
            obstructive_apneas_num = str(
                safe_float(pre_treatment.split("Apneas")[1].split(" ")[3]) + safe_float(pre_treatment.split("Apneas")[1].split(" ")[6])
                + safe_float(pre_treatment.split("Apneas")[2].split(" ")[3]) + safe_float(pre_treatment.split("Apneas")[2].split(" ")[6])
                )
            
            obstructive_hypopneas_num = str(
                safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[3]) + safe_float(pre_treatment.split("Hypopneas")[1].split(" ")[6])
                + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[3]) + safe_float(pre_treatment.split("Hypopneas")[2].split(" ")[6])
                )
            
            relevant_info["BackPositionNumAC"] = back_position_num_ac
            relevant_info["BackPositionNumAM"] = back_position_num_am
            relevant_info["BackPositionNumAO"] = back_position_num_ao
            relevant_info["BackPositionNumHC"] = back_position_num_hc
            relevant_info["BackPositionNumHM"] = back_position_num_hm
            relevant_info["BackPositionNumHO"] = back_position_num_ho
            relevant_info["NonBackPositionNumAC"] = non_back_position_num_ac
            relevant_info["NonBackPositionNumAM"] = non_back_position_num_am
            relevant_info["NonBackPositionNumAO"] = non_back_position_num_ao
            relevant_info["NonBackPositionNumHC"] = non_back_position_num_hc
            relevant_info["NonBackPositionNumHM"] = non_back_position_num_hm
            relevant_info["NonBackPositionNumHO"] = non_back_position_num_ho
            relevant_info["CentralApneasNum"] = central_apneas_num
            relevant_info["CentralHypopneasNum"] = central_hypopneas_num
            relevant_info["MixedApneasNum"] = mixed_apneas_num
            relevant_info["MixedHypopneasNum"] = mixed_hypopneas_num
            relevant_info["ObstructiveApneasNum"] = obstructive_apneas_num
            relevant_info["ObstructiveHypopneasNum"] = obstructive_hypopneas_num


            print(f"Back position num AC: {back_position_num_ac}\n")
            print(f"Back position num AM: {back_position_num_am}\n")
            print(f"Back position num AO: {back_position_num_ao}\n")
            print(f"Back position num HC: {back_position_num_hc}\n")
            print(f"Back position num HM: {back_position_num_hm}\n")
            print(f"Back position num HO: {back_position_num_ho}\n")
            print(f"Non back position num AC: {non_back_position_num_ac}\n")
            print(f"Non back position num AM: {non_back_position_num_am}\n")
            print(f"Non back position num AO: {non_back_position_num_ao}\n")
            print(f"Non back position num HC: {non_back_position_num_hc}\n")
            print(f"Non back position num HM: {non_back_position_num_hm}\n")
            print(f"Non back position num HO: {non_back_position_num_ho}\n")
            print(f"Central apneas num: {central_apneas_num}\n")
            print(f"Central hypopneas num: {central_hypopneas_num}\n")
            print(f"Mixed apneas num: {mixed_apneas_num}\n")
            print(f"Mixed hypopneas num: {mixed_hypopneas_num}\n")
            print(f"Obstructive apneas num: {obstructive_apneas_num}\n")
            print(f"Obstructive hypopneas num: {obstructive_hypopneas_num}\n")

        if "sao2 intervals" in text.lower():
            pst = text.split("Percent Sleep Time")[1]

            print(pst.split(" ")[2]+ "," + pst.split(" ")[3]+ "," + pst.split(" ")[4]+ "," + pst.split(" ")[5]+ "," + pst.split(" ")[6]+ "," + pst.split(" ")[7]+ "," + pst.split(" ")[8].split("\n")[0])

            dessaturation_under_90 = str(
                safe_float(pst.split(" ")[2]) + safe_float(pst.split(" ")[3]) + safe_float(pst.split(" ")[4]) + safe_float(pst.split(" ")[5])
                + safe_float(pst.split(" ")[6]) + safe_float(pst.split(" ")[7]) + safe_float(pst.split(" ")[8].split("\n")[0])
                ) 
            
            relevant_info["Desaturation<90%"] = dessaturation_under_90.replace(",", ".").strip()

            print(f"Desaturation under 90%: {dessaturation_under_90}\n")

        if "ekg statistics" in text.lower():
            heart_rate_average = text.split("Steady Sleep Avg ")[1].split(" ")[0]

            relevant_info["HeartRate_average"] = heart_rate_average.replace(",", ".").strip()

            print(f"Heart rate average: {heart_rate_average}\n")

        if "polissonografia revista" in text.lower():
            
            #grab all aasmcriteria until the last mention of "Associated Events"    
            AASM_criteria_text = "Polissonografia revista" + text.split("Polissonografia revista")[1]
            AASM_criteria_aux = AASM_criteria_text.split("Associated Events")
            AASM_criteria = ""

            for line in range(len(AASM_criteria_aux)-1):
                AASM_criteria += AASM_criteria_aux[line] + "Associated Events"

            relevant_info["AASMCriteria"] = AASM_criteria + '"'

            print(f"AASM criteria: {relevant_info['AASMCriteria']}\n")

        if "oximetry statistics" in text.lower():

            apneas_count = text.split("Apneas, Total ")[1].split(" ")[0]
            apneas_index = text.split("Apneas, Total ")[1].split(" ")[1]
            apneas_arousal = text.split("Apneas, Total ")[1].split(" ")[2]
            apneas_arousal_index = text.split("Apneas, Total ")[1].split(" ")[3]

            hypopneas_count = text.split("Hypopneas, Total ")[1].split(" ")[0]
            hypopneas_index = text.split("Hypopneas, Total ")[1].split(" ")[1]

            events_apnea_plus_hypopnea_count = text.split("Events (Apnea + Hypopnea) ")[1].split(" ")[0]
            events_apnea_plus_hypopnea_index = text.split("Events (Apnea + Hypopnea) ")[1].split(" ")[1]

            sao2_mean_wake = text.split("SaO2, Mean Wake ")[1].split(" ")[0]
            sao2_min = text.split("SaO2 Minimum ")[1].split(" ")[0]

            relevant_info["ApneasTotal"] = apneas_count.replace(",", ".").strip()
            relevant_info["ApneasTotalIndex"] = apneas_index.replace(",", ".").strip()
            relevant_info["ApneasArousals"] = apneas_arousal.replace(",", ".").strip()
            relevant_info["ApneasArousalsIndex"] = apneas_arousal_index.replace(",", ".").strip()
            relevant_info["HypopneasTotal"] = hypopneas_count.replace(",", ".").strip()
            relevant_info["HypopneasTotalIndex"] = hypopneas_index.replace(",", ".").strip()
            relevant_info["AHI"] = events_apnea_plus_hypopnea_count.replace(",", ".").strip()
            relevant_info["AHI.TTS"] = events_apnea_plus_hypopnea_index.replace(",", ".").strip()
            relevant_info["SaO2mean"] = sao2_mean_wake.replace(",", ".").strip()
            relevant_info["SaO2min"] = sao2_min.replace(",", ".").strip()

            print(f"Apneas count: {apneas_count}\n")
            print(f"Apneas index: {apneas_index}\n")
            print(f"Hypopneas count: {hypopneas_count}\n")
            print(f"Hypopneas index: {hypopneas_index}\n")
            print(f"Events apnea plus hypopnea count: {events_apnea_plus_hypopnea_count}\n")
            print(f"Events apnea plus hypopnea index: {events_apnea_plus_hypopnea_index}\n")
            print(f"SaO2 mean wake: {sao2_mean_wake}\n")
            print(f"SaO2 min: {sao2_min}\n")

        if "jerk counts" in text.lower(): #lol
            
            legs_movement_index = text.split("Isolated")[1].split(" ")[8]
            legs_movement_num  = text.split("Isolated")[1].split(" ")[10]
            
            plm_index = text.split("Jerks")[1].split(" ")[2]
            plm_num = text.split("Jerks")[1].split(" ")[1]

            relevant_info["LegsMovementIndex"] = legs_movement_index.replace(",", ".").strip()
            relevant_info["LegsMovementNum"] = legs_movement_num.replace(",", ".").strip()
            relevant_info["PLMIndex"] = plm_index.replace(",", ".").strip()
            relevant_info["PLMNum"] = plm_num.replace(",", ".").strip()

            print(f"Legs movement index: {legs_movement_index}\n")
            print(f"Legs movement num: {legs_movement_num}\n")
            print(f"PLM index: {plm_index}\n")
            print(f"PLM num: {plm_num}\n")

        if "body position statistics" in text.lower():
            
            back_position_duration = text.split("Total Sleep Time")[1].split(" ")[1]
            back_position_num_A = text.split("Number of Apneas")[1].split(" ")[1]
            back_position_num_H  = text.split("Number of Hypopneas")[1].split(" ")[1]

            non_back_position_duration = str(
                safe_float(text.split("Total Sleep Time")[1].split(" ")[2]) + safe_float(text.split("Total Sleep Time")[1].split(" ")[3])
                + safe_float(text.split("Total Sleep Time")[1].split(" ")[4]) + safe_float(text.split("Total Sleep Time")[1].split(" ")[5])
                )
            
            non_back_position_num_A = str(
                safe_float(text.split("Number of Apneas")[1].split(" ")[2]) + safe_float(text.split("Number of Apneas")[1].split(" ")[3])
                + safe_float(text.split("Number of Apneas")[1].split(" ")[4]) + safe_float(text.split("Number of Apneas")[1].split(" ")[5])
                )
            
            non_back_position_num_H = str(
                safe_float(text.split("Number of Hypopneas")[1].split(" ")[2]) + safe_float(text.split("Number of Hypopneas")[1].split(" ")[3])
                + safe_float(text.split("Number of Hypopneas")[1].split(" ")[4]) + safe_float(text.split("Number of Hypopneas")[1].split(" ")[5])
                )
            
            relevant_info["BackPositionDuration"] = back_position_duration.replace(",", ".").strip()
            relevant_info["BackPositionNumA"] = back_position_num_A.replace(",", ".").strip()
            relevant_info["BackPositionNumH"] = back_position_num_H.replace(",", ".").strip()
            relevant_info["NonBackPositionDuration"] = non_back_position_duration.replace(",", ".").strip()
            relevant_info["NonBackPositionNumA"] = non_back_position_num_A.replace(",", ".").strip()
            relevant_info["NonBackPositionNumH"] = non_back_position_num_H.replace(",", ".").strip()

            print(f"Back position duration: {back_position_duration}\n")
            print(f"Back position num A: {back_position_num_A}\n")
            print(f"Back position num H: {back_position_num_H}\n")
            print(f"Non back position duration: {non_back_position_duration}\n")
            print(f"Non back position num A: {non_back_position_num_A}\n")
            print(f"Non back position num H: {non_back_position_num_H}\n")
            

        if "physician interpretation" in text.lower():
            
            comments = text.split("Physician Interpretation\n")[1].split("Page")[0]

            recording_type = text.split("do tipo ")[1].split(".")[0] if "do tipo " in text else "---"

            relevant_info["Comments"] = comments
            relevant_info["Type"] = recording_type

            print(f"Comments: {comments}\n")
            print(f"Type: {recording_type}\n")


    return relevant_info



