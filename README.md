# Clinical Data Review with added NLP Analysis

## Project Overview

This project simulates a **clinical trial data review and reporting workflow** using **synthetic clinical study data**. It demonstrates skills relevant to **clinical data analyst**, **clinical programming**, and **pharma analytics** roles.

The project includes:

- SQL-based clinical data review queries
- synthetic study data generation in Python
- NLP analysis of free-text operational and safety fields

---

## Skills Demonstrated

- **SQL**
- **Python**
- **Clinical data review**
- **Data cleaning / discrepancy detection**
- **Safety reporting**
- **Operational analytics**
- **NLP (TF-IDF + clustering)**
- **Jupyter notebooks**
- **Synthetic data generation**

---

## Dataset Contents

- `subjects.csv`
- `sites.csv`
- `visits.csv`
- `labs.csv`
- `adverse_events.csv`
- `conmeds.csv`
- `protocol_deviations.csv`
- `data_queries.csv`
- `incident_change_log.csv`

---

## NLP Extension

This project also includes an NLP workflow applied to **clinical operations and safety text fields**.

The NLP pipeline analyzes:

- adverse event descriptions
- protocol deviation narratives
- incident/change log descriptions

using:

- **TF-IDF vectorization**
- **KMeans clustering**

This helps identify recurring operational and safety themes.

---

## How to Run

### 1. Create and activate a virtual environment

#### Windows CMD
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### Windows PowerShell
```powershell
python -m venv venv
cmd /c venv\Scripts\activate.bat
```

#### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Generate synthetic data

```bash
python scripts/synthetic_clinical_study_generator.py
```

---

### 4. Run NLP analysis

```bash
python scripts/nlp_analysis.py
```

---

### 5. Explore notebook (optional)

```bash
jupyter notebook
```

Open:

```bash
notebooks/clinical_review_analysis.ipynb
```
---
### 6. Load CSV's to SQLite

```bash
python scripts/load_to_sqlite.py
```
---
### 7. Open SQLite in Virtual Environment and run SQl files individually
---
## Example SQL Analyses

The SQL folder includes queries for:

- enrollment funnel analysis
- missing forms
- out-of-range lab detection
- adverse event summaries
- protocol deviation review
- open data query tracking
- visit compliance
- incident/change request summaries

