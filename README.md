# Sleep Report Extraction

Automatically extract structured data from sleep study PDF reports and visualize results using a Dash web application.

This repository contains tools to parse various types of sleep study reports (e.g., Alice Sleepware reports, short reports, REM Logic polysomnography and polygraphy reports), export structured data to JSON and CSV, perform simple exploratory analysis, and run a Dash UI for visualization and further analysis.

---

## ✅ Features
- Parse and extract structured fields from different sleep report PDF formats:
	- Alice Sleepware reports
	- Short reports
	- REMLogic Polysomnography and Polygraphy reports
- Export per-report JSON files and a combined CSV summary (`data/jsons`, `data/csvs/report_summary.csv`).
- Dash-based web UI to upload PDFs, visualize summary stats, and view each report details.
- Basic Named Entity Recognition on medical comments using a pre-trained Portuguese NER model (Hugging Face pipeline) and save entities to `src/entities.json`.

---

## 🧭 Quickstart

Prerequisites: Python 3.10+ recommended, Windows example below using PowerShell. The repository includes a `requirements.txt` file listing the dependencies.

1) Create a virtual environment and install requirements

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2) Provide input PDFs
- Place the sleep study PDF files you want to parse into `data/pdfs/input`. The `data/` directory contains: `pdfs/`, `jsons/`, `csvs/`.

3) CLI extraction (process all PDFs in `data/pdfs/input` and write outputs)

```powershell
python src\data_extraction.py
```

This will produce individual JSON files for each report in `data/jsons` and a combined CSV `data/csvs/report_summary.csv`.

4) Run the Dash web app (interactive)

```powershell
python src\app.py
```

Open http://127.0.0.1:8050/ or the localhost URL printed out to upload PDFs via the web UI, process them and visualize results.

---

## 🔍 Repository structure

Main folders:
- `data/` – Input PDFs and output JSONs/CSVs. Contains `pdfs/input`, `jsons`, `csvs`.
- `src/` – Source code and Dash app.
	- `alice_report_extraction.py` – Parser for Alice Sleepware reports.
	- `short_report_extraction.py` – Parser for Acquisition/Short Reports.
	- `readRemFile.py` / `readRemPolyFile.py` – Parsers for REMLogic Polysomnography and Polygraphy.
	- `data_extraction.py` – Main CLI file that detects the report type and exports JSON/CSV.
	- `app.py` – Dash web application entry point (uploads + visualization).
	- `callbacks/`, `layouts/`, `assets/` – Dash UI components and callbacks.
	- `utils.py` – Helper functions used by the different parsers.

---

## 📝 How it works / parsing strategy
- For each PDF, `data_extraction.extract_info_from_pdfs()` opens the PDF using `pdfplumber` and checks the first page's contents to guess the report format (e.g. first word is "Alice", or presence of "short report", "polysomnography", "polygraphy").
- Then the appropriate handler runs and extracts fields using a mix of table extraction and regular expressions.
- Exported data is normalized to JSON and concatenated into a summary CSV using pandas.
- The Dash app allows uploading PDFs and performs the same extraction on uploaded files. Uploaded PDFs are temporarily saved to `data/pdfs/input`, processed, and removed after processing.

---

## 🛠️ Adding support for new report types
1. Add a new parser in `src/` (e.g., `my_format_parser.py`) that provides a function `handle_my_format(pdf)` which returns a dict with keys and extracted values.
2. Update `src/data_extraction.py` to call the new parser from `extract_info_from_pdfs()` when the format detection matches your file type.
3. Optionally add frontend adjustments (layout or categories) in `src/callbacks/utils.py` if you need to display new fields.

---

## ⚠️ Notes & troubleshooting
- These parsers rely on heuristics and specific PDF layouts; they will not be 100% accurate for all sources or new versions of report templates.
- Text extraction may vary depending on the PDF renderer—`pdfplumber` is used (pdfminer underneath). If the text/tables are not extracted correctly, the parser may fail or return incomplete output.
- The Hugging Face NER model used for comment analysis is `portugueseNLP/medialbertina_pt-pt_900m_NER` — this is downloaded dynamically the first time you run the app, so allow some time during the first run and make sure you have internet access.

---

## 🧪 Tests
There are no dedicated unit tests in this repository yet. If you want to add tests, the parsers can be tested against sample PDFs placed into `data/pdfs/input` using a small test harness that calls `data_extraction.py` or the handler functions directly.

---

## 🤝 Contributing
If you'd like to help, please:
- Fork the repository
- Add your feature, bug fix, or tests in a separate branch
- Open a pull request with a description of your changes and example PDFs for the new parser (if applicable)

Consider contributing a sample PDF for each parser you're enhancing (no patient-identifying info).

---

## 🔒 Data & privacy
- Uploaded PDFs and generated intermediate files are processed locally and removed after processing (see `file_upload_callbacks.py` where files are deleted after extraction).
- This repository does not include de-identification steps — if you plan to share or upload reports with PHI, please anonymize the data first.

---

## 📄 License
No license file is included at the moment. If this project should be open source, consider adding a `LICENSE` (for example, `MIT`) to the root of this repository.

---

## 👥 Authors & Acknowledgments
This project was created to help automate the extraction of structured information from clinical sleep study reports. Thanks to the maintainers of `pdfplumber`, `pandas`, `Dash`, and the Hugging Face ecosystem used in the project.

