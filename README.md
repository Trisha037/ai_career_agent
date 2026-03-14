# 🚀 AI Career Agent

AI Career Agent is a Streamlit application that analyzes a user's CV and provides a personalized roadmap to reach their dream job.

The application uses Google's Gemini model to generate career insights while performing most analysis locally to keep API usage low.

---

## Features

- 📄 Upload and analyze your CV (PDF)
- 🤖 AI-generated career advice
- 🎯 ATS Resume Score
- 📊 Skill detection and visualization
- 🔍 Missing job keywords analysis
- ☁️ CV word cloud
- 📥 Downloadable career report

---

## How It Works

1. The user uploads their CV.
2. The application extracts the text from the PDF.
3. A single Gemini API request generates career guidance.
4. Additional analysis (skills, ATS score, keyword gaps) is computed locally.

This architecture keeps the application fast and reduces API costs.

---

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- PyPDF
- Pandas
- WordCloud
- Matplotlib

---
## App Preview


## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-career-agent.git
cd ai-career-agent



