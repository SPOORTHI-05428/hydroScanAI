/* ============================================================
   HYDROSCAN REPORTS JS
   ============================================================ */

function downloadReport() {
    const status = document.getElementById("report-status");
    status.textContent = "Generating report...";
    status.className = "mt-3 small text-primary";

    fetch("/api/report?download=1")
        .then(res => {
            if (!res.ok) throw new Error("HTTP " + res.status);
            return res.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "hydroscan_report.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            status.textContent = "Report downloaded successfully!";
            status.className = "mt-3 small text-success";
            showToast("PDF report downloaded", "success");
        })
        .catch(err => {
            status.textContent = "Failed to generate report.";
            status.className = "mt-3 small text-danger";
            showToast("Error: " + err.message, "danger");
        });
}

function pageRefresh() {
    // Nothing to auto-refresh on reports page
}
