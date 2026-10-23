/* ============================================================
   HYDROSCAN HISTORY JS
   ============================================================ */

let charts = {};

function loadHistory() {
    const count = document.getElementById("historyCount").value;
    showLoading(true);

    fetch("/api/history?results=" + count)
        .then(res => {
            if (!res.ok) throw new Error("HTTP " + res.status);
            return res.json();
        })
        .then(data => {
            showLoading(false);
            if (!data.success) {
                showToast(data.error || "Failed to load history", "danger");
                return;
            }

            const hist = data.history;
            if (!hist.length) {
                showToast("No history data available", "warning");
                return;
            }

            const labels = hist.map(h => formatTimestamp(h.timestamp).split(",")[0]);

            // Trends
            setTrend("trend-ph", hist.map(h => h.ph));
            setTrend("trend-tds", hist.map(h => h.tds));
            setTrend("trend-turbidity", hist.map(h => h.turbidity));
            setTrend("trend-temperature", hist.map(h => h.temperature));

            // Charts
            renderChart("chart-ph", "pH", labels, hist.map(h => h.ph), "#0d6efd");
            renderChart("chart-tds", "TDS (Mg/L)", labels, hist.map(h => h.tds), "#198754");
            renderChart("chart-turbidity", "Turbidity (NTU)", labels, hist.map(h => h.turbidity), "#fd7e14");
            renderChart("chart-temperature", "Temperature (°C)", labels, hist.map(h => h.temperature), "#dc3545");

            // Table
            const tbody = document.querySelector("#historyTable tbody");
            tbody.innerHTML = "";
            hist.slice().reverse().forEach(h => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${formatTimestamp(h.timestamp)}</td>
                    <td>${h.ph}</td>
                    <td>${h.turbidity}</td>
                    <td>${h.tds}</td>
                    <td>${h.temperature}</td>`;
                tbody.appendChild(tr);
            });

            showToast("History loaded (" + hist.length + " readings)", "success");
        })
        .catch(err => {
            showLoading(false);
            showToast("Connection Error: " + err.message, "danger");
        });
}

function setTrend(id, values) {
    const el = document.getElementById(id);
    if (!el) return;
    let trend = "stable";
    if (values.length >= 2) {
        const half = Math.floor(values.length / 2);
        const first = values.slice(0, half).reduce((a, b) => a + b, 0) / half;
        const second = values.slice(half).reduce((a, b) => a + b, 0) / (values.length - half);
        if (second > first * 1.02) trend = "increasing";
        else if (second < first * 0.98) trend = "decreasing";
    }
    const icons = { increasing: "↗", decreasing: "↘", stable: "→" };
    const colors = { increasing: "text-danger", decreasing: "text-success", stable: "text-muted" };
    el.innerHTML = `<span class="${colors[trend]}">${icons[trend]} ${trend}</span>`;
}

function renderChart(id, label, labels, data, color) {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    if (charts[id]) charts[id].destroy();
    charts[id] = new Chart(canvas, {
        type: "line",
        data: {
            labels,
            datasets: [{
                label,
                data,
                borderColor: color,
                backgroundColor: color + "22",
                fill: true,
                tension: 0.3,
                pointRadius: 1
            }]
        },
options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: chartTheme().grid }, ticks: { color: chartTheme().tick } },
                x: { ticks: { maxTicksLimit: 8, color: chartTheme().tick } }
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    loadHistory();
    // Repaint charts when theme changes
    document.addEventListener("themechange", loadHistory);
});

function pageRefresh() { loadHistory(); }
