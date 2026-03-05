/* ═══════════════════════════════════════════════════════════════════════════
   BiteBot — Client Logic
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  "use strict";

  // ── DOM refs ──────────────────────────────────────────────────────────
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => document.querySelectorAll(s);

  const dropzone = $("#dropzone");
  const imageInput = $("#image-input");
  const dropzoneContent = $("#dropzone-content");
  const previewImage = $("#preview-image");
  const detectedBadge = $("#detected-badge");
  const detectedList = $("#detected-list");

  const ingredientsTA = $("#ingredients");
  const equipmentTA = $("#equipment");
  const dietaryInput = $("#dietary");
  const cuisineSelect = $("#cuisine");
  const timeLimitSelect = $("#time-limit");

  const generateBtn = $("#generate-btn");
  const btnText = $(".btn-text");
  const btnLoader = $("#btn-loader");

  const recipeSection = $("#recipe-output");
  const recipeContent = $("#recipe-content");
  const nutritionSection = $("#nutrition-output");
  const nutritionGrid = $("#nutrition-grid");

  const toast = $("#toast");
  const toastMsg = $("#toast-msg");

  // ── Toast ─────────────────────────────────────────────────────────────

  let toastTimer = null;
  function showToast(msg, duration = 4000) {
    toastMsg.textContent = msg;
    toast.classList.remove("hidden");
    requestAnimationFrame(() => toast.classList.add("visible"));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove("visible");
      setTimeout(() => toast.classList.add("hidden"), 300);
    }, duration);
  }

  // ── Dropzone ──────────────────────────────────────────────────────────

  dropzone.addEventListener("click", () => imageInput.click());
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("drag-over");
  });
  dropzone.addEventListener("dragleave", () => dropzone.classList.remove("drag-over"));
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("drag-over");
    if (e.dataTransfer.files.length) handleImageFile(e.dataTransfer.files[0]);
  });
  imageInput.addEventListener("change", () => {
    if (imageInput.files.length) handleImageFile(imageInput.files[0]);
  });

  async function handleImageFile(file) {
    // Preview
    const url = URL.createObjectURL(file);
    previewImage.src = url;
    previewImage.classList.remove("hidden");
    dropzoneContent.classList.add("hidden");

    // Detect
    const form = new FormData();
    form.append("image", file);

    try {
      const resp = await fetch("/api/detect", { method: "POST", body: form });
      const data = await resp.json();
      if (data.error) {
        showToast("⌫ Detection unavailable — enter ingredients manually");
        return;
      }
      if (data.ingredients && data.ingredients.length) {
        detectedList.textContent = data.ingredients.join(", ");
        detectedBadge.classList.remove("hidden");
        // Autofill
        const existing = ingredientsTA.value.trim();
        const detected = data.ingredients.join(", ");
        ingredientsTA.value = existing ? existing + ", " + detected : detected;
      }
    } catch {
      showToast("⌫ Could not connect to detection service");
    }
  }

  // ── Generate recipe ───────────────────────────────────────────────────

  generateBtn.addEventListener("click", handleGenerate);

  async function handleGenerate() {
    const ingredients = ingredientsTA.value.trim();
    const equipment = equipmentTA.value.trim();

    if (!ingredients) { showToast("⌦ Please list your ingredients"); return; }
    if (!equipment) { showToast("⌦ Please list your equipment"); return; }

    setLoading(true);

    try {
      const resp = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ingredients,
          equipment,
          dietary_restrictions: dietaryInput.value.trim(),
          cuisine: cuisineSelect.value,
          time_limit: timeLimitSelect.value,
        }),
      });

      const data = await resp.json();
      if (data.error) { showToast("⌫ " + data.error); setLoading(false); return; }

      // Render recipe
      recipeContent.innerHTML = markdownToHtml(data.recipe);
      recipeSection.classList.remove("hidden");
      recipeSection.scrollIntoView({ behavior: "smooth", block: "start" });

      // Fetch nutrition in parallel
      fetchNutrition(ingredients);
    } catch (err) {
      showToast("⌫ Failed to generate recipe");
    } finally {
      setLoading(false);
    }
  }

  async function fetchNutrition(ingredients) {
    try {
      const resp = await fetch("/api/nutrition", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients }),
      });
      const data = await resp.json();
      if (data.error || !data.nutrition || !data.nutrition.length) {
        nutritionSection.classList.add("hidden");
        return;
      }

      nutritionGrid.innerHTML = "";
      data.nutrition.forEach((item, i) => {
        const card = document.createElement("div");
        card.className = "nutrition-card";
        card.style.animationDelay = `${i * 0.08}s`;
        card.innerHTML = `
          <div class="nutrition-card-name">${escapeHtml(item.name || "Ingredient")}</div>
          ${nutritionRow("Calories", item.calories, "kcal")}
          ${nutritionRow("Protein", item.protein_g, "g")}
          ${nutritionRow("Fat", item.fat_total_g, "g")}
          ${nutritionRow("Carbs", item.carbohydrates_total_g, "g")}
          ${nutritionRow("Sugar", item.sugar_g, "g")}
        `;
        nutritionGrid.appendChild(card);
      });
      nutritionSection.classList.remove("hidden");
    } catch {
      // Silently fail nutrition — not critical
    }
  }

  function nutritionRow(label, val, unit) {
    if (typeof val === 'string' && val.toLowerCase().includes('premium')) {
      return `<div class="nutrition-stat">
                <span class="nutrition-stat-label">${label}</span>
                <span class="nutrition-premium-badge">★ Premium Only</span>
              </div>`;
    }
    const display = val != null ? `${val} ${unit}` : "—";
    return `<div class="nutrition-stat">
              <span class="nutrition-stat-label">${label}</span>
              <span class="nutrition-stat-value">${display}</span>
            </div>`;
  }

  // ── Loading state ─────────────────────────────────────────────────────

  function setLoading(on) {
    generateBtn.disabled = on;
    if (on) {
      btnText.style.opacity = "0";
      btnLoader.classList.remove("hidden");
    } else {
      btnText.style.opacity = "1";
      btnLoader.classList.add("hidden");
    }
  }

  // ── Minimal Markdown → HTML ───────────────────────────────────────────
  // Handles headings, bold, italic, lists, and paragraphs.

  function markdownToHtml(md) {
    if (!md) return "";
    let html = escapeHtml(md);

    // Headings
    html = html.replace(/^#### (.+)$/gm, "<h4>$1</h4>");
    html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
    html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");
    html = html.replace(/^# (.+)$/gm, "<h1>$1</h1>");

    // Bold + Italic
    html = html.replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>");
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");

    // Unordered lists
    html = html.replace(/^[•\-\*] (.+)$/gm, "<li>$1</li>");

    // Ordered lists (1. 2. etc.)
    html = html.replace(/^\d+\.\s(.+)$/gm, "<li>$1</li>");

    // Wrap consecutive <li> in <ul>
    html = html.replace(/((?:<li>.+<\/li>\n?)+)/g, "<ul>$1</ul>");

    // Paragraphs — wrap remaining plain lines
    html = html.split("\n").map((line) => {
      line = line.trim();
      if (!line) return "";
      if (/^<[hulo]/.test(line)) return line;
      return `<p>${line}</p>`;
    }).join("\n");

    return html;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // ── Smooth nav background on scroll ───────────────────────────────────

  const nav = $("#topnav");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 80) {
      nav.style.background = "rgba(255, 253, 249, .95)";
    } else {
      nav.style.background = "rgba(255, 253, 249, .8)";
    }
  }, { passive: true });

})();
