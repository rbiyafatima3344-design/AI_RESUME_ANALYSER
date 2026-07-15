# 📄 AI Resume Analyzer (ATS Evaluator)

An AI-powered **Applicant Tracking System (ATS)** tool that helps job seekers analyze their resumes against specific job descriptions. Built using **Python (Flask)**, **Groq API (Llama 3)**, and **PyPDF2**.

---

## 🚀 Key Features

*   **PDF Parsing:** Extracts and processes raw text from PDF resumes using `PyPDF2`.
*   **AI-Powered Analysis:** Leverages the **Llama-3 model (via Groq API)** to evaluate candidate profiles.
*   **ATS Score Generation:** Calculates an estimated match percentage based on skills and experience.
*   **Skill Gap Analysis:** Generates structured lists of **Matching Skills** and **Missing Skills** to help candidates optimize their resumes.
*   **Clean Web Interface:** Built with a clean, responsive HTML/CSS UI for easy resume uploading and job description pasting.

---

## 🛠️ Tech Stack & Tools

*   **Backend:** Python 3.x, Flask (Web Framework)
*   **AI Engine:** Groq Cloud API (Llama-3-8b-8192)
*   **Libraries:** PyPDF2 (PDF text extraction), Requests, JSON
*   **Frontend:** Responsive HTML5 & CSS3
*   **Deployment:** Ready for Render / Heroku

---

## 📁 Project Structure

Here is the clean directory structure of this project:

```text
AI_Resume_Analyzer/
│
├── templates/
│   └── index.html          # Clean & interactive frontend interface
│
├── app.py                  # Main Flask backend application (Handles PDF parsing & Groq API)
├── requirements.txt        # Python dependencies required for deployment
└── README.md               # Project documentation (You are here!)
