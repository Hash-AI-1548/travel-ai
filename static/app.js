// Global state
let currentStep = 1;
let token = localStorage.getItem("travel_ai_token") || null;
let user = null;
let authMode = "login";

const passport = {
  full_name: "Evelyn Thorne",
  age: 29,
  gender: "Female",
  nationality: "Indian",
  home_city: "Mumbai",
  personal_notes: "Celebrating 5th wedding anniversary",
  profile_picture_url: null,
  languages_spoken: ["English", "Hindi"],
  traveler_type: "couple",
  traveler_type_custom: "",
  accessibility_mobility: true,
  accessibility_visual: false,
  accessibility_hearing: false,
  accessibility_senior: false,
  accessibility_child: false,
  accessibility_none: false,
  accessibility_custom: "",
  travel_styles: ["adventure", "nature", "culture", "food", "photography"],
  travel_styles_custom: "",
  dietary_standards: ["vegetarian", "halal"],
  allergies_restrictions: "Severe peanut allergy, prefers gluten-free options where possible",
  food_custom: "",
  pack_styles: ["western", "casual"],
  modest_clothing: true,
  prioritize_hot_weather: false,
  clothing_custom: "",
  budget_tier: "moderate",
  budget_currency: "INR",
  budget_custom: "50000",
  budget_standardized_usd: "≈ $595 USD",
  current_step: 1
};

const allLanguages = [
  "English", "Spanish", "French", "German", "Mandarin Chinese", "Cantonese",
  "Japanese", "Hindi", "Arabic", "Portuguese", "Russian", "Bengali", "Italian",
  "Korean", "Turkish", "Vietnamese", "Polish", "Dutch", "Swedish", "Greek",
  "Thai", "Indonesian", "Malay", "Persian / Farsi", "Hebrew", "Tagalog / Filipino",
  "Swahili", "Punjabi", "Telugu", "Tamil", "Marathi", "Urdu", "Gujarati",
  "Kannada", "Malayalam", "Ukrainian", "Romanian", "Czech", "Hungarian",
  "Danish", "Finnish", "Norwegian", "Irish", "Croatian", "Serbian", "Slovak",
  "Bulgarian", "Lithuanian", "Latvian", "Estonian", "Icelandic", "Basque",
  "Catalan", "Galician", "Welsh", "Scottish Gaelic", "Yoruba", "Igbo",
  "Hausa", "Zulu", "Xhosa", "Amharic", "Somali", "Nepali", "Sinhala",
  "Burmese", "Khmer", "Lao", "Mongolian", "Georgian", "Armenian", "Azerbaijani",
  "Kazakh", "Uzbek", "Esperanto", "Latin", "Afrikaans", "Albanian", "Bosnian"
];

const currencyRates = {
  INR: { rate: 0.0119, symbol: "₹", name: "Indian Rupee" },
  USD: { rate: 1.0, symbol: "$", name: "US Dollar" },
  EUR: { rate: 1.087, symbol: "€", name: "Euro" },
  GBP: { rate: 1.266, symbol: "£", name: "British Pound" },
  AED: { rate: 0.272, symbol: "د.إ", name: "UAE Dirham" },
  CAD: { rate: 0.735, symbol: "C$", name: "Canadian Dollar" },
  AUD: { rate: 0.658, symbol: "A$", name: "Australian Dollar" },
  SGD: { rate: 0.746, symbol: "S$", name: "Singapore Dollar" },
  JPY: { rate: 0.00658, symbol: "¥", name: "Japanese Yen" },
  SAR: { rate: 0.267, symbol: "﷼", name: "Saudi Riyal" },
  QAR: { rate: 0.275, symbol: "QR", name: "Qatari Riyal" },
  KWD: { rate: 3.26, symbol: "KD", name: "Kuwaiti Dinar" },
  BHD: { rate: 2.65, symbol: "BD", name: "Bahraini Dinar" },
  OMR: { rate: 2.60, symbol: "OMR", name: "Omani Rial" },
  CHF: { rate: 1.136, symbol: "Fr", name: "Swiss Franc" },
  CNY: { rate: 0.138, symbol: "¥", name: "Chinese Yuan" },
  HKD: { rate: 0.128, symbol: "HK$", name: "Hong Kong Dollar" },
  NZD: { rate: 0.612, symbol: "NZ$", name: "New Zealand Dollar" },
  THB: { rate: 0.0274, symbol: "฿", name: "Thai Baht" },
  MYR: { rate: 0.213, symbol: "RM", name: "Malaysian Ringgit" },
  IDR: { rate: 0.0000625, symbol: "Rp", name: "Indonesian Rupiah" },
  PHP: { rate: 0.0175, symbol: "₱", name: "Philippine Peso" },
  VND: { rate: 0.000039, symbol: "₫", name: "Vietnamese Dong" },
  KRW: { rate: 0.000725, symbol: "₩", name: "South Korean Won" },
  PKR: { rate: 0.0036, symbol: "₨", name: "Pakistani Rupee" },
  BDT: { rate: 0.0085, symbol: "৳", name: "Bangladeshi Taka" },
  LKR: { rate: 0.0033, symbol: "Rs", name: "Sri Lankan Rupee" },
  NPR: { rate: 0.0075, symbol: "Rs", name: "Nepalese Rupee" },
  BRL: { rate: 0.183, symbol: "R$", name: "Brazilian Real" },
  ZAR: { rate: 0.054, symbol: "R", name: "South African Rand" },
  TRY: { rate: 0.029, symbol: "₺", name: "Turkish Lira" },
  RUB: { rate: 0.011, symbol: "₽", name: "Russian Ruble" },
  MXN: { rate: 0.0549, symbol: "Mex$", name: "Mexican Peso" }
};

// ================= STEP NAVIGATION =================
function goToStep(stepNum) {
  saveCurrentStepDOM();
  currentStep = Math.max(1, Math.min(stepNum, 8));

  // Update step sections
  for (let i = 1; i <= 8; i++) {
    const sec = document.getElementById(`step-section-${i}`);
    if (sec) sec.style.display = i === currentStep ? "block" : "none";

    const nav = document.getElementById(`nav-step-${i}`);
    const numEl = document.getElementById(`nav-num-${i}`);
    if (nav) {
      nav.classList.remove("active", "completed");
      if (i === currentStep) {
        nav.classList.add("active");
        if (numEl) numEl.innerText = i;
      } else if (i < currentStep) {
        nav.classList.add("completed");
        if (numEl) numEl.innerHTML = "&#10003;";
      } else {
        if (numEl) numEl.innerText = i;
      }
    }
  }

  // Update counter & progress bar
  const counter = document.getElementById("step-counter");
  if (counter) counter.innerText = `STEP ${currentStep} OF 8`;
  const fill = document.getElementById("progress-fill");
  if (fill) fill.style.width = `${(currentStep / 8) * 100}%`;

  // Update buttons
  const backBtn = document.getElementById("back-btn");
  if (backBtn) backBtn.style.visibility = currentStep === 1 ? "hidden" : "visible";

  const nextBtn = document.getElementById("next-btn");
  if (nextBtn) {
    if (currentStep === 8) {
      nextBtn.innerHTML = `Continue to Plan My Trip <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
    } else {
      nextBtn.innerHTML = `Continue <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
    }
  }

  if (currentStep === 8) {
    updateSummaryCards();
  }

  const panel = document.querySelector(".content-panel");
  if (panel) panel.scrollTo({ top: 0, behavior: "smooth" });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function nextStep() {
  if (currentStep < 8) {
    goToStep(currentStep + 1);
  } else {
    showTripPlannerModal();
  }
}

function prevStep() {
  if (currentStep > 1) {
    goToStep(currentStep - 1);
  }
}

function saveCurrentStepDOM() {
  const fn = document.getElementById("inp-fullname");
  if (fn) passport.full_name = fn.value;
  const age = document.getElementById("inp-age");
  if (age) passport.age = parseInt(age.value) || 29;
  const gen = document.getElementById("inp-gender");
  if (gen) passport.gender = gen.value;
  const nat = document.getElementById("inp-nationality");
  if (nat) passport.nationality = nat.value;
  const city = document.getElementById("inp-homecity");
  if (city) passport.home_city = city.value;
  const pn = document.getElementById("inp-personal-notes");
  if (pn) passport.personal_notes = pn.value;

  const ttc = document.getElementById("inp-traveler-type-custom");
  if (ttc) passport.traveler_type_custom = ttc.value;

  const ac = document.getElementById("inp-accessibility-custom");
  if (ac) passport.accessibility_custom = ac.value;

  const tsc = document.getElementById("inp-travel-styles-custom");
  if (tsc) passport.travel_styles_custom = tsc.value;

  const all = document.getElementById("inp-allergies");
  if (all) passport.allergies_restrictions = all.value;
  const fc = document.getElementById("inp-food-custom");
  if (fc) passport.food_custom = fc.value;

  const cc = document.getElementById("inp-clothing-custom");
  if (cc) passport.clothing_custom = cc.value;

  const curr = document.getElementById("inp-budget-currency");
  if (curr) passport.budget_currency = curr.value;
  const bc = document.getElementById("inp-budget-custom");
  if (bc) passport.budget_custom = bc.value;

  // Sync to backend asynchronously if user is logged in
  if (token) {
    fetch("/api/v1/passport", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(passport)
    }).catch(() => {});
  }
}

// ================= STEP 1: LANGUAGES & AVATAR =================
function handleLanguageSearch(query) {
  const dropdown = document.getElementById("lang-suggestions");
  if (!dropdown) return;
  const trimmed = query.trim().toLowerCase();
  if (!trimmed) {
    dropdown.style.display = "none";
    dropdown.innerHTML = "";
    return;
  }
  const currentSet = new Set(passport.languages_spoken || []);
  const matches = allLanguages.filter(l => l.toLowerCase().includes(trimmed) && !currentSet.has(l)).slice(0, 8);

  if (matches.length === 0) {
    dropdown.innerHTML = `
      <div class="lang-suggestion-item" onclick="addLanguage('${query.replace(/'/g, "\\'")}')">
        <span>Add <strong>"${query}"</strong> as custom language</span>
        <span style="font-size:11px; color:var(--primary); font-weight:700;">+ Add</span>
      </div>
    `;
  } else {
    dropdown.innerHTML = matches.map(lang => `
      <div class="lang-suggestion-item" onclick="addLanguage('${lang.replace(/'/g, "\\'")}')">
        <span>${lang}</span>
        <span style="font-size:11px; color:var(--primary); font-weight:700;">+ Select</span>
      </div>
    `).join('');
  }
  dropdown.style.display = "block";
}

function handleLanguageKeydown(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    addCustomLanguageFromInput();
  }
}

function addCustomLanguageFromInput() {
  const input = document.getElementById("lang-search-input");
  if (!input) return;
  const val = input.value.trim();
  if (val) {
    addLanguage(val);
    input.value = "";
    const dropdown = document.getElementById("lang-suggestions");
    if (dropdown) dropdown.style.display = "none";
  }
}

function addLanguage(lang) {
  if (!lang) return;
  if (!passport.languages_spoken) passport.languages_spoken = [];
  if (!passport.languages_spoken.includes(lang)) {
    passport.languages_spoken.push(lang);
    renderSelectedLanguages();
  }
}

function removeLanguage(lang) {
  if (!passport.languages_spoken) return;
  passport.languages_spoken = passport.languages_spoken.filter(l => l !== lang);
  renderSelectedLanguages();
}

function toggleLanguage(lang, el) {
  if (!passport.languages_spoken) passport.languages_spoken = [];
  if (passport.languages_spoken.includes(lang)) {
    removeLanguage(lang);
    if (el) { el.classList.remove("selected"); el.innerHTML = `${lang} +`; }
  } else {
    addLanguage(lang);
    if (el) { el.classList.add("selected"); el.innerHTML = `${lang} &#10003;`; }
  }
}

function renderSelectedLanguages() {
  const container = document.getElementById("selected-langs-box");
  const countEl = document.getElementById("lang-count");
  if (countEl) countEl.innerText = passport.languages_spoken.length;
  if (!container) return;

  container.innerHTML = passport.languages_spoken.map(lang => `
    <span class="selected-lang-chip">
      ${lang}
      <span class="chip-remove" onclick="removeLanguage('${lang.replace(/'/g, "\\'")}')">&times;</span>
    </span>
  `).join('');

  // Update pills
  const pills = document.querySelectorAll("#popular-langs-container .pill-tag");
  pills.forEach(pill => {
    const rawText = pill.innerText.replace(/[\+\u2713]/g, '').trim();
    const isSel = passport.languages_spoken.includes(rawText);
    pill.classList.toggle("selected", isSel);
    pill.innerHTML = `${rawText} ${isSel ? '&#10003;' : '+'}`;
  });
}

function handleAvatarUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    passport.profile_picture_url = e.target.result;
    const dropzone = document.getElementById("avatar-dropzone");
    if (dropzone) {
      dropzone.innerHTML = `<img src="${e.target.result}" class="avatar-preview-img">`;
    }
  };
  reader.readAsDataURL(file);

  if (token) {
    const formData = new FormData();
    formData.append("file", file);
    fetch("/api/v1/passport/avatar", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: formData
    }).catch(() => {});
  }
}

// ================= STEP 2: TRAVELER TYPE =================
function selectTravelerType(typeId, el) {
  el.parentElement.querySelectorAll(".select-card").forEach(c => c.classList.remove("selected"));
  el.classList.add("selected");
  passport.traveler_type = typeId;
}

// ================= STEP 3: ACCESSIBILITY =================
function toggleAccessibility(key, input) {
  if (key === "accessibility_none") {
    if (input.checked) {
      // Uncheck all other accessibility options
      const otherKeys = [
        "accessibility_mobility",
        "accessibility_visual",
        "accessibility_hearing",
        "accessibility_senior",
        "accessibility_child"
      ];
      const otherIds = ["chk-mobility", "chk-visual", "chk-hearing", "chk-senior", "chk-child"];
      otherKeys.forEach(k => passport[k] = false);
      otherIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.checked = false;
          const c = el.closest(".toggle-card");
          if (c) c.classList.remove("active");
        }
      });
      passport.accessibility_none = true;
      const card = input.closest(".toggle-card");
      if (card) card.classList.add("active");
    } else {
      passport.accessibility_none = false;
      const card = input.closest(".toggle-card");
      if (card) card.classList.remove("active");
    }
  } else {
    // If any specific accommodation is checked, uncheck "None"
    passport[key] = input.checked;
    const card = input.closest(".toggle-card");
    if (card) card.classList.toggle("active", input.checked);

    if (input.checked) {
      passport.accessibility_none = false;
      const noneInput = document.getElementById("chk-none");
      if (noneInput) {
        noneInput.checked = false;
        const noneCard = noneInput.closest(".toggle-card");
        if (noneCard) noneCard.classList.remove("active");
      }
    }
  }
}

// ================= STEP 4: TRAVEL STYLES =================
function toggleStyleCard(styleId, el) {
  el.classList.toggle("selected");
  if (!passport.travel_styles) passport.travel_styles = [];
  if (passport.travel_styles.includes(styleId)) {
    passport.travel_styles = passport.travel_styles.filter(s => s !== styleId);
  } else {
    passport.travel_styles.push(styleId);
  }
  const count = passport.travel_styles.length;
  const badge = document.getElementById("style-badge");
  if (badge) {
    badge.innerHTML = `<span>&#9432; <strong>${count} styles selected</strong> ${count >= 3 ? '— Great selection! This unlocks specialized local guide layers.' : '— Please select at least 3 styles for optimal itinerary generation.'}</span>`;
  }
}

// ================= STEP 5: FOOD PREFERENCES =================
function toggleDiet(dietId, el) {
  el.classList.toggle("selected");
  if (!passport.dietary_standards) passport.dietary_standards = [];
  if (passport.dietary_standards.includes(dietId)) {
    passport.dietary_standards = passport.dietary_standards.filter(d => d !== dietId);
  } else {
    passport.dietary_standards.push(dietId);
  }
}

// ================= STEP 6: CLOTHING =================
function togglePackStyle(styleName, el) {
  el.classList.toggle("selected");
  if (!passport.pack_styles) passport.pack_styles = [];
  if (passport.pack_styles.includes(styleName)) {
    passport.pack_styles = passport.pack_styles.filter(s => s !== styleName);
    el.innerHTML = `${styleName.charAt(0).toUpperCase() + styleName.slice(1)} +`;
  } else {
    passport.pack_styles.push(styleName);
    el.innerHTML = `${styleName.charAt(0).toUpperCase() + styleName.slice(1)} &#10003;`;
  }
}

function toggleModesty(checked) {
  passport.modest_clothing = checked;
  const card = document.getElementById("inp-modest")?.closest(".toggle-card");
  if (card) card.classList.toggle("active", checked);
}

function toggleHotWeather(checked) {
  passport.prioritize_hot_weather = checked;
  const card = document.getElementById("inp-hotweather")?.closest(".toggle-card");
  if (card) card.classList.toggle("active", checked);
}

// ================= STEP 7: BUDGET & USD CONVERSION =================
// ================= STEP 7: BUDGET & USD CONVERSION =================
let isRoundOffActive = false;

function handleCurrencyChange(val) {
  passport.budget_currency = val;
  const info = currencyRates[val] || { symbol: val };
  document.querySelectorAll(".curr-symbol").forEach(el => {
    el.innerText = info.symbol || val;
  });
  calculateSplitupTotal();
}

function handleBudgetCustom(val) {
  passport.budget_custom = val;
  updateBudgetConversionBadge();
}

function addCustomSplitupRow(purpose = "Custom Activity / Reserve", amount = 1000) {
  const container = document.getElementById("budget-splitup-list");
  if (!container) return;
  const currCode = (passport.budget_currency || "INR").trim().toUpperCase();
  const info = currencyRates[currCode] || { symbol: currCode };

  const row = document.createElement("div");
  row.className = "splitup-row";
  row.style.cssText = "display:flex; gap:12px; align-items:center; background:#F8FAF9; padding:12px 16px; border-radius:10px; border:1px solid var(--border-color);";
  row.innerHTML = `
    <div style="flex:2; font-size:13px; font-weight:700; color:var(--text-main); display:flex; align-items:center; gap:8px;">
      <span>✨</span>
      <input type="text" class="split-purpose" value="${purpose}" style="font-weight:700; border:none; background:transparent; width:100%; font-size:13px;" oninput="calculateSplitupTotal()">
    </div>
    <div style="flex:1; display:flex; align-items:center; gap:6px;">
      <span class="curr-symbol" style="font-weight:800; color:var(--text-muted);">${info.symbol || '₹'}</span>
      <input type="number" class="split-amount" value="${amount}" min="0" step="500" style="height:40px; border-radius:8px; border:1.5px solid var(--border-color); padding:0 10px; width:100%; font-weight:700;" oninput="calculateSplitupTotal()">
    </div>
    <button type="button" onclick="removeSplitupRow(this)" style="background:none; border:none; color:#C62828; font-size:18px; cursor:pointer; padding:0 6px;">&times;</button>
  `;
  container.appendChild(row);
  calculateSplitupTotal();
}

function removeSplitupRow(btn) {
  const row = btn.closest(".splitup-row");
  if (row) row.remove();
  calculateSplitupTotal();
}

function toggleRoundOff(checked) {
  isRoundOffActive = checked;
  calculateSplitupTotal();
}

function calculateSplitupTotal() {
  const rows = document.querySelectorAll("#budget-splitup-list .splitup-row");
  let sum = 0;
  const breakdown = [];
  rows.forEach(r => {
    const purpose = r.querySelector(".split-purpose")?.value || "Expense";
    const amt = parseFloat(r.querySelector(".split-amount")?.value || "0") || 0;
    sum += amt;
    breakdown.push({ purpose, amount: amt });
  });

  if (isRoundOffActive && sum > 0) {
    if (sum < 1000) {
      sum = Math.round(sum / 50) * 50;
    } else if (sum < 5000) {
      sum = Math.round(sum / 100) * 100;
    } else {
      sum = Math.round(sum / 500) * 500;
    }
  }

  const currCode = (passport.budget_currency || "INR").trim().toUpperCase();
  const info = currencyRates[currCode] || { symbol: currCode };
  const display = document.getElementById("splitup-total-display");
  if (display) {
    display.innerText = `${currCode} ${info.symbol || ''}${sum.toLocaleString()}${isRoundOffActive ? ' (Rounded)' : ''}`;
  }

  const customInp = document.getElementById("inp-budget-custom");
  if (customInp) {
    customInp.value = `${sum.toLocaleString()}${isRoundOffActive ? ' (Rounded)' : ''}`;
  }
  passport.budget_custom = `${sum}`;
  passport.budget_breakdown = breakdown;

  updateBudgetConversionBadge();
}

function updateBudgetConversionBadge() {
  const currCode = (passport.budget_currency || "INR").trim().toUpperCase();
  const customVal = passport.budget_custom || "";
  const info = currencyRates[currCode] || { rate: 0.0119, symbol: currCode, name: currCode };
  const badgeText = document.getElementById("conversion-text");
  if (!badgeText) return;

  if (!customVal.trim()) {
    badgeText.innerHTML = `Standardized for Global Itinerary Planning: <em>Enter a budget amount above</em>`;
    passport.budget_standardized_usd = null;
    return;
  }

  const nums = customVal.match(/\b\d+(?:,\d+)*(?:\.\d+)?\b/g);
  if (!nums || nums.length === 0) {
    badgeText.innerHTML = `Standardized for Global Itinerary Planning: ≈ ${customVal} (${currCode})`;
    passport.budget_standardized_usd = `${customVal} (${currCode})`;
    return;
  }

  if (nums.length >= 2) {
    const lowUsd = Math.round(parseFloat(nums[0].replace(/,/g, '')) * info.rate);
    const highUsd = Math.round(parseFloat(nums[1].replace(/,/g, '')) * info.rate);
    const formatted = `≈ $${lowUsd.toLocaleString()} – $${highUsd.toLocaleString()} USD (Converted from ${currCode} ${info.symbol})`;
    badgeText.innerHTML = `Standardized for Global Itinerary Planning: <strong>${formatted}</strong>`;
    passport.budget_standardized_usd = formatted;
  } else {
    const valUsd = Math.round(parseFloat(nums[0].replace(/,/g, '')) * info.rate);
    const formatted = `≈ $${valUsd.toLocaleString()} USD (Converted from ${currCode} ${info.symbol})`;
    badgeText.innerHTML = `Standardized for Global Itinerary Planning: <strong>${formatted}</strong>`;
    passport.budget_standardized_usd = formatted;
  }
}

// ================= STEP 8: SUMMARY REVIEW =================
function updateSummaryCards() {
  saveCurrentStepDOM();
  const p = passport;
  const styles = (p.travel_styles || []).map(s => s.replace("_", " ").toUpperCase());
  if (p.travel_styles_custom) styles.push(`+ ${p.travel_styles_custom.toUpperCase()}`);
  const diets = (p.dietary_standards || []).map(d => d.replace("_", " ").toUpperCase());
  const pack = (p.pack_styles || []).map(ps => ps.toUpperCase()).join(", ");
  const nat = p.nationality ? ` (${p.nationality})` : "";

  const curr = p.budget_currency || "INR";
  const customAmt = p.budget_custom || "50,000";
  const usdNote = p.budget_standardized_usd ? ` [${p.budget_standardized_usd}]` : "";

  const setHtml = (id, html) => { const el = document.getElementById(id); if (el) el.innerHTML = html; };

  setHtml("sum-personal-headline", `${p.full_name || 'Evelyn Thorne'}, ${p.age || 29} • ${p.gender || 'Female'}${nat}`);
  setHtml("sum-personal-subtext", `Home: ${p.home_city || 'Mumbai'} • ${(p.languages_spoken || []).join(', ')}${p.personal_notes ? ` • Note: ${p.personal_notes}` : ''}`);
  
  setHtml("sum-type-headline", `${(p.traveler_type || 'couple').toUpperCase()} Configuration`);
  setHtml("sum-type-subtext", p.traveler_type_custom ? `Custom: ${p.traveler_type_custom}` : "Intimate private tour routes, romantic stays, fine dining");

  setHtml("sum-access-headline", p.accessibility_mobility ? "Mobility / Wheelchair Access" : "Standard Accommodations");
  setHtml("sum-access-subtext", p.accessibility_custom ? `Note: ${p.accessibility_custom}` : "Step-free entry, elevators, prioritized accessibility filters");

  setHtml("sum-style-headline", styles.join(", ") || "ADVENTURE, NATURE, CULTURE, FOOD, PHOTOGRAPHY");
  setHtml("sum-style-subtext", `${styles.length} style layers calibrated for POI selection`);

  setHtml("sum-food-headline", diets.join(", ") || "VEGETARIAN, HALAL");
  setHtml("sum-food-subtext", `Allergies: ${p.allergies_restrictions || 'None'}${p.food_custom ? ` • Custom: ${p.food_custom}` : ''}`);

  setHtml("sum-clothing-headline", `${pack || 'WESTERN, CASUAL'} wear`);
  setHtml("sum-clothing-subtext", p.modest_clothing ? `Modesty filters active${p.clothing_custom ? ` • ${p.clothing_custom}` : ''}` : (p.clothing_custom || "Standard checklist"));

  setHtml("sum-budget-headline", `${curr} ${customAmt}${usdNote}`);
  setHtml("sum-budget-subtext", `Currency: ${curr} • Standardized USD conversion calibrated for global itinerary flights & hotels`);
}

// ================= AUTH MODAL =================
function showAuthModal() {
  const modal = document.getElementById("auth-modal");
  if (modal) modal.style.display = "flex";
  const errEl = document.getElementById("auth-error-msg");
  if (errEl) errEl.style.display = "none";
  const succEl = document.getElementById("auth-success-msg");
  if (succEl) succEl.style.display = "none";
}

function hideAuthModal() {
  const modal = document.getElementById("auth-modal");
  if (modal) modal.style.display = "none";
}

function switchAuthTab(mode) {
  authMode = mode;
  const tabLogin = document.getElementById("tab-login");
  const tabReg = document.getElementById("tab-register");
  const groupName = document.getElementById("group-fullname");
  const submitBtn = document.getElementById("auth-submit-btn");
  const errEl = document.getElementById("auth-error-msg");
  const succEl = document.getElementById("auth-success-msg");

  if (errEl) errEl.style.display = "none";
  if (succEl) succEl.style.display = "none";

  if (mode === "register") {
    if (tabLogin) { tabLogin.style.background = "#F0F4F2"; tabLogin.style.color = "var(--text-muted)"; }
    if (tabReg) { tabReg.style.background = "var(--primary-light)"; tabReg.style.color = "var(--primary)"; }
    if (groupName) groupName.style.display = "block";
    if (submitBtn) submitBtn.innerText = "Create Account & Start";
  } else {
    if (tabLogin) { tabLogin.style.background = "var(--primary-light)"; tabLogin.style.color = "var(--primary)"; }
    if (tabReg) { tabReg.style.background = "#F0F4F2"; tabReg.style.color = "var(--text-muted)"; }
    if (groupName) groupName.style.display = "none";
    if (submitBtn) submitBtn.innerText = "Sign In";
  }
}

async function handleAuthSubmit(e) {
  if (e && e.preventDefault) e.preventDefault();
  const emailEl = document.getElementById("auth-email");
  const passwordEl = document.getElementById("auth-password");
  const nameEl = document.getElementById("auth-name");
  const errEl = document.getElementById("auth-error-msg");
  const succEl = document.getElementById("auth-success-msg");
  const submitBtn = document.getElementById("auth-submit-btn");

  const email = emailEl ? emailEl.value.trim() : "";
  const password = passwordEl ? passwordEl.value : "";
  const fullName = nameEl ? nameEl.value.trim() : "";

  if (!email || !password) {
    if (errEl) {
      errEl.innerText = "Please enter both your email address and password.";
      errEl.style.display = "block";
    }
    return;
  }

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerText = authMode === "register" ? "Creating Account..." : "Signing In...";
  }

  const endpoint = authMode === "register" ? "/api/v1/auth/register" : "/api/v1/auth/login";
  const body = authMode === "register" ? { email, password, full_name: fullName || undefined } : { email, password };

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();

    if (res.ok && data.access_token) {
      token = data.access_token;
      localStorage.setItem("travel_ai_token", token);
      
      const display = document.getElementById("user-display");
      if (display) {
        display.innerText = fullName || passport.full_name || email;
      }
      const authBtn = document.getElementById("auth-btn");
      if (authBtn) authBtn.style.display = "none";
      const signoutBtn = document.getElementById("signout-btn");
      if (signoutBtn) signoutBtn.style.display = "inline-block";

      if (succEl) {
        succEl.innerText = authMode === "register" ? "Account created successfully!" : "Signed in successfully!";
        succEl.style.display = "block";
      }
      setTimeout(async () => {
        hideAuthModal();
        await loadUserProfile();
      }, 500);
    } else {
      const errorMsg = data.detail || (typeof data === 'string' ? data : "Authentication failed. Please check your credentials.");
      if (errEl) {
        errEl.innerText = errorMsg;
        errEl.style.display = "block";
      } else {
        alert(errorMsg);
      }
    }
  } catch (err) {
    if (errEl) {
      errEl.innerText = "Connection error: " + err.message;
      errEl.style.display = "block";
    } else {
      alert("Connection error: " + err.message);
    }
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerText = authMode === "register" ? "Create Account & Start" : "Sign In";
    }
  }
}

async function loadUserProfile() {
  if (!token) {
    const display = document.getElementById("user-display");
    if (display) display.innerText = "Guest Traveler";
    const authBtn = document.getElementById("auth-btn");
    if (authBtn) authBtn.style.display = "inline-block";
    const signoutBtn = document.getElementById("signout-btn");
    if (signoutBtn) signoutBtn.style.display = "none";
    return;
  }

  try {
    const userRes = await fetch("/api/v1/auth/me", {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (userRes.ok) {
      user = await userRes.json();
      const display = document.getElementById("user-display");
      if (display) {
        display.innerText = user.full_name || passport.full_name || user.email || "Traveler";
      }
      const authBtn = document.getElementById("auth-btn");
      if (authBtn) authBtn.style.display = "none";
      const signoutBtn = document.getElementById("signout-btn");
      if (signoutBtn) signoutBtn.style.display = "inline-block";
    }

    const passRes = await fetch("/api/v1/passport", {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (passRes.ok) {
      const serverPass = await passRes.json();
      Object.assign(passport, serverPass);
      // Sync to inputs
      const fn = document.getElementById("inp-fullname"); if (fn && passport.full_name) fn.value = passport.full_name;
      const age = document.getElementById("inp-age"); if (age && passport.age) age.value = passport.age;
      const nat = document.getElementById("inp-nationality"); if (nat && passport.nationality) nat.value = passport.nationality;
      const city = document.getElementById("inp-homecity"); if (city && passport.home_city) city.value = passport.home_city;
      
      const display = document.getElementById("user-display");
      if (display && (passport.full_name || (user && user.full_name))) {
        display.innerText = passport.full_name || user.full_name;
      }
      
      renderSelectedLanguages();
      updateBudgetConversionBadge();
    }
  } catch (e) {
    console.warn("User load delayed", e);
  }
}

function logout() {
  localStorage.removeItem("travel_ai_token");
  token = null;
  user = null;
  location.reload();
}

// ================= TRIP GENERATOR MODAL =================
function showTripPlannerModal() {
  const modal = document.getElementById("trip-modal");
  const body = document.getElementById("trip-modal-body");
  const title = document.getElementById("trip-modal-title");
  if (!modal || !body) return;

  if (title) title.innerText = "Plan Your Custom AI Trip";
  modal.style.display = "flex";

  body.innerHTML = `
    <div style="max-width: 580px; margin: 0 auto;">
      <p style="color:var(--text-muted); font-size:14px; margin-bottom:20px;">
        Your Travel Passport preferences (dietary standards, modesty guidelines, budget standardized to USD, accessibility requirements, and all custom inputs) will be automatically injected into this itinerary generator.
      </p>

      <div class="form-group">
        <label>Dream Destination</label>
        <input type="text" id="trip-dest-input" value="Kyoto, Japan" placeholder="e.g. Kyoto, Japan | Rome, Italy | Bali, Indonesia | Goa, India">
      </div>

      <div class="form-grid-2" style="margin-bottom:0;">
        <div class="form-group">
          <label>Trip Duration (Days)</label>
          <select id="trip-duration-input">
            <option value="2">2 Days (Weekend Getaway)</option>
            <option value="3" selected>3 Days (Classic City Exploration)</option>
            <option value="5">5 Days (Full Cultural Journey)</option>
            <option value="7">7 Days (Deep Immersion)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Start Date</label>
          <input type="date" id="trip-date-input" value="2026-10-15">
        </div>
      </div>

      <div class="form-group">
        <label>Special Requests or Vibe (Optional)</label>
        <input type="text" id="trip-notes-input" placeholder="e.g. Peaceful morning walks, tea houses, scenic photography spots">
      </div>

      <div style="display:flex; justify-content:flex-end; gap:12px; margin-top:24px;">
        <button type="button" class="btn-back" onclick="hideTripModal()">Cancel</button>
        <button type="button" class="btn-continue" onclick="triggerAISynthesis()">
          ⚡ Synthesize AI Itinerary
        </button>
      </div>
    </div>
  `;
}

function hideTripModal() {
  const modal = document.getElementById("trip-modal");
  if (modal) modal.style.display = "none";
}

async function triggerAISynthesis() {
  const dest = document.getElementById("trip-dest-input")?.value || "Kyoto, Japan";
  const duration = parseInt(document.getElementById("trip-duration-input")?.value) || 3;
  const date = document.getElementById("trip-date-input")?.value || "2026-10-15";
  const notes = document.getElementById("trip-notes-input")?.value || "";

  const body = document.getElementById("trip-modal-body");
  const title = document.getElementById("trip-modal-title");
  if (title) title.innerText = `Synthesizing AI Itinerary for ${dest}...`;

  body.innerHTML = `
    <div style="text-align:center; padding:60px 20px;">
      <div style="width:48px; height:48px; border:4px solid var(--primary-light); border-top-color:var(--primary); border-radius:50%; animation: spin 1s infinite linear; margin:0 auto 20px auto;"></div>
      <h3 style="font-size:20px; font-weight:800; color:var(--text-main);">Synthesizing AI Itinerary for ${dest}...</h3>
      <p style="color:var(--text-muted); font-size:14px; margin-top:8px; max-width:480px; margin-left:auto; margin-right:auto;">
        Applying Travel Passport rules: Strict ${passport.dietary_standards?.join(', ') || 'dietary'} culinary filtering, ${passport.modest_clothing ? 'modest sacred site dress codes' : 'attire guidance'}, ${passport.accessibility_mobility ? 'wheelchair & elevator paths' : 'accessible paths'}, and ${passport.budget_tier || 'moderate'} budget allocation standardized in USD.
      </p>
    </div>
    <style>
      @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
  `;

  try {
    let trip = null;
    if (token) {
      const res = await fetch("/api/v1/trips/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          destination: dest,
          duration_days: duration,
          start_date: date,
          custom_notes: notes
        })
      });
      if (res.ok) trip = await res.json();
    }

    if (!trip) {
      trip = generateLocalTrip(dest, duration);
    }

    renderTripResult(trip);
  } catch (e) {
    body.innerHTML = `<div style="color:red; text-align:center; padding:40px;">Error generating trip: ${e.message}</div>`;
  }
}

function generateLocalTrip(destination, duration) {
  const p = passport;
  const days = [];
  for (let d = 1; d <= duration; d++) {
    days.push({
      day_number: d,
      theme: `Day ${d}: Heritage, Scenic Exploration & Culinary Tracks in ${destination}`,
      activities: [
        {
          time_slot: "Morning (09:00 - 12:30)",
          activity_name: "Historic Heritage Quarter Walking Tour",
          location: `${destination} Central Heritage District`,
          description: "Explore iconic preservation architecture, artisan silk & pottery workshops, and tranquil garden pathways.",
          dress_code_advice: p.modest_clothing ? "Cover shoulders & knees for temple entries." : "Comfortable walking attire.",
          accessibility_notes: p.accessibility_mobility ? "Wheelchair ramp entrances & elevator routes verified." : "Smooth paved pathways."
        },
        {
          time_slot: "Afternoon (14:00 - 17:30)",
          activity_name: "Scenic Panoramic Lookout & Nature Boardwalk",
          location: `${destination} Riverside Quarter`,
          description: "Breath-taking viewpoints and shaded forest paths beside ancient stone bridges.",
          dress_code_advice: "Breathable comfortable walking shoes.",
          accessibility_notes: "Rest benches available every 200m."
        },
        {
          time_slot: "Evening (18:30 - 21:30)",
          activity_name: "Evening Lantern Promenade & Artisan Tastings",
          location: `${destination} Lantern Walk`,
          description: "Atmospheric evening stroll beneath warm lanterns with curated seasonal culinary sampling.",
          dress_code_advice: "Smart casual with a light evening layer.",
          accessibility_notes: "Step-free boardwalk."
        }
      ],
      recommended_stay: {
        hotel_name: `${destination} Artisan Heritage Boutique Hotel`,
        vibe: "Charming localized decor, step-free access, central positioning, and organic breakfast."
      }
    });
  }

  const bTier = p.budget_tier || "moderate";
  const curr = p.budget_currency || "INR";
  const usdNote = p.budget_standardized_usd ? ` [${p.budget_standardized_usd}]` : "";

  return {
    destination: destination,
    duration_days: duration,
    budget_breakdown: {
      total_estimated_range: p.budget_custom ? `${curr} ${p.budget_custom}${usdNote}` : "₹4,000 – ₹8,500 / day ($48 – $102 USD)",
      accommodation_per_night: bTier === "budget" ? "₹800 – ₹1,800 / night (≈ $10 – $22 USD)" : (bTier === "premium_luxury" ? "₹8,000 – ₹20,000+ / night (≈ $95 – $240+ USD)" : "₹2,500 – ₹5,000 / night (≈ $30 – $60 USD)"),
      meals_daily_estimate: bTier === "budget" ? "₹400 – ₹800 / day (≈ $5 – $10 USD)" : (bTier === "premium_luxury" ? "₹2,500 – ₹6,000 / day (≈ $30 – $72 USD)" : "₹1,000 – ₹2,000 / day (≈ $12 – $24 USD)"),
      activities_daily_estimate: "₹500 – ₹1,500 / day (≈ $6 – $18 USD)",
      tier_label: (bTier || "moderate").toUpperCase()
    },
    itinerary: days,
    dining_recommendations: [
      {
        meal_type: "Breakfast / Morning Cafe",
        restaurant_name: `The Artisan Botanist Cafe (${destination})`,
        dietary_alignment: `Dedicated ${(p.dietary_standards || ['Vegetarian']).join(', ')} breakfast menu`,
        allergy_safety_note: `Strict allergen protocol: ${p.allergies_restrictions || 'None flagged'}`,
        estimated_cost_tier: "₹₹ ($15 – $25 USD)"
      },
      {
        meal_type: "Lunch / Midday Refuel",
        restaurant_name: `Heritage Green Kitchen`,
        dietary_alignment: `Organic ${(p.dietary_standards || ['Vegetarian']).join(', ')} courses`,
        allergy_safety_note: `Allergen-isolated kitchen preparation`,
        estimated_cost_tier: "₹₹ ($15 – $25 USD)"
      },
      {
        meal_type: "Dinner / Evening Experience",
        restaurant_name: `Lantern Garden Gastronomy`,
        dietary_alignment: `Curated chef tasting set`,
        allergy_safety_note: `Personalized chef consultation on arrival`,
        estimated_cost_tier: "₹₹₹ ($40 – $90 USD)"
      }
    ],
    packing_checklist: {
      modesty_specific_items: p.modest_clothing ? [
        "Lightweight shawl or scarf to cover shoulders at sacred sites",
        "Full-length trousers / maxi skirt covering knees",
        "Slip-on walking shoes for easy entry at temples"
      ] : ["Standard comfortable travel attire"],
      weather_adaptation_items: [
        "UV-blocking sunhat & sunglasses",
        "Breathable cotton & linen shirts",
        "Compact travel umbrella"
      ],
      special_accessibility_items: p.accessibility_mobility ? [
        "Wheelchair charger & portable ramp guide app",
        "Accessible transit pass card"
      ] : []
    }
  };
}

function renderTripResult(trip) {
  const title = document.getElementById("trip-modal-title");
  if (title) title.innerText = `${trip.destination} (${trip.duration_days} Days) — AI Itinerary`;

  const body = document.getElementById("trip-modal-body");
  body.innerHTML = `
    <div style="margin-bottom:20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <div>
        <h2 style="font-size:22px; font-weight:800; color:var(--primary);">${trip.destination}</h2>
        <p style="font-size:13px; color:var(--text-muted); margin-top:2px;">
          Duration: <strong>${trip.duration_days} Days</strong> • Budget Allocation: <strong>${trip.budget_breakdown?.total_estimated_range || '₹4,000 – ₹8,500/day'}</strong> (${trip.budget_breakdown?.tier_label || 'MODERATE'})
        </p>
      </div>
      <button class="btn-sm" onclick="showTripPlannerModal()">+ Plan Another Destination</button>
    </div>

    <div class="trip-section-title">&#128506; Day-by-Day Personalized Itinerary</div>
    ${trip.itinerary.map(day => `
      <div class="trip-day">
        <div class="trip-day-header">${day.theme}</div>
        ${day.activities.map(act => `
          <div class="trip-act">
            <div class="trip-act-time">${act.time_slot} • ${act.location}</div>
            <div class="trip-act-title">${act.activity_name}</div>
            <div class="trip-act-desc">${act.description}</div>
            <div style="font-size:11px; color:#0D6D63; margin-top:4px; font-weight:600;">
              &#128087; ${act.dress_code_advice} | &#9855; ${act.accessibility_notes}
            </div>
          </div>
        `).join('')}
        <div style="margin-top:12px; font-size:12px; background:#E0F5F0; padding:10px 14px; border-radius:8px; color:#0D6D63;">
          <strong>Recommended Stay:</strong> ${day.recommended_stay?.hotel_name || 'Boutique Heritage Hotel'} — ${day.recommended_stay?.vibe || 'Accessible, central location with premium amenities.'}
        </div>
      </div>
    `).join('')}

    <div class="trip-section-title">&#127860; Vetted Dining Recommendations (Strictly Filtered)</div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)); gap:12px; margin-bottom:20px;">
      ${trip.dining_recommendations.map(d => `
        <div style="border:1.5px solid var(--border-color); border-radius:10px; padding:14px; background:white;">
          <span style="font-size:11px; font-weight:800; color:var(--primary); text-transform:uppercase;">${d.meal_type}</span>
          <h4 style="font-size:14px; margin:4px 0;">${d.restaurant_name} (${d.estimated_cost_tier || '₹₹'})</h4>
          <p style="font-size:12px; color:var(--text-muted);">${d.dietary_alignment}</p>
          <p style="font-size:11px; color:#0D6D63; margin-top:6px; font-weight:700;">&#10003; ${d.allergy_safety_note}</p>
        </div>
      `).join('')}
    </div>

    <div class="trip-section-title">&#129539; Custom Packing Checklist</div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
      <div style="background:#F9FBFB; border:1px solid var(--border-color); padding:16px; border-radius:10px;">
        <h4 style="font-size:13px; font-weight:700; margin-bottom:8px; color:var(--primary);">Modesty & Sacred Sites Outfits:</h4>
        <ul style="font-size:12px; padding-left:20px; line-height:1.7;">
          ${(trip.packing_checklist?.modesty_specific_items || []).map(i => `<li>${i}</li>`).join('')}
        </ul>
      </div>
      <div style="background:#F9FBFB; border:1px solid var(--border-color); padding:16px; border-radius:10px;">
        <h4 style="font-size:13px; font-weight:700; margin-bottom:8px; color:var(--primary);">Weather & Accessibility Gear:</h4>
        <ul style="font-size:12px; padding-left:20px; line-height:1.7;">
          ${(trip.packing_checklist?.weather_adaptation_items || []).map(i => `<li>${i}</li>`).join('')}
          ${(trip.packing_checklist?.special_accessibility_items || []).map(i => `<li>${i}</li>`).join('')}
        </ul>
      </div>
    </div>
  `;
}

// Close language dropdown on outside click
document.addEventListener("click", (e) => {
  const wrapper = document.querySelector(".lang-search-wrapper");
  const dropdown = document.getElementById("lang-suggestions");
  if (wrapper && dropdown && !wrapper.contains(e.target)) {
    dropdown.style.display = "none";
  }
});

// Auto-prompt login modal on first visit if not authenticated
function checkInitialAuthPrompt() {
  goToStep(1);
  if (!token) {
    showAuthModal();
  } else {
    loadUserProfile();
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", checkInitialAuthPrompt);
} else {
  checkInitialAuthPrompt();
}

// App object for global compatibility
window.addCustomSplitupRow = addCustomSplitupRow;
window.removeSplitupRow = removeSplitupRow;
window.toggleRoundOff = toggleRoundOff;
window.calculateSplitupTotal = calculateSplitupTotal;
window.logout = logout;

window.app = {
  goToStep, nextStep, prevStep, showAuthModal, hideAuthModal, switchAuthTab,
  handleAuthSubmit, handleAvatarUpload, handleLanguageSearch, handleLanguageKeydown,
  addCustomLanguageFromInput, addLanguage, removeLanguage, toggleLanguage,
  selectTravelerType, toggleAccessibility, toggleStyleCard, toggleDiet,
  togglePackStyle, toggleModesty, toggleHotWeather,
  handleCurrencyChange, handleBudgetCustom, addCustomSplitupRow, removeSplitupRow,
  toggleRoundOff, calculateSplitupTotal, logout, showTripPlannerModal, hideTripModal,
  triggerAISynthesis, passport
};
