import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from fpdf import FPDF

# -----------------------
# Gemini Config
# -----------------------

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-flash-lite-latest")

# -----------------------
# UI
# -----------------------

st.title("🚀 AI Career Agent")
st.write("Upload your CV and discover how to reach your dream job.")

uploaded_file = st.file_uploader("Upload CV (PDF)", type="pdf")
dream_job = st.text_input("Enter your dream job role")
analyze = st.button("Analyze Career Path")

# -----------------------
# Skill database
# -----------------------

skills_db = [
    "Python","SQL","R","Tableau","Power BI","Machine Learning",
    "Deep Learning","AWS","Azure","Docker","Kubernetes",
    "Excel","Pandas","NumPy","TensorFlow","PyTorch"
]

job_keywords = {
    "data scientist":["machine learning","python","statistics","pandas","deep learning"],
    "data analyst":["sql","tableau","excel","dashboard","data visualization"],
    "software engineer":["algorithms","python","java","system design","api"]
}

# -----------------------
# Functions
# -----------------------

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_skills(text):
    found = []
    for skill in skills_db:
        if skill.lower() in text.lower():
            found.append(skill)
    return found

def ats_score(cv_text, job, skills):
    score = 0
    
    if len(cv_text) > 1500:
        score += 30
        
    if job.lower() in cv_text.lower():
        score += 30
        
    score += min(len(skills)*5,40)
    
    return score

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.cell(200,10,txt=line,ln=True)

    file_path = "career_report.pdf"
    pdf.output(file_path)
    return file_path

# -----------------------
# Main Logic
# -----------------------

if analyze:

    if uploaded_file and dream_job:

        cv_text = extract_text(uploaded_file)

        # -----------------------
        # Local analysis (FREE)
        # -----------------------

        skills = extract_skills(cv_text)

        score = ats_score(cv_text, dream_job, skills)

        keywords = job_keywords.get(dream_job.lower(),[])
        missing_keywords = [k for k in keywords if k not in cv_text.lower()]

        # -----------------------
        # Single Gemini call
        # -----------------------

        prompt = f"""
You are a career advisor.

Candidate CV:
{cv_text}

Dream Job:
{dream_job}

Provide:

1. Missing technical skills
2. Three project ideas they should build
3. A 3 month learning roadmap
4. Five interview questions for this role

Use clear headings.
Be concise.
"""

        response = model.generate_content(prompt)

        # -----------------------
        # Display Results
        # -----------------------

        st.header("🤖 AI Career Analysis")
        st.write(response.text)

        # -----------------------
        # ATS Score
        # -----------------------

        st.header("🎯 ATS Resume Score")

        st.progress(score/100)
        st.write(f"Score: {score}/100")

        # -----------------------
        # Detected Skills
        # -----------------------

        st.header("📊 Detected Skills")

        if skills:

            df = pd.DataFrame({"Skill": skills, "Value":[1]*len(skills)})
            st.bar_chart(df.set_index("Skill"))

        else:
            st.write("No common skills detected.")

        # -----------------------
        # Missing Keywords
        # -----------------------

        st.header("🔍 Missing Keywords")

        if missing_keywords:
            st.write(missing_keywords)
        else:
            st.write("Your CV already contains most relevant keywords.")

        # -----------------------
        # Word Cloud
        # -----------------------

        st.header("☁️ CV Word Cloud")

        wc = WordCloud(width=800,height=400,background_color="white").generate(cv_text)

        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")

        st.pyplot(fig)

        # -----------------------
        # Download Report
        # -----------------------

        st.header("📥 Download Career Report")

        file_path = create_pdf(response.text)

        with open(file_path, "rb") as f:
            st.download_button(
                "Download PDF Report",
                f,
                file_name="career_report.pdf"
            )

    else:
        st.warning("Please upload your CV and enter your dream job.")