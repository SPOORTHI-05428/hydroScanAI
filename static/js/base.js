/* ============================================================
   HYDROSCAN BASE JS - shared across all pages
   ============================================================ */

// Theme management
const THEME_KEY = "hydroscan-theme";

function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "light" ? "dark" : "light";
    applyTheme(next);
    // Notify pages so Chart.js charts can repaint with theme-aware colors
    document.dispatchEvent(new CustomEvent("themechange", { detail: next }));
}

// Return theme-aware colors for Chart.js
function chartTheme() {
    const dark = document.documentElement.getAttribute("data-theme") === "dark";
    return {
        dark,
        grid: dark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.08)",
        tick: dark ? "#8a9bb5" : "#6c757d",
        text: dark ? "#e6edf7" : "#1a2a3a"
    };
}

// Sidebar toggle (mobile)
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebarOverlay");
    if (sidebar) {
        sidebar.classList.toggle("open");
        overlay.classList.toggle("show");
    }
}

// Show toast
function showToast(message, type = "success") {
    const container = document.getElementById("toastContainer");
    if (!container) return;
    const icons = {
        success: "bi-check-circle-fill",
        danger: "bi-x-circle-fill",
        warning: "bi-exclamation-triangle-fill",
        info: "bi-info-circle-fill"
    };
    const colors = {
        success: "text-success",
        danger: "text-danger",
        warning: "text-warning",
        info: "text-primary"
    };
    const toast = document.createElement("div");
    toast.className = "custom-toast";
    toast.innerHTML = `
        <i class="bi ${icons[type] || icons.info} ${colors[type] || colors.info}"></i>
        <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => toast.classList.add("show"), 10);
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// Show/hide loading
function showLoading(show) {
    const overlay = document.getElementById("loadingOverlay");
    if (overlay) overlay.classList.toggle("d-none", !show);
}

// Global refresh (override in pages)
function refreshAll() {
    showToast("Refreshing...", "info");
    if (typeof pageRefresh === "function") pageRefresh();
}

// Format timestamp
function formatTimestamp(ts) {
    if (!ts) return "--";
    const d = new Date(ts);
    return d.toLocaleString();
}

// Draw a semi-circular gauge
function drawGauge(canvas, score) {
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const cx = canvas.width / 2;
    const cy = canvas.height - 10;
    const r = Math.min(canvas.width, canvas.height) - 20;
    const start = Math.PI;
    const end = 2 * Math.PI;
    const pct = Math.max(0, Math.min(100, score)) / 100;

    // Background arc
    ctx.beginPath();
    ctx.arc(cx, cy, r, start, end);
    ctx.strokeStyle = getComputedStyle(document.documentElement)
        .getPropertyValue("--card-border").trim() || "#e0e6ed";
    ctx.lineWidth = 14;
    ctx.lineCap = "round";
    ctx.stroke();

    let color = "#dc3545";
    if (score >= 90) color = "#198754";
    else if (score >= 70) color = "#ffc107";
    else if (score >= 50) color = "#fd7e14";

    if (pct > 0) {
        ctx.beginPath();
        ctx.arc(cx, cy, r, start, start + (end - start) * pct);
        ctx.strokeStyle = color;
        ctx.lineWidth = 14;
        ctx.lineCap = "round";
        ctx.stroke();
    }

    ctx.fillStyle = color;
    ctx.font = "bold " + Math.round(r * 0.35) + "px Inter";
    ctx.textAlign = "center";
    ctx.fillText(Math.round(score), cx, cy);

    ctx.fillStyle = "#888";
    ctx.font = "12px Inter";
    ctx.fillText("/ 100", cx, cy + 18);
}

// ============================================================
// INIT
// ============================================================

document.addEventListener("DOMContentLoaded", function () {
    // Restore theme
    const saved = localStorage.getItem(THEME_KEY) || "light";
    applyTheme(saved);

    // Theme toggle button
    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) themeToggle.addEventListener("click", toggleTheme);

    // Sidebar toggle
    const sbToggle = document.getElementById("sidebarToggle");
    const overlay = document.getElementById("sidebarOverlay");
    if (sbToggle) sbToggle.addEventListener("click", toggleSidebar);
    if (overlay) overlay.addEventListener("click", toggleSidebar);
});
