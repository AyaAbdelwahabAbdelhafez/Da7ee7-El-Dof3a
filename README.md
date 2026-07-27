# Da7ee7-El-Dof3a (دحيح الدفعة)

AI-powered exam preparation system. Upload lecture slides, PowerPoints,
previous exams, and lecture audio/video — get back a Smart Summary,
Important Topics, Solved Previous Exams, and Final Revision Notes.

See `docs/ARCHITECTURE.md` for the full system design.

## Project structure

```
Da7ee7-El-Dof3a/
├── frontend/            Static HTML/CSS/JS site (Home, Upload, Processing, Results, Summary, Solved Exams)
├── backend/              FastAPI service — runs locally, proxies to Kaggle
│   └── app/
│       ├── main.py            App entrypoint (CORS, logging, routers)
│       ├── config.py          Settings (.env-driven)
│       ├── routers/           upload / summary / solve_exam / download / health
│       ├── services/          file_storage.py, kaggle_client.py
│       ├── models/            Pydantic schemas
│       └── utils/             logger.py
├── ai_service/            Everything that runs on Kaggle GPU
│   ├── Da7ee7_El_Dof3a_Kaggle_AI_Service.ipynb   ← upload this to Kaggle
│   ├── prompts/            Standalone prompt template modules (mirrors notebook cell 8)
│   └── requirements.txt
├── docs/                  Architecture notes
├── uploads/               Local file storage (backend), gitignored contents
└── outputs/               Generated PDFs (backend cache), gitignored contents
```

## Running it

### 1. AI Service (Kaggle)

1. Upload `ai_service/Da7ee7_El_Dof3a_Kaggle_AI_Service.ipynb` to Kaggle.
2. Turn on a GPU accelerator (Settings → Accelerator → GPU T4 x2 or better).
3. Add a Kaggle secret named `NGROK_AUTH_TOKEN` (Add-ons → Secrets) with your
   [ngrok](https://ngrok.com) auth token. If any candidate LLM is gated
   (Llama, Gemma), also add an `HF_TOKEN` secret after accepting its license
   on Hugging Face.
4. Run all cells. The last cell prints a public URL, e.g.
   `https://xxxx-xx-xx.ngrok-free.app`.

### 2. Backend (local)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# paste the ngrok URL from Kaggle into KAGGLE_AI_BASE_URL inside .env
uvicorn app.main:app --reload --port 8000
```

Backend docs: http://127.0.0.1:8000/docs

### 3. Frontend (local)

The frontend is fully static — open `frontend/index.html` directly in a
browser, or serve it:

```bash
cd frontend
python -m http.server 5500
```

Then visit `http://127.0.0.1:5500`. It talks to the backend at
`http://127.0.0.1:8000` (configured in `frontend/js/api.js`).

## APIs exposed by the backend

| Method | Path              | Purpose                                      |
|--------|-------------------|-----------------------------------------------|
| GET    | `/api/health`     | Backend + Kaggle/ngrok reachability            |
| POST   | `/api/upload`     | Upload files, kicks off Kaggle ingestion       |
| POST   | `/api/summary`    | Smart Summary + Important Topics + Revision Notes |
| POST   | `/api/solve-exam` | Solve a previous exam file or a free-text question |
| GET    | `/api/download`   | Download a generated PDF                       |

## Notes

- Every session is keyed by a `session_id` returned from `/api/upload`.
- The notebook keeps FAISS indexes and generated content in memory/disk for
  the life of the Kaggle session — restarting the notebook clears them.
- ngrok assigns a new URL every run; update `backend/.env` each time.
