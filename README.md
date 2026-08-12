---
title: Drug Complaint Classifier
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.26.0
app_file: app.py
pinned: false
---

# 🚀 Drug Free TN AI System

An industry-grade, production-ready AI-powered pipeline and analytical dashboard built to classify, analyze, and map drug-related complaints in Tamil Nadu. The system processes multilingual (English, Tamil, and Tanglish) inputs, runs semantic validation/junk filtering, extracts critical entities (drugs, crimes, locations), stores structured data in a database, and visualizes hotspots and trends to help law enforcement take swift action.

---

## 🏗️ System Architecture & Flow

```
   ┌──────────────────────────────────────────────────────────┐
   │                    User Interface                        │
   │   (HTML Dashboard / Submit Page / Streamlit Dashboard)   │
   └─────────────┬──────────────────────────────▲─────────────┘
                 │ (1) Submit Complaint         │ (4) Fetch Aggregated
                 │     (Text & Address)         │     Data & Stats
                 ▼                              │
   ┌────────────────────────────────────────────┴─────────────┐
   │                    FastAPI Backend                       │
   │                  (app/main.py API)                       │
   └─────────────┬──────────────────────────────▲─────────────┘
                 │ (2) Run NLP Pipeline         │ (3) Save/Retrieve
                 ▼                              │     Structured Data
   ┌────────────────────────────────────────────┼─────────────┐
   │                     AI Engine              │   MySQL DB  │
   │  - Text Normalization & Tamil Cleaning     │  (complaints│
   │  - Junk & Relevance Classifier (BART)      │    table)   │
   │  - Drug & Crime Classifier (MiniLM)        │             │
   │  - Named Entity & Location Extraction      └──────▲──────┘
   └───────────────────────────────────────────────────┘
```

---

## ✨ Features

- **Multilingual Support**: Tailored to parse clean English, formal Tamil, and colloquial Tanglish (Tamil written in English script) using standard preprocessors and fuzzy matching.
- **Intelligent Relevance Filtering**: Screens incoming messages to isolate spam, casual texts, or irrelevant junk, maintaining database cleanliness.
- **Deep Semantic Classification**:
  - **Drug Detection**: Identifies drug categories (e.g., Ganja, Heroin, Painkillers) via embedding similarity.
  - **Crime Classification**: Classifies behavior type (e.g., Sale, Usage, Cultivation, Transport).
- **Location Extraction & Geocoding**: Dissects raw text and input addresses to isolate the targeted city and specific location detail, mapping them to geographic coordinates.
- **Interactive Dashboards**:
  - **Single Entry Portal**: Accessible UI for submitting individual complaints and viewing real-time AI classification metrics.
  - **Analytics Dashboard**: Rich web UI depicting KPIs (Total vs. High Risk, Junk ratio), city trends, crime distributions, historical heatmaps, and high-risk sale zones.
  - **Streamlit App**: Alternate data-scientific representation of complaint patterns.

---

## 🛠️ Tech Stack & Model Cards

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI** | High-performance ASGI framework for serving predictions and dashboard stats. |
| **Database** | **MySQL** | Reliable relational storage for keeping track of complaints, locations, and predictions. |
| **Analytics Dashboard** | **Streamlit / HTML5** | Dual presentation layers showcasing visual data analytics, charts, and maps. |
| **Junk Detection** | `facebook/bart-large-mnli` | Zero-shot classification model for intent and relevance verification. |
| **Semantic Extraction** | `paraphrase-multilingual-MiniLM-L12-v2` | Sentence-transformer used to generate robust embeddings for similarity matching. |
| **Entity Extractor (NER)** | `dslim/bert-base-NER` | Transformer model trained to identify standard entities (Persons, Organizations, Locations). |

---

## 📁 Project Structure

```text
Ai-tool-29426/
├── app/
│   ├── main.py                 # FastAPI application entry point & route registration
│   ├── config.py               # Central configuration settings
│   ├── database/
│   │   ├── db.py               # MySQL connection initializer
│   │   └── crud.py             # Database CRUD (insertion logic)
│   ├── models/
│   │   └── complaint_model.py  # Pydantic schemas for API validation
│   ├── routes/
│   │   ├── complaint.py        # Endpoints for single and bulk complaint analysis
│   │   └── dashboard.py        # Endpoints to serve HTML view and dashboard metrics
│   ├── services/
│   │   ├── ai_pipeline.py      # Core coordination of the AI pipeline
│   │   ├── Tamil_preprocessor.py # Cleans Tamil characters and maps colloquial words
│   │   ├── text_normalizer.py  # Standardizes string casing and formats
│   │   ├── junk_classifier.py  # Validates relevance using BART models
│   │   ├── drug_classifier.py  # Maps drug names using sentence embeddings
│   │   ├── crime_classifier.py # Maps crime categories using sentence embeddings
│   │   ├── location_extractor.py # Resolves cities and local addresses
│   │   └── ner_extractor.py    # Extracts named entities via BERT NER
│   └── utils/                  # Helper utilities and math functions
├── dashboard/
│   ├── dashboard.html          # Interactive analytics dashboard interface
│   ├── dashboard.js            # Custom interactive styling script
│   └── streamlit_app.py        # Streamlit-based data dashboard
├── notebooks/
│   └── model_training.ipynb    # Python notebook detailing model explorations
├── complaint-json.py           # Helper script to convert Excel reports into JSON payload
├── requirements.txt            # System dependencies
├── README.md                   # Project documentation
└── .env                        # Environment configuration variables
```

---

## 🚀 Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed along with a running MySQL server.

### 2. Configure Database
Login to your MySQL instance and execute the following database setup:
```sql
CREATE DATABASE drug_ai;
USE drug_ai;

CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_text TEXT,
    is_junk BOOLEAN,
    drug_type VARCHAR(100),
    crime_type VARCHAR(100),
    address TEXT,
    city VARCHAR(100),
    location_detail VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
*Note: If your MySQL database credentials differ from user `root` / password `root`, update them in [app/database/db.py](file:///d:/Drug%20free%20TN/Ai-tool-29426/app/database/db.py).*

### 3. Install Dependencies
Initialize a virtual environment and install the required dependencies:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🏃 Running the Application

### Running the API & Dashboard Server
To start the FastAPI server with reload functionality:
```bash
uvicorn app.main:app --reload --port 8080
```
- **Web App Dashboard**: Visit [http://localhost:8080/](http://localhost:8080/)
- **Complaint Submission Portal**: Visit [http://localhost:8080/api/dashboard/submit](http://localhost:8080/api/dashboard/submit)
- **API Documentation (Swagger)**: Visit [http://localhost:8080/docs](http://localhost:8080/docs)

### Running the Streamlit Dashboard (Alternative)
```bash
streamlit run dashboard/streamlit_app.py
```

### Batch Processing Excel Files
If you have complaints in an Excel sheet, convert them to JSON using:
```bash
python complaint-json.py
```
Then send the output list to the `/api/analyze-bulk` endpoint.

---

## 🔌 API Reference

### 1. Analyze Single Complaint
- **Endpoint**: `POST /api/analyze-complaint`
- **Request Body**:
  ```json
  {
    "complaint": "Ganja sales happening near Salem central bus stand in the evening hours.",
    "address": "Salem Bus Stand"
  }
  ```
- **Response**:
  ```json
  {
    "complaint_text": "ganja sales happening near salem central bus stand in the evening hours.",
    "is_junk": false,
    "junk_confidence": 0.05,
    "drug_type": "ganja",
    "drug_confidence": 0.92,
    "crime_type": "sale",
    "crime_confidence": 0.88,
    "address": "Salem Bus Stand",
    "city": "salem",
    "location_detail": "salem central bus stand",
    "entities": {
      "persons": [],
      "locations": ["Salem central bus stand"],
      "organizations": []
    }
  }
  ```

### 2. Bulk Process Complaints
- **Endpoint**: `POST /api/analyze-bulk`
- **Request Body**:
  ```json
  {
    "complaints": [
      {
        "complaint": "Someone is selling drugs near Madurai college.",
        "address": "Madurai"
      },
      {
        "complaint": "Hi how are you",
        "address": "Unknown"
      }
    ]
  }
  ```
- **Response**: A list containing prediction objects for each input.
