/**
 * summary.js — Loads the Smart Summary / Important Topics / Revision Notes,
 * either from cache (sessionStorage, set by processing.js) or by calling
 * POST /api/summary directly, and wires up tab switching + PDF export.
 */

function renderSummary(data) {
  document.getElementById("summaryCard").innerHTML = `<p>${data.smart_summary || "No summary available yet."}</p>`;

  const topicsHtml = (data.important_topics || [])
    .map((topic) => `<span class="topic-pill">${topic}</span>`)
    .join("");
  document.getElementById("topicsCard").innerHTML =
    topicsHtml || "<p>No topics extracted yet.</p>";

  document.getElementById("revisionCard").innerHTML = `<p style="white-space:pre-wrap;">${
    data.revision_notes || "No revision notes available yet."
  }</p>`;
}

function setupTabs() {
  const buttons = document.querySelectorAll(".tab-btn");
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".tab-panel").forEach((panel) => (panel.style.display = "none"));
      document.getElementById(`tab-${btn.dataset.tab}`).style.display = "block";
    });
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  setupTabs();

  const sessionId = Api.getSession();
  if (!sessionId) {
    window.location.href = "upload.html";
    return;
  }

  const cached = sessionStorage.getItem("dahih_summary");
  if (cached) {
    renderSummary(JSON.parse(cached));
  } else {
    try {
      const data = await Api.getSummary(sessionId);
      sessionStorage.setItem("dahih_summary", JSON.stringify(data));
      renderSummary(data);
    } catch (err) {
      document.getElementById("summaryCard").innerHTML = `<p style="color:var(--coral);">${err.message}</p>`;
    }
  }

  document.getElementById("downloadSummaryBtn").addEventListener("click", () => {
    Api.downloadFile(sessionId, "summary");
  });
});
