/**
 * results.js — Wires up the download buttons on the Results overview page.
 */

document.addEventListener("DOMContentLoaded", () => {
  const sessionId = Api.getSession();
  if (!sessionId) {
    window.location.href = "upload.html";
    return;
  }

  document.getElementById("sessionNote").textContent =
    `Here's what Da7ee7-El-Dof3a produced from your uploaded material (session ${sessionId}).`;

  document.querySelectorAll("[data-download]").forEach((btn) => {
    btn.addEventListener("click", () => {
      Api.downloadFile(sessionId, btn.dataset.download);
    });
  });
});
