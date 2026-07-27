/**
 * upload.js — Drag & drop file collection, category detection, and submission
 * to POST /api/upload. On success, redirects to processing.html.
 */

const CATEGORY_RULES = {
  slides: [".pdf"],
  ppt: [".ppt", ".pptx"],
  exam: [], // detected by filename heuristics below
  audio: [".mp3", ".wav", ".m4a"],
  video: [".mp4", ".mov", ".mkv"],
};

let selectedFiles = [];

function extOf(name) {
  const idx = name.lastIndexOf(".");
  return idx === -1 ? "" : name.slice(idx).toLowerCase();
}

function detectCategory(file) {
  const ext = extOf(file.name);
  const lowerName = file.name.toLowerCase();

  if (lowerName.includes("exam") || lowerName.includes("quiz") || lowerName.includes("midterm")) {
    return "exam";
  }
  if (CATEGORY_RULES.ppt.includes(ext)) return "ppt";
  if (CATEGORY_RULES.slides.includes(ext)) return "slides";
  if (CATEGORY_RULES.audio.includes(ext)) return "audio";
  if (CATEGORY_RULES.video.includes(ext)) return "video";
  return "other";
}

function renderFileList() {
  const list = document.getElementById("fileList");
  list.innerHTML = "";

  selectedFiles.forEach((file, index) => {
    const row = document.createElement("div");
    row.className = "file-row";
    row.innerHTML = `
      <div>
        <div class="name">${file.name}</div>
      </div>
      <div style="display:flex; align-items:center; gap:12px;">
        <span class="type-tag">${detectCategory(file)}</span>
        <button class="remove" data-index="${index}" aria-label="Remove file">✕</button>
      </div>
    `;
    list.appendChild(row);
  });

  document.querySelectorAll(".remove").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const idx = Number(e.currentTarget.dataset.index);
      selectedFiles.splice(idx, 1);
      renderFileList();
      updateChecklist();
      updateSubmitState();
    });
  });
}

function updateChecklist() {
  const presentCategories = new Set(selectedFiles.map(detectCategory));
  document.querySelectorAll("#checklist .item").forEach((item) => {
    const cat = item.dataset.cat;
    item.classList.toggle("done", presentCategories.has(cat));
  });
}

function updateSubmitState() {
  document.getElementById("submitBtn").disabled = selectedFiles.length === 0;
}

function addFiles(fileList) {
  for (const file of fileList) {
    // avoid duplicate name+size entries
    if (!selectedFiles.some((f) => f.name === file.name && f.size === file.size)) {
      selectedFiles.push(file);
    }
  }
  renderFileList();
  updateChecklist();
  updateSubmitState();
}

document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const submitBtn = document.getElementById("submitBtn");
  const errorBox = document.getElementById("uploadError");

  dropZone.addEventListener("click", () => fileInput.click());

  ["dragenter", "dragover"].forEach((evt) =>
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropZone.classList.add("dragover");
    })
  );

  ["dragleave", "drop"].forEach((evt) =>
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");
    })
  );

  dropZone.addEventListener("drop", (e) => {
    addFiles(e.dataTransfer.files);
  });

  fileInput.addEventListener("change", (e) => {
    addFiles(e.target.files);
  });

  submitBtn.addEventListener("click", async () => {
    errorBox.style.display = "none";
    submitBtn.disabled = true;
    submitBtn.textContent = "Uploading…";

    try {
      const response = await Api.uploadFiles(selectedFiles);
      sessionStorage.setItem("dahih_last_upload", JSON.stringify(response));
      window.location.href = "processing.html";
    } catch (err) {
      errorBox.textContent = err.message || "Upload failed. Please try again.";
      errorBox.style.display = "block";
      submitBtn.disabled = false;
      submitBtn.textContent = "Upload & start processing →";
    }
  });
});
