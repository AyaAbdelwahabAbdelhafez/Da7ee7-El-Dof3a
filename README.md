 # 🚀 Da7ee7-El-Dof3a
### AI-Powered Study Assistant using Large Language Models (LLMs)

> 🏆 Official submission for the **Tips Hindawi Challenge (June–July 2026)**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-black)
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

Students upload lecture slides, notes, recordings, and previous exams. The AI service (a Kaggle GPU notebook exposed through FastAPI + ngrok) indexes everything with a multilingual (Arabic/English) FAISS retriever, then generates:

- Smart Summaries (full-course Map-Reduce, not just top-k chunks)
- Ranked Important Topics
- Revision Notes (Must-Know / Formulas / Common Mistakes)
- AI-Solved Exams, question by question

---

# ✨ Features

## 📚 Smart Summary

Every chunk of every uploaded file is summarized (Map step), then merged into one de-duplicated, logically-ordered Smart Summary (Reduce step) — so the whole course is covered, not just whatever a similarity search happens to retrieve.

---

## 🎯 Important Topics

Returns a ranked JSON list (5–12 items) of the most heavily emphasized exam topics, derived from the same partial summaries used for the Smart Summary.

---

## 📝 Revision Notes

A single revision sheet, under 400 words, with exactly three sections: Must-Know, Formulas/Definitions, and Common Mistakes.

---

## 🤖 AI Exam Solver

Solves previous exams question-by-question using Retrieval-Augmented Generation. Question splitting is multi-stage: numbered markers (Latin **and Arabic**, e.g. `Q1`, `1.`, `١.`, `السؤال 1`, `س1:`) → blank-line paragraphs → sentence-level `?`/`؟` splitting → an LLM-based semantic fallback for irregular layouts. Each answer is capped at 2–5 lines, grounded strictly in the uploaded material, and a single question failing never aborts the rest of the exam.

---

## 🔍 Semantic Search

Multilingual FAISS retrieval (`paraphrase-multilingual-mpnet-base-v2`) over chunked lecture content, so Arabic and English material are both searchable.

---

## 🎙️ Audio & Video Transcription

Lecture recordings (`.mp3`, `.wav`, `.m4a`) and videos (`.mp4`, `.mov`, `.mkv`) are transcribed with Whisper (`medium`) before indexing — video audio is extracted automatically first.

---

## 📄 PDF Export

Summaries, revision notes, and solved exams are exportable as formatted PDFs via ReportLab.

---

## ⚡ FastAPI Backend

The Kaggle notebook itself exposes a REST API (via an ngrok tunnel) that the local backend calls directly for every AI operation.

---

# 🏗️ System Architecture

```text
Student
   │
   ▼
Upload PDF / PPTX / DOCX / audio / video   (POST /ingest)
   │
   ▼
Text Extraction  +  Whisper transcription (audio/video)
   │
   ▼
Chunking (RecursiveCharacterTextSplitter)
   │
   ▼
Multilingual Embeddings (Arabic + English)
   │
   ▼
FAISS Vector Index (per session)
   │
   ▼
Retriever  +  Qwen2.5-7B-Instruct (4-bit NF4, single fixed model)
   │
   ▼
Smart Summary · Important Topics · Revision Notes · Solved Exam
   │
   ▼
PDF Export (ReportLab)  →  GET /download
```

---

# 🛠️ Tech Stack

## AI Service (Kaggle notebook)

- **Model:** `Qwen/Qwen2.5-7B-Instruct` — one fixed, open-weight, Apache-2.0 model (no per-session benchmarking, no gated-license risk), quantized to 4-bit NF4 (falls back to 8-bit if unsupported)
- Hugging Face Transformers + `pipeline` (greedy decoding, repetition penalty, `no_repeat_ngram_size` to prevent looping/hallucinated output)
- LangChain (RetrievalQA-style chunking + prompting) + LangChain-HuggingFace
- FAISS (`faiss-cpu`) for per-session vector search
- Sentence-Transformers multilingual embeddings (`paraphrase-multilingual-mpnet-base-v2`)
- OpenAI Whisper (`medium`) for audio/video transcription
- ReportLab for PDF export
- FastAPI + Uvicorn, tunneled publicly with pyngrok

## Backend

- Python
- FastAPI
- Uvicorn

## Data Processing

- pypdf, python-pptx, python-docx
- moviepy (video → audio extraction)

## Deployment

- Kaggle GPU (T4 x2 or better)
- ngrok tunnel

---

# 📡 AI Service Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Model name, quantization mode, device, active session count |
| POST | `/ingest` | Upload files for a session; builds the FAISS index |
| POST | `/generate-summary` | Returns Smart Summary + Important Topics + Revision Notes, exports both PDFs |
| POST | `/solve-exam` | Solves an uploaded exam file, or a single free-text question |
| GET | `/download` | Downloads a generated `summary` / `revision_notes` / `solved_exam` PDF |

---

# 📂 Project Structure

```text
Da7ee7-El-Dof3a/
│
├── ai_service/
│   ├── da7ee7-el-dof3a-kaggle-ai-service-3-improved.ipynb
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

### Running the AI Service (Kaggle)

1. Open `ai_service/da7ee7-el-dof3a-kaggle-ai-service-3-improved.ipynb` on Kaggle.
2. Enable **GPU T4 x2** (or better) under *Settings → Accelerator*.
3. Add a Kaggle secret named `NGROK_AUTH_TOKEN` with your ngrok auth token.
4. Run all cells — the notebook loads the model, starts FastAPI, and prints the public ngrok URL.
5. Copy that URL into the backend's `.env` as `KAGGLE_AI_BASE_URL` (a new URL is assigned every time the notebook restarts).

---

# 🚀 Usage

1. Upload lecture materials (slides, notes, recordings).
2. Wait for FAISS indexing.
3. Generate:
   - Smart Summary
   - Important Topics
   - Revision Notes
4. Upload a previous exam (or ask a single free-text question).
5. Receive AI-generated, source-grounded answers.
6. Download PDF reports.

---

# 📊 Results

✔ Upload and process lecture files (PDF, PPTX, DOCX, audio, video)

✔ Transcribe audio/video lectures with Whisper

✔ Build a multilingual FAISS vector database

✔ Generate full-course AI-powered summaries (Map-Reduce)

✔ Identify important topics automatically (ranked JSON)

✔ Produce structured revision notes (Must-Know / Formulas / Common Mistakes)

✔ Solve previous exams using RAG, including Arabic-numbered questions

✔ Export downloadable PDF reports

---

# 🔮 Future Improvements

- User authentication
- Multi-course support
- OCR for scanned PDFs
- Cloud deployment (move off Kaggle-session-only hosting)
- Chat with lecture materials
- Persistent session storage (sessions currently live only in the Kaggle notebook's memory for the duration of the run)

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
