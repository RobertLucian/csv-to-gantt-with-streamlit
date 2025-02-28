# Gantt Chart Generator

This is a **Streamlit app** that allows users to **upload or paste CSV files** to generate **interactive Gantt charts**. It ensures that the input format is correct and highlights errors in the data.

## 🚀 Features
- Upload multiple CSV files or paste data directly.
- Generates **separate Gantt charts** for each dataset.
- Ensures input validation (date format, missing columns, logical errors).
- Displays **monthly labels** for better visualization.

## 📌 CSV Input Requirements
- The CSV must contain these **3 columns**:
  - `Activitati` (Task Name)
  - `Data estimativa inceput` (Start Date) in **MM/DD/YYYY** format
  - `Data estimativa finalizare` (End Date) in **MM/DD/YYYY** format
- The start date **must not be after** the end date.
- Extra columns are **ignored automatically**.

## 🔧 How to Run Locally
```sh
pip install -r requirements.txt
streamlit run app.py
```

## 🚀 Deploy on Streamlit Cloud
Click the button below to **deploy instantly** on **Streamlit Cloud**:

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/RobertLucian/csv-to-gantt-with-streamlit/main/app.py)
