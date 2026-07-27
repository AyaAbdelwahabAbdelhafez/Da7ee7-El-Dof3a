/**
 * processing.js — Drives the visual progress of the processing page while
 * the real work happens on the Kaggle AI service. Polls the backend for
 * the generated summary; once ready, stores it and unlocks "View results".
 */

const STAGES = ["upload", "extract", "transcribe", "embed", "generate", "done"];

let currentStageIndex = 0;

function setStageState(index) {
  STAGES.forEach((stage, i) => {
    const el = document.querySelector(`.stage-item[data-stage="${stage}"]`);
    el.classList.remove("active", "done");
    if (i < index) el.classList.add("done");
    if (i === index) el.classList.add("active");
  });

  const progress = Math.round((index / (STAGES.length - 1)) * 100);
  document.getElementById("progressBar").style.width = `${progress}%`;
  document.getElementById("progressLabel").textContent = `${progress}%`;
}

function advanceStageVisually() {
  if (currentStageIndex < STAGES.length - 2) {
    currentStageIndex += 1;
    setStageState(currentStageIndex);
  }
}

async function pollForResults(sessionId) {
  const maxAttempts = 60; // ~10 minutes at 10s intervals
  let attempt = 0;

  while (attempt < maxAttempts) {
    try {
      const summary = await Api.getSummary(sessionId);
      sessionStorage.setItem("dahih_summary", JSON.stringify(summary));
      setStageState(STAGES.length - 1);
      document.getElementById("viewResultsBtn").style.display = "inline-flex";
      return;
    } catch (err) {
      // Not ready yet or AI service still warming up — keep waiting.
    }
    attempt += 1;
    await new Promise((resolve) => setTimeout(resolve, 10000));
  }

  document.getElementById("progressLabel").textContent =
    "Taking longer than expected — check the Kaggle notebook / ngrok URL.";
}

document.addEventListener("DOMContentLoaded", () => {
  setStageState(0);

  const sessionId = Api.getSession();
  if (!sessionId) {
    window.location.href = "upload.html";
    return;
  }

  // Visually advance through early stages while we wait for the backend.
  const visualTimer = setInterval(advanceStageVisually, 4000);

  pollForResults(sessionId).finally(() => clearInterval(visualTimer));
});
