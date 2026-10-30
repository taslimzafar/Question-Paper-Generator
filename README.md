# 📝 Question Paper Generator (PaperForge)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-red.svg)](https://streamlit.io/)

An interactive, browser-based assessment generation tool built with Streamlit. It allows educators and trainers to transform course notes, syllabus documents, and learning materials into structured, customizable, and editable question papers.

---

## ✨ Features

- **Dual Generation Modes:**
  - **Offline Mode:** Privacy-first, deterministic extractive question generation running entirely on your local machine with zero external network calls or API keys required.
  - **LLM Mode:** Connect to any OpenAI-compatible API endpoint (OpenAI, LocalAI, vLLM, Ollama, Groq, etc.) with custom model and base URL settings.
- **Multi-Format Document Ingestion:**
  - Supports direct text pasting as well as file uploads (`.txt`, `.pdf`, `.docx`).
- **Flexible Assessment Configuration:**
  - Customizable subject, class/grade, assessment type (Unit test, Midterm, Quiz, Practice test, Final exam).
  - Configurable question count, total marks distribution, and difficulty levels (Easy, Moderate, Challenging).
  - Multiple question formats: Short Answer, Long Answer, and Multiple Choice (MCQ).
- **Interactive Review & Editing:**
  - Edit question prompts, mark weightings, and model answer keys directly inside expandable UI cards before exporting.
  - Teacher view includes rationale, suggested answers, and source sentence grounding.
- **One-Click Export:**
  - Download Student Question Paper (`.txt`).
  - Download Teacher Answer Key & Marking Guide (`.txt`).
  - Export complete structured assessment data (`.json`).
- **Exploratory Data Analysis (EDA) Suite:**
  - Standalone data processing and SVG chart generation for retrieval metadata benchmarking.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher installed and added to your system `PATH`.
- Git installed.

### Option 1: One-Click Launcher

#### On Windows:
Double-click `run_windows.bat` or run in PowerShell:
```powershell
.\run_windows.bat
```

#### On Linux / macOS:
Make the script executable and run:
```bash
chmod +x run_unix.sh
./run_unix.sh
```

---

### Option 2: Manual Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/taslimzafar/Question-Paper-Generator.git
   cd Question-Paper-Generator
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```text
Question-Paper-Generator/
├── app.py                       # Main Streamlit web application & generation logic
├── requirements.txt             # Python project dependencies
├── run_windows.bat              # Automated Windows setup & launcher script
├── run_unix.sh                  # Automated Linux/macOS setup & launcher script
├── .gitignore                   # Ignored files (virtual environments, cache, OS files)
├── README.md                    # Project documentation
│
├── analysis/                    # Data exploration & chart generation
│   ├── eda.py                   # Reproducible data cleaning & visualization script
│   ├── eda_summary.json         # Summary statistics of the reference metadata
│   ├── query_type_counts.svg    # Query distribution chart
│   ├── retrieval_score_distribution.svg # Score distribution chart
│   └── word_count_vs_quality.svg        # Quality vs word count scatter chart
│
├── data/                        # Reference metadata & dictionary
│   ├── dataset.csv              # Cleaned reference dataset (500 rows)
│   ├── dataset_original.csv     # Raw reference dataset
│   ├── data_dictionary.csv      # Data dictionary with field specifications
│   └── data_dictionary_original.csv
│
└── docs/                        # Formal documentation & reports
    ├── architecture.png         # System architecture diagram (raster)
    ├── architecture.svg         # System architecture diagram (vector)
    ├── Ethical_Compliance_Checklist.md # Ethics, fairness, and privacy checklist
    ├── Project_Report.md        # Comprehensive academic/technical report
    ├── Project_Report.docx      # Word document format of project report
    ├── Project_Synopsis_Completed.md   # Project synopsis
    └── Project_Synopsis_Completed.docx # Word document format of synopsis
```

---

## 📊 Exploratory Data Analysis (EDA)

To regenerate the descriptive analysis and charts:
```bash
python analysis/eda.py
```
This processes `data/dataset_original.csv`, cleans the records, validates value bounds, and produces vector SVG charts in the `analysis/` directory.

---

## ⚖️ Responsible Use & Ethics

- **Human-in-the-Loop:** All generated questions and answer keys must be reviewed and vetted by a subject-matter educator prior to examination use.
- **Data Privacy:**
  - Offline mode does not transmit your text or documents over the internet.
  - LLM mode transmits text to your specified API provider. Avoid uploading confidential, proprietary, or personally identifiable information without proper authorization.
  - API keys entered in the UI are held only in memory during the active session and are never logged or stored.


