/* ============================================================
   HYDROSCAN RECOMMENDATIONS JS
   ============================================================ */

function loadRecommendations() {
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

            // Header info
            document.getElementById("prediction-display").textContent = data.prediction;
            document.getElementById("confidence-display").textContent =
                (data.confidence ? data.confidence.toFixed(1) + "%" : "N/A");
            document.getElementById("score-display").textContent =
                data.score.category + " (" + data.score.score + ")";

            // Explanation
            document.getElementById("explanation-summary").textContent = data.explanation.summary;
            const exPoints = document.getElementById("explanation-points");
            exPoints.innerHTML = "";
            data.explanation.points.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `<i class="bi bi-${data.explanation.verdict === "Safe" ? "check-circle text-success" : "x-circle text-danger"} me-1"></i>${p}`;
                exPoints.appendChild(li);
            });

            // Alerts
            const alertsList = document.getElementById("alerts-list");
            if (data.alerts && data.alerts.length) {
                alertsList.innerHTML = data.alerts.map(a =>
                    `<div class="alert alert-danger py-2 mb-2">
                        <i class="bi bi-exclamation-triangle me-1"></i>${a.message}
                    </div>`).join("");
            } else {
                alertsList.innerHTML = '<div class="text-success"><i class="bi bi-check-circle me-1"></i>No alerts. Water parameters are within safe limits.</div>';
            }

            // Purification
            const purList = document.getElementById("purification-list");
            purList.innerHTML = "";
            data.purification.forEach(rec => {
                purList.innerHTML += `<div class="rec-item">
                    <span class="rec-icon">${rec.icon}</span>
                    <div><strong>${rec.title}</strong><div class="small text-muted">${rec.detail}</div></div>
                </div>`;
            });

            // Usage
            const usageList = document.getElementById("usage-list");
            usageList.innerHTML = "";
            data.usage.forEach(u => {
                const cl = u.allowed ? "usage-allowed" : "usage-not-allowed";
                const ic = u.allowed ? "bi-check-circle-fill" : "bi-x-circle-fill";
                usageList.innerHTML += `<div class="usage-item">
                    <span><span class="me-2">${u.icon}</span>${u.name}</span>
                    <span class="${cl}"><i class="bi ${ic} me-1"></i>${u.allowed ? "Allowed" : "Not Allowed"}</span>
                </div>`;
                if (!u.allowed && u.reason && u.reason !== "within limits") {
                    usageList.innerHTML += `<div class="small text-muted ps-4 pb-1">${u.reason}</div>`;
                }
            });

            showToast("Recommendations loaded", "success");
        })
        .catch(err => {
            showLoading(false);
            showToast("Connection Error: " + err.message, "danger");
        });
}

document.addEventListener("DOMContentLoaded", function () {
    loadRecommendations();
});

function pageRefresh() { loadRecommendations(); }
