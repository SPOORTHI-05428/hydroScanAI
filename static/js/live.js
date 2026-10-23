/* ============================================================
   HYDROSCAN LIVE MONITOR JS
   ============================================================ */

function refreshLive() {
    showLoading(true);
    fetch("/predict")
        .then(res => {
            if (!res.ok) throw new Error("HTTP " + res.status);
            return res.json();
        })
        .then(data => {
            showLoading(false);
            if (!data.success) {
                showToast(data.error || "Failed to load", "danger");
                return;
            }

            const s = data.sensor;

            // Top row big values
            document.getElementById("sensor-ph").textContent = s.pH;
            document.getElementById("sensor-turbidity").textContent = s.Turbidity_NTU;
            document.getElementById("sensor-tds").textContent = s.TDS_mg_L;
            document.getElementById("sensor-temperature").textContent = s.Temperature_C;

            // Big detail cards
            document.getElementById("sensor-ph-big").textContent = s.pH;
            document.getElementById("sensor-turbidity-big").textContent = s.Turbidity_NTU + " NTU";
            document.getElementById("sensor-tds-big").textContent = s.TDS_mg_L + " Mg/L";
            document.getElementById("sensor-temperature-big").textContent = s.Temperature_C + " °C";

            // Progress bars & status
            const phPct = Math.min(100, (s.pH / 14) * 100);
            document.getElementById("ph-progress").style.width = phPct + "%";
            document.getElementById("ph-progress").className = "progress-bar " + (s.pH >= 6.5 && s.pH <= 8.5 ? "bg-success" : "bg-danger");
            setStatus("sensor-ph-status", s.pH >= 6.5 && s.pH <= 8.5, "pH " + s.pH);

            const turPct = Math.min(100, (s.Turbidity_NTU / 10) * 100);
            document.getElementById("turbidity-progress").style.width = turPct + "%";
            document.getElementById("turbidity-progress").className = "progress-bar " + (s.Turbidity_NTU <= 5 ? "bg-success" : "bg-danger");
            setStatus("sensor-turbidity-status", s.Turbidity_NTU <= 5, s.Turbidity_NTU + " NTU");

            const tdsPct = Math.min(100, (s.TDS_mg_L / 1000) * 100);
            document.getElementById("tds-progress").style.width = tdsPct + "%";
            document.getElementById("tds-progress").className = "progress-bar " + (s.TDS_mg_L <= 500 ? "bg-success" : "bg-danger");
            setStatus("sensor-tds-status", s.TDS_mg_L <= 500, s.TDS_mg_L + " Mg/L");

            const tempPct = Math.min(100, (s.Temperature_C / 40) * 100);
            document.getElementById("temperature-progress").style.width = tempPct + "%";
            document.getElementById("temperature-progress").className = "progress-bar " + (s.Temperature_C >= 10 && s.Temperature_C <= 30 ? "bg-success" : "bg-danger");
            setStatus("sensor-temperature-status", s.Temperature_C >= 10 && s.Temperature_C <= 30, s.Temperature_C + " °C");

            // Score gauge
            drawGauge(document.getElementById("scoreGauge"), data.score.score);
            const cat = document.getElementById("score-category");
            cat.textContent = data.score.category + " (" + data.score.score + ")";
            cat.className = "score-category fw-bold mt-2 " + data.score.color;

            // Last update
            document.getElementById("last-update").textContent = formatTimestamp(s.timestamp);

            // Alerts
            showAlerts(data.alerts);

            showToast("Live data updated", "success");
        })
        .catch(err => {
            showLoading(false);
            showToast("Connection Error: " + err.message, "danger");
        });
}

function setStatus(id, ok, text) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = text;
        el.className = "status-badge " + (ok ? "ok" : "bad");
    }
}

function showAlerts(alerts) {
    const banner = document.getElementById("alertBanner");
    const msg = document.getElementById("alertMessages");
    if (!alerts || alerts.length === 0) {
        banner.classList.add("d-none");
        return;
    }
    banner.classList.remove("d-none");
    msg.innerHTML = alerts.map(a =>
        `<div><i class="bi bi-bell me-1"></i>${a.message}</div>`).join("");
}

document.addEventListener("DOMContentLoaded", function () {
    refreshLive();
    // Auto refresh every 30s
    setInterval(refreshLive, 30000);
});

function pageRefresh() { refreshLive(); }
