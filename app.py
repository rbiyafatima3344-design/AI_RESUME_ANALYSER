import os
from flask import Flask, render_template, request
from groq import Groq
import PyPDF2
import json

app = Flask(__name__)

# 🔑 Apni Groq API Key yahan paste karein
GROQ_API_KEY =os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# PDF file se text nikalne ka function
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    jd_data = request.form.get('jd')
    resume_file = request.files.get('resume')
    
    if not resume_file or not jd_data:
        return "Error: Resume aur Job Description dono zaroori hain!"
    
    try:
        # 1. PDF se text nikalna
        resume_text = extract_text_from_pdf(resume_file)
        
        # 2. Prompt banana
        prompt = f"""
        You are an ATS Resume Analyzer. Analyze the resume against the job description.
        Return only valid JSON with fields:
        "summary": "Brief summary of candidate profile",
        "match_score": "Percentage score (e.g., 85%) based on match",
        "matching_skills": ["List of skills present in both resume and JD"],
        "missing_skills": ["List of important skills present in JD but missing in resume"]
        
        Job Description: {jd_data}
        Resume Text: {resume_text}
        """
        
        # 3. Groq API ko request bhejna (Llama3 model use kar rahe hain)
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}  # Groq khud hi pakka JSON bana kar dega!
        )
        
        # 4. JSON parse karna
        report = json.loads(response.choices[0].message.content)
        
        # 5. Ek khoobsurat HTML response screen par dikhana
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 30px auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: white; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h2 style="color: #007BFF; text-align: center;">📊 Analysis Report</h2>
            <hr>
            <h3>🎯 Match Score: <span style="color: #28a745;">{report.get('match_score', 'N/A')}</span></h3>
            <p><b>Summary:</b> {report.get('summary', 'N/A')}</p>
            
            <h4 style="color: #28a745;">✅ Matching Skills:</h4>
            <ul>
                {"".join(f"<li>{skill}</li>" for skill in report.get('matching_skills', []))}
            </ul>
            
            <h4 style="color: #dc3545;">❌ Missing Skills:</h4>
            <ul>
                {"".join(f"<li>{skill}</li>" for skill in report.get('missing_skills', []))}
            </ul>
            
            <br>
            <a href="/" style="display: block; text-align: center; background: #007BFF; color: white; padding: 10px; text-decoration: none; border-radius: 5px;">Analyze Another Resume 🔄</a>
        </div>
        """
    except Exception as e:
        return f"<h3>Kuch masla hua hai:</h3> <p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)