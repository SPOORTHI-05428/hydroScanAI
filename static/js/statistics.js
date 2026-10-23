/* ============================================================
   HYDROSCAN STATISTICS JS
   ============================================================ */

let pieChart = null;
let importanceChart = null;

function loadStats() {
    showLoading(true);
    fetch("/api/statistics?results=100")
        .then(res => {
            if (!res.ok) throw new Error("HTTP " + res.status);
            return res.json();
        })
        .then(data => {
            showLoading(false);
            if (!data.success) {
                showToast(data.error || "Failed to load statistics", "danger");
                return;
            }

            const st = data.statistics;
            const model = data.model;

            // Model accuracy (if provided by model info)
            // We don't have stored accuracy; show model type
            document.getElementById("stat-accuracy").textContent = model.model_type || "--";

            // Counters
            document.getElementById("stat-readings").textContent = st.total_readings;
            document.getElementById("stat-safe").textContent = st.safe_readings;
            document.getElementById("stat-unsafe").textContent = st.unsafe_readings;

            // Averages
            document.getElementById("stat-avg-ph").textContent = st.avg_ph;
            document.getElementById("stat-avg-tds").textContent = st.avg_tds;
            document.getElementById("stat-avg-turbidity").textContent = st.avg_turbidity;
            document.getElementById("stat-avg-temp").textContent = st.avg_temperature;

            // Pie chart (safe vs unsafe). safe_readings is 0 by design;
            // we show total as "monitored" instead. Use total vs 0.
            if (pieChart) pieChart.destroy();
pieChart = new Chart(document.getElementById("chart-pie"), {
                type: "doughnut",
                data: {
                    labels: ["Total Readings"],
                    datasets: [{
                        data: [st.total_readings],
                        backgroundColor: ["#0d6efd"]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { labels: { color: chartTheme().text }, position: "bottom" } }
                }
            });

            // Feature importance
            if (importanceChart) importanceChart.destroy();
            const features = data.feature_importance.map(f => f.feature);
            const importances = data.feature_importance.map(f => f.importance);
            importanceChart = new Chart(document.getElementById("chart-importance"), {
                type: "bar",
                data: {
                    labels: features,
                    datasets: [{
                        label: "Importance (%)",
                        data: importances,
                        backgroundColor: ["#0d6efd", "#198754", "#fd7e14", "#dc3545"]
                    }]
                },
options: {
                    responsive: true,
                    indexAxis: "y",
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { beginAtZero: true, grid: { color: chartTheme().grid }, ticks: { color: chartTheme().tick } },
                        y: { ticks: { color: chartTheme().tick } }
                    }
                }
            });

            // Class probabilities list (from model labels)
            const probList = document.getElementById("probabilities-list");
            probList.innerHTML = "";
            if (model.labels && model.labels.length) {
                model.labels.forEach(label => {
                    probList.innerHTML += `<div class="usage-item">
                        <span>${label}</span>
                        <span class="text-primary fw-bold">Class</span>
                    </div>`;
                });
            } else {
                probList.innerHTML = '<div class="text-muted small">No class info available.</div>';
            }

            // Confusion matrix - not available from loaded model directly.
            // Display a note.
            const ct = document.getElementById("confusion-table");
            ct.innerHTML = '<tr><td class="text-center text-muted py-3">Confusion matrix is available after training (see train.py). Retrain to populate.</td></tr>';

            showToast("Statistics loaded", "success");
        })
        .catch(err => {
            showLoading(false);
            showToast("Connection Error: " + err.message, "danger");
        });
}

document.addEventListener("DOMContentLoaded", function () {
    loadStats();
    // Repaint charts when theme changes
    document.addEventListener("themechange", loadStats);
});

function pageRefresh() {
    loadStats();
    // Also reload predictions for probabilities
    fetch("/predict").then(r => r.json()).then(d => {
        if (d.success && d.probabilities) {
            const probList = document.getElementById("probabilities-list");
            probList.innerHTML = "";
            Object.entries(d.probabilities).forEach(([label, p]) => {
                probList.innerHTML += `<div class="usage-item">
                    <span>${label}</span>
                    <span class="text-primary fw-bold">${p.toFixed(1)}%</span>
                </div>`;
            });
        }
    }).catch(() => {});
}
