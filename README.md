# 💼 HireScout AI - Smart ATS System

An Enterprise-grade Applicant Tracking System (ATS) powered by Google Gemini AI and Streamlit. This tool automates the resume screening process by analyzing candidate PDFs against job descriptions.

## 🚀 Features
* **Smart Parsing:** Extracts text from PDF resumes seamlessly.
* **AI Evaluation:** Uses Google Gemini 1.5 Flash to evaluate candidates.
* **Analytics Dashboard:** Visual representation of match scores.
* **Exportable Reports:** Download a comprehensive CSV audit report.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI Model:** Google Gemini API
* **Language:** Python 3.x

## 💻 How to Run Locally

1. Install the requirements:
   pip install -r requirements.txt

2. Add your Google API Key in a `.env` file:
   GOOGLE_API_KEY="your_api_key_here"

3. Run the application:
   streamlit run app.py
