/**
 * common.js - Shared utilities, API client, toast notifications, and UI helpers
 * Strictly follows UI_UX.md and API_SPEC.md
 */

// 1. Toast Notification System
function showToast(message, type = 'danger') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.setAttribute('role', 'alert');

  const icon = type === 'success' ? '✓' : '✕';
  toast.innerHTML = `
    <span style="font-weight:bold; color:var(--${type === 'success' ? 'success' : 'danger'}); font-size:1.1rem;">${icon}</span>
    <div style="flex:1;">${message}</div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4500);
}

// 2. Standardized JSON Fetch Helper
async function fetchJSON(url, options = {}) {
  const defaultHeaders = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const errorMsg = (data && data.error) ? data.error : `Request failed with status ${response.status}`;
      showToast(errorMsg, 'danger');
      throw new Error(errorMsg);
    }

    return data;
  } catch (err) {
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      const netError = 'Network connection error. Is the server running?';
      showToast(netError, 'danger');
      throw new Error(netError);
    }
    throw err;
  }
}

// 3. Formatting Utilities
function formatNumber(num) {
  if (num === null || num === undefined || isNaN(num)) return '—';
  return Number(num).toLocaleString();
}

function formatDuration(ms) {
  if (ms === null || ms === undefined || isNaN(ms)) return '—';
  return `${Number(ms).toFixed(1)} ms`;
}

function formatTimestamp(isoStr) {
  if (!isoStr) return '—';
  try {
    const d = new Date(isoStr);
    return d.toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  } catch (e) {
    return isoStr;
  }
}

// 4. Loading State Helper for Buttons and Progress Lines
function setButtonLoading(button, progressLine, isLoading, loadingText = 'Running threads…') {
  if (!button) return;
  if (isLoading) {
    button.dataset.originalText = button.innerHTML;
    button.innerHTML = loadingText;
    button.disabled = true;
    if (progressLine) progressLine.classList.add('active');
  } else {
    if (button.dataset.originalText) {
      button.innerHTML = button.dataset.originalText;
    }
    button.disabled = false;
    if (progressLine) progressLine.classList.remove('active');
  }
}

// 5. Active Nav Link Highlighter
document.addEventListener('DOMContentLoaded', () => {
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  const navLinks = document.querySelectorAll('.nav-links a');
  navLinks.forEach(link => {
    const href = link.getAttribute('href').replace(/\/$/, '') || '/';
    if (href === currentPath) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
});
