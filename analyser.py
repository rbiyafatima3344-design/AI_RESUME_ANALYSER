import os
import json
from ollama import chat
from pypdf import PdfReader

while True:
    resume_file = input("enter resume file: ").strip('\'" ')
    name, ext = os.path.splitext(resume_file)
    if ext.lower() != ".pdf":
        print("invalid file.plz enter correct file format")
        continue
    elif not os.path.exists(resume_file):
        print("file not found")
        continue
    else:
        print("correct format file found")
        break

while True:
    job_description = input("enter job description: ").strip('\'" ')
    name, ext = os.path.splitext(job_description)
    if ext.lower() != ".txt":
        print("invalid job description must be in .txt")
        continue
    elif not os.path.exists(job_description):
        print("file not found")
        continue
    else:
        print("file found in correct format") 
        break

print("\n--- READING FILES NOW ---")

try:
    reader = PdfReader(resume_file)
    pages = reader.pages
    resume_text = ""
    for i in pages:
        page_text = i.extract_text()
        if page_text is None:
            print("extracted text is empty")
        else:
            resume_text = resume_text + page_text
    print("file read and text extracted successfully")
except:
    print("unable to read pdf file")        

try:
    with open(job_description, "r") as f:
        description = f.read()
    print("description read successfully")
except:
    print("invalid description") 

messages = []
messages.append(
    {
        'role': 'system',
        'content': f"You are an ATS Resume Analyzer. Analyze the resume against the job description. Return only valid JSON with fields: summary, match_score, matching_skills, missing_skills. Job Description:\n{description}\n\nResume:\n{resume_text}"
    }
)

response = chat(model="llama3:8b", messages=messages, format="json")
bot_response = response.message.content
report = json.loads(bot_response)

print("summary")
print(report["summary"])
print("match scores")
print(report["match_score"])

for i in report["matching_skills"]:
    print(i)

for i in report["missing_skills"]:  
    print(i)

messages.append({
    "role": "system",
    "content": "You are an AI Career Counselor and Resume Advisor. Use the provided resume and job description to answer the user's questions. Provide concise, practical, and actionable advice. Do not return JSON unless explicitly requested."
})

while True:
    query = input("\nWant to ask any question? (Type 'exit' to quit): ")
    if query.lower() == "exit":
        print("\nTHANKS FOR USING MY APP!")
        break
        
    messages.append({
        "role": "user",
        "content": query
    }) 
    
    response = chat(
        model="llama3:8b",
        messages=messages
    )
    chatbot_response = response.message.content
    print("\nASSISTANT:\n", chatbot_response)
    
    messages.append({
        "role": "assistant",
        "content": chatbot_response
    })