# 🚀 Da7ee7-El-Dof3a
### AI-Powered Study Assistant using Large Language Models (LLMs)

> 🏆 Official submission for the **Tips Hindawi Challenge (June–July 2026)**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

</div>

---

# 👤 Author

| Field | Information |
|--------|-------------|
| **Name** | Aya Abdelwahab Abdelhafez |
| **GitHub** | https://github.com/AyaAbdelwahabAbdelhafez |
| **Project** | Da7ee7-El-Dof3a |
| **Challenge** | Tips Hindawi Challenge (June–July 2026) |
| **Training Program** | Large Language Models (LLMs) |
| **Organization** | Edrak for AI |

---

# 📖 Overview

Da7ee7-El-Dof3a is an AI-powered study assistant that transforms lecture materials into interactive learning resources.

The system enables students to upload lecture slides, notes, PDFs, and previous exams, then automatically generates:

- Smart Summaries
- Important Topics
- Revision Notes
- AI-powered Exam Solutions

The project combines Retrieval-Augmented Generation (RAG), vector databases, and Large Language Models to produce accurate answers grounded in the uploaded course material.

---

# ✨ Features

## 📚 Smart Summary

Generate concise summaries from lecture slides and study materials.

---

## 🎯 Important Topics

Automatically identify the most important concepts for revision.

---

## 📝 Revision Notes

Create exam-focused revision notes from uploaded content.

---

## 🤖 AI Exam Solver

Solve previous exams using Retrieval-Augmented Generation (RAG).

---

## 🔍 Semantic Search

Retrieve the most relevant lecture content using FAISS vector search.

---

## 📄 PDF Export

Download generated summaries, revision notes, and solved exams as professionally formatted PDF files.

---

## ⚡ FastAPI Backend

RESTful API built with FastAPI for seamless frontend integration.

---

# 🏗️ System Architecture

```text
Student
   │
   ▼
Upload PDFs / PPTX / DOCX
   │
   ▼
Text Extraction
   │
   ▼
Chunking
   │
   ▼
Embeddings
   │
   ▼
FAISS Vector Database
   │
   ▼
Retriever
   │
   ▼
Large Language Model
   │
   ▼
Summary
Important Topics
Revision Notes
Solved Exam
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- Uvicorn

## AI

- Hugging Face Transformers
- LangChain
- FAISS
- Sentence Transformers

## Data Processing

- pdfplumber
- python-pptx
- python-docx

## Deployment

- Kaggle GPU
- ngrok

---

# 📂 Project Structure

```text
Da7ee7-El-Dof3a/
│
├── ai_service/
│   ├── da7ee7-el-dof3a-ai-service.ipynb
│   └── requirements.txt
│
├── backend/
│   ├── app/
│   ├── logs/
│   ├── .env
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── index.html
│   ├── upload.html
│   ├── processing.html
│   ├── summary.html
│   ├── results.html
│   └── solved_exams.html
│
├── .vscode/
│   └── launch.json
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/AyaAbdelwahabAbdelhafez/Da7ee7-El-Dof3a.git

cd Da7ee7-El-Dof3a
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

---

# 🚀 Usage

1. Upload lecture materials.
2. Wait for indexing.
3. Generate:
   - Smart Summary
   - Important Topics
   - Revision Notes
4. Upload a previous exam.
5. Receive AI-generated answers.
6. Download PDF reports.

---

# 📊 Results

✔ Upload and process lecture files

✔ Build a FAISS vector database

✔ Generate AI-powered summaries

✔ Identify important topics automatically

✔ Produce revision notes

✔ Solve previous exams using RAG

✔ Export downloadable PDF reports

---

# 🔮 Future Improvements

- User authentication
- Multi-course support
- OCR for scanned PDFs
- Arabic language optimization
- Voice lecture transcription
- Cloud deployment
- Chat with lecture materials

---

# 🎓 About the Challenge

This project was developed as part of the **Tips Hindawi Challenge (June–July 2026)** under the **Large Language Models (LLMs)** training program organized by **Edrak for AI**.

The challenge focuses on applying Large Language Models to solve real-world educational problems through practical AI applications.

---

# 👨‍💻 Developer

**Aya Abdelwahab Abdelhafez**

GitHub:
https://github.com/AyaAbdelwahabAbdelhafez

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 📄 License

This project is intended for educational, research, and portfolio purposes.
