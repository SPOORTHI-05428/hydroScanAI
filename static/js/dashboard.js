/* ============================================================
   HYDROSCAN DASHBOARD JS
   ============================================================ */

let scoreGaugeChart = null;
let miniChart = null;

// Helper to set sensor status
function setSensorStatus(id, elId, value, ok) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = value;
        el.className = "status-badge " + (ok ? "ok" : "bad");
    }
}

function refreshDashboard() {
    showLoading(true);
    fetch("/predict")
        .then(res => {
            if (!res.ok) throw new Error("HTTP " + res.status);
            return res.json();
        })
        .then(data => {
            showLoading(false);
            if (!data.success) {
                showToast(data.error || "Analysis failed", "danger");
                return;
            }

            // Sensor values
            const s = data.sensor;
            document.getElementById("sensor-ph").textContent = s.pH;
            document.getElementById("sensor-turbidity").textContent = s.Turbidity_NTU + " NTU";
            document.getElementById("sensor-tds").textContent = s.TDS_mg_L + " Mg/L";
            document.getElementById("sensor-temperature").textContent = s.Temperature_C + " °C";

            // Prediction
            const predEl = document.getElementById("prediction");
            predEl.textContent = data.prediction;
            predEl.className = "prediction";
            if (String(data.prediction).toLowerCase().includes("unsafe")) {
                predEl.classList.add("prediction-unsafe");
            } else if (String(data.prediction).toLowerCase().includes("drink")) {
                predEl.classList.add("prediction-drink");
            } else {
                predEl.classList.add("prediction-safe");
            }

            document.getElementById("confidence-badge").textContent =
                "Confidence: " + (data.confidence ? data.confidence.toFixed(1) + "%" : "N/A");

            // Probabilities
            const probInfo = document.getElementById("probabilities-info");
            if (data.probabilities) {
                probInfo.innerHTML = "<strong>Class Probabilities:</strong>";
                Object.entries(data.probabilities).forEach(([label, p]) => {
                    probInfo.innerHTML += `<div class="d-flex justify-content-between">
                        <span>${label}</span><span>${p.toFixed(1)}%</span></div>`;
                });
            }

            // Score gauge
            drawGauge(document.getElementById("scoreGauge"), data.score.score);
            const cat = document.getElementById("score-category");
            cat.textContent = data.score.category + " (" + data.score.score + ")";
            cat.className = "score-category fw-bold mt-1 " + data.score.color;

            // Quick stats: fetch statistics
            loadQuickStats();

            // Explanation summary
            document.getElementById("explanation-summary").textContent = data.explanation.summary;
            const pts = document.getElementById("explanation-points");
            pts.innerHTML = "";
            data.explanation.points.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `<i class="bi bi-${data.explanation.verdict === "Safe" ? "check-circle text-success" : "x-circle text-danger"} me-1"></i>${p}`;
                pts.appendChild(li);
            });

            // Purification preview
            const pur = document.getElementById("purification-preview");
            pur.innerHTML = "";
            data.purification.slice(0, 3).forEach(rec => {
                pur.innerHTML += `<div class="rec-item">
                    <span class="rec-icon">${rec.icon}</span>
                    <div><strong>${rec.title}</strong><div class="small text-muted">${rec.detail}</div></div>
                </div>`;
            });

            // Last update
            document.getElementById("last-update").textContent = formatTimestamp(s.timestamp);

            // Alerts banner
            showAlerts(data.alerts);

            // Mini chart
            loadMiniChart();

            showToast("Analysis complete", "success");
        })
        .catch(err => {
            showLoading(false);
            showToast("Connection Error: " + err.message, "danger");
        });
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

    // Browser notification
    if ("Notification" in window && Notification.permission === "granted") {
        new Notification("HydroScan Alert", { body: alerts[0].message });
    }
}

function loadQuickStats() {
    fetch("/api/statistics?results=20")
        .then(r => r.json())
        .then(d => {
            if (!d.success) return;
            const st = d.statistics;
            document.getElementById("avg-ph").textContent = st.avg_ph;
            document.getElementById("avg-tds").textContent = st.avg_tds;
            document.getElementById("safe-count").textContent = st.safe_readings;
            document.getElementById("unsafe-count").textContent = st.unsafe_readings;
        })
        .catch(() => {});
}

function loadMiniChart() {
    fetch("/api/history?results=20")
        .then(r => r.json())
        .then(d => {
            if (!d.success || !d.history.length) return;
            const labels = d.history.map(h => formatTimestamp(h.timestamp).split(",")[0]);
            const ph = d.history.map(h => h.ph);

            if (miniChart) miniChart.destroy();
            miniChart = new Chart(document.getElementById("chart-ph-mini"), {
                type: "line",
                data: {
                    labels,
                    datasets: [{
                        label: "pH",
                        data: ph,
                        borderColor: "#0d6efd",
                        backgroundColor: "rgba(13,110,253,0.1)",
                        fill: true,
                        tension: 0.3,
                        pointRadius: 2
                    }]
                },
options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { display: false }, ticks: { color: chartTheme().tick } },
                        x: { ticks: { color: chartTheme().tick } }
                    }
                }
            });
        })
        .catch(() => {});
}

// Init
document.addEventListener("DOMContentLoaded", function () {
    // Request notification permission
    if ("Notification" in window && Notification.permission === "default") {
        Notification.requestPermission();
    }
    refreshDashboard();
    // Repaint mini chart when theme changes
    document.addEventListener("themechange", loadMiniChart);
});

// Expose page refresh
function pageRefresh() { refreshDashboard(); }
