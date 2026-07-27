/**
 * api.js — Central Fetch API wrapper for the Da7ee7-El-Dof3a frontend.
 * The frontend talks ONLY to the local FastAPI backend, never to Kaggle directly.
 */

const API_BASE = "http://127.0.0.1:8000";

const SESSION_KEY = "dahih_session_id";

const Api = {
  /** Persist the active session id (returned by /api/upload) in localStorage. */
  setSession(sessionId) {
    localStorage.setItem(SESSION_KEY, sessionId);
  },

  getSession() {
    return localStorage.getItem(SESSION_KEY);
  },

  clearSession() {
    localStorage.removeItem(SESSION_KEY);
  },

  async _handle(response) {
    if (!response.ok) {
      let detail = `Request failed (${response.status})`;
      try {
        const body = await response.json();
        detail = body.detail || detail;
      } catch (_) { /* ignore parse errors */ }
      throw new Error(detail);
    }
    return response.json();
  },

  /** GET /api/health */
  async health() {
    const res = await fetch(`${API_BASE}/api/health`);
    return this._handle(res);
  },

  /** POST /api/upload (multipart/form-data with multiple files) */
  async uploadFiles(fileList, onProgress) {
    const formData = new FormData();
    for (const file of fileList) {
      formData.append("files", file);
    }

    const res = await fetch(`${API_BASE}/api/upload`, {
      method: "POST",
      body: formData,
    });
    const data = await this._handle(res);
    if (data.session_id) this.setSession(data.session_id);
    return data;
  },

  /** POST /api/summary */
  async getSummary(sessionId) {
    const res = await fetch(`${API_BASE}/api/summary`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    });
    return this._handle(res);
  },

  /** POST /api/solve-exam */
  async solveExam(sessionId, { examFilename = null, questionText = null } = {}) {
    const res = await fetch(`${API_BASE}/api/solve-exam`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        exam_filename: examFilename,
        question_text: questionText,
      }),
    });
    return this._handle(res);
  },

  /** GET /api/download?session_id=...&file_type=... — triggers a browser download */
  downloadFile(sessionId, fileType) {
    const url = `${API_BASE}/api/download?session_id=${encodeURIComponent(sessionId)}&file_type=${encodeURIComponent(fileType)}`;
    window.open(url, "_blank");
  },
};
