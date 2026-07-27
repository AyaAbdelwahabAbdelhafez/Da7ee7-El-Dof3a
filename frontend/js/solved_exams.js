/**
 * solved_exams.js — Handles the "ask a question" and "solve full exam" flows
 * against POST /api/solve-exam, and renders the resulting Q&A list.
 */

function renderSolved(solvedQuestions) {
  const container = document.getElementById("solvedList");

  if (!solvedQuestions || solvedQuestions.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="icon">🧠</div>
        <p>No answer generated yet.</p>
      </div>`;
    return;
  }

  container.innerHTML = solvedQuestions
    .map(
      (item) => `
      <div class="qa-item">
        <div class="q">${item.question}</div>
        <div class="a">${item.answer}</div>
        ${
          item.confidence != null
            ? `<div class="confidence">confidence: ${(item.confidence * 100).toFixed(0)}%</div>`
            : ""
        }
      </div>`
    )
    .join("");

  document.getElementById("downloadExamBtn").style.display = "inline-flex";
}

function setLoading() {
  document.getElementById("solvedList").innerHTML = `
    <div class="empty-state">
      <span class="loader-dot"></span><span class="loader-dot"></span><span class="loader-dot"></span>
      <p style="margin-top:14px;">Solving with your lecture material as context…</p>
    </div>`;
}

document.addEventListener("DOMContentLoaded", () => {
  const sessionId = Api.getSession();
  if (!sessionId) {
    window.location.href = "upload.html";
    return;
  }

  // Populate the exam file dropdown from the last upload response, if available.
  const lastUpload = sessionStorage.getItem("dahih_last_upload");
  if (lastUpload) {
    const parsed = JSON.parse(lastUpload);
    const select = document.getElementById("examFileSelect");
    (parsed.files_received || [])
      .filter((name) => /exam|quiz|midterm/i.test(name))
      .forEach((name) => {
        const opt = document.createElement("option");
        opt.value = name;
        opt.textContent = name;
        select.appendChild(opt);
      });
  }

  document.getElementById("askBtn").addEventListener("click", async () => {
    const questionText = document.getElementById("questionInput").value.trim();
    if (!questionText) return;

    setLoading();
    try {
      const result = await Api.solveExam(sessionId, { questionText });
      renderSolved(result.solved_questions);
    } catch (err) {
      document.getElementById("solvedList").innerHTML =
        `<div class="empty-state"><p style="color:var(--coral);">${err.message}</p></div>`;
    }
  });

  document.getElementById("solveFileBtn").addEventListener("click", async () => {
    const examFilename = document.getElementById("examFileSelect").value;
    if (!examFilename) return;

    setLoading();
    try {
      const result = await Api.solveExam(sessionId, { examFilename });
      renderSolved(result.solved_questions);
    } catch (err) {
      document.getElementById("solvedList").innerHTML =
        `<div class="empty-state"><p style="color:var(--coral);">${err.message}</p></div>`;
    }
  });

  document.getElementById("downloadExamBtn").addEventListener("click", () => {
    Api.downloadFile(sessionId, "solved_exam");
  });
});
