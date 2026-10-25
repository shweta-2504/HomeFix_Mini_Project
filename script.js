const appliance = document.getElementById("appliance");
const symptom = document.getElementById("symptom");
const checkBtn = document.getElementById("checkBtn");
const results = document.getElementById("results");
const historyList = document.getElementById("historyList");

document.querySelectorAll("[data-symptom]").forEach(btn => {
  btn.addEventListener("click", () => {
    symptom.value = btn.dataset.symptom;
    symptom.focus();
  });
});

async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}

function safeText(value) {
  const el = document.createElement("span");
  el.textContent = value ?? "";
  return el.innerHTML;
}

checkBtn.addEventListener("click", async () => {
  if (!appliance.value || !symptom.value.trim()) {
    results.innerHTML = '<div class="result-card"><p class="muted">Please select an appliance and describe its problem.</p></div>';
    return;
  }
  checkBtn.disabled = true;
  checkBtn.textContent = "Checking possible causes…";
  results.innerHTML = '<div class="result-card"><p class="muted">HomeFix is checking its troubleshooting rules.</p></div>';
  try {
    const data = await api("/api/troubleshoot", {
      method: "POST",
      body: JSON.stringify({ appliance: appliance.value, symptom: symptom.value.trim() })
    });
    let html = '<div class="result-card"><h3>🔎 Troubleshooting results</h3>';
    data.results.forEach((r, index) => {
      html += `<div class="result-item"><h4>${index + 1}. Possible cause</h4>
        <p>${safeText(r.possible_cause)}</p><h4>Suggested steps</h4>
        <p>${safeText(r.solution)}</p>
        <div class="warning"><strong>Safety warning:</strong> ${safeText(r.safety_warning)}</div></div>`;
    });
    html += '</div>';
    results.innerHTML = html;
    await loadHistory();
  } catch (err) {
    results.innerHTML = `<div class="result-card"><p class="warning">${safeText(err.message)}</p><p class="muted">Make sure MySQL is running and database.sql has been imported.</p></div>`;
  } finally {
    checkBtn.disabled = false;
    checkBtn.innerHTML = 'Find possible solutions <span>→</span>';
  }
});

async function loadHistory() {
  try {
    const rows = await api("/api/history");
    if (!rows.length) {
      historyList.innerHTML = '<p class="muted">No repair checks yet. Try checking an appliance above.</p>';
      return;
    }
    historyList.innerHTML = rows.map(row => `<div class="history-row">
      <div><strong>${safeText(row.appliance)} — ${safeText(row.symptom)}</strong>
      <small>${safeText(row.result_summary)}</small></div><time>${safeText(row.created_at)}</time>
    </div>`).join("");
  } catch (err) {
    historyList.innerHTML = `<p class="muted">${safeText(err.message)}</p>`;
  }
}

document.getElementById("refreshHistory").addEventListener("click", loadHistory);
document.getElementById("techBtn").addEventListener("click", async () => {
  try {
    const data = await api("/api/technician", {
      method: "POST",
      body: JSON.stringify({ appliance: appliance.value || "Home appliance" })
    });
    results.innerHTML = `<div class="result-card"><h3>🧰 Technician safety checklist</h3>
      <p>${safeText(data.message)}</p><ul>${data.checklist.map(item => `<li>${safeText(item)}</li>`).join("")}</ul></div>`;
    document.getElementById("checker").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    alert(err.message);
  }
});

loadHistory();
