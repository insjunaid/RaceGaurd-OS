/**
 * comparison.js - Comparative benchmark, Chart.js visualization, and SQLite log management
 */

let chartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('compare-form');
  const inputThreads = document.getElementById('comp-threads');
  const inputIterations = document.getElementById('comp-iterations');
  const btnCompare = document.getElementById('btn-compare');
  const compProgress = document.getElementById('comp-progress');

  const tableEmpty = document.getElementById('compare-table-empty');
  const tableContent = document.getElementById('compare-table-content');
  const chartEmpty = document.getElementById('chart-empty');
  const chartWrapper = document.getElementById('chart-wrapper');

  const tblNoExpected = document.getElementById('tbl-no-expected');
  const tblMuExpected = document.getElementById('tbl-mu-expected');
  const tblNoActual = document.getElementById('tbl-no-actual');
  const tblMuActual = document.getElementById('tbl-mu-actual');
  const tblNoLost = document.getElementById('tbl-no-lost');
  const tblMuLost = document.getElementById('tbl-mu-lost');
  const tblNoRace = document.getElementById('tbl-no-race');
  const tblMuRace = document.getElementById('tbl-mu-race');
  const tblNoDuration = document.getElementById('tbl-no-duration');
  const tblMuDuration = document.getElementById('tbl-mu-duration');

  const btnClearLogs = document.getElementById('btn-clear-logs');
  const logsTableWrapper = document.getElementById('logs-table-wrapper');
  const logsTableBody = document.getElementById('logs-table-body');
  const logsEmpty = document.getElementById('logs-empty');

  // 1. Render Side-by-side Table
  function renderTable(data) {
    const no = data.no_mutex;
    const mu = data.mutex;

    tblNoExpected.textContent = formatNumber(no.expected);
    tblMuExpected.textContent = formatNumber(mu.expected);

    tblNoActual.textContent = formatNumber(no.actual);
    tblMuActual.textContent = formatNumber(mu.actual);

    tblNoLost.textContent = formatNumber(no.lost_updates);
    tblMuLost.textContent = formatNumber(mu.lost_updates);

    if (no.race_detected) {
      tblNoRace.innerHTML = '<span class="badge badge-danger">Race Detected (✕)</span>';
    } else {
      tblNoRace.innerHTML = '<span class="badge badge-success">Correct (✓)</span>';
    }

    if (mu.race_detected) {
      tblMuRace.innerHTML = '<span class="badge badge-danger">Race Detected (✕)</span>';
    } else {
      tblMuRace.innerHTML = '<span class="badge badge-success">Prevented (✓)</span>';
    }

    tblNoDuration.textContent = formatDuration(no.duration_ms);
    tblMuDuration.textContent = formatDuration(mu.duration_ms);

    tableEmpty.style.display = 'none';
    tableContent.style.display = 'block';
  }

  // 2. Render Chart.js Grouped Bar Chart
  function renderChart(no, mu) {
    chartEmpty.style.display = 'none';
    chartWrapper.style.display = 'block';

    const ctx = document.getElementById('comparisonChart').getContext('2d');

    if (chartInstance) {
      chartInstance.destroy();
    }

    // Chart.js 4.x configuration
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Without Mutex', 'With Mutex'],
        datasets: [
          {
            label: 'Expected',
            data: [no.expected, mu.expected],
            backgroundColor: '#5B574F', // ink-soft
            borderColor: '#1B1B1B',
            borderWidth: 1,
            barPercentage: 0.6,
            categoryPercentage: 0.7,
          },
          {
            label: 'Actual',
            data: [no.actual, mu.actual],
            backgroundColor: [
              no.race_detected ? '#9B2C2C' : '#2F6B4F', // danger / success
              '#2F6B4F', // success
            ],
            borderColor: '#1B1B1B',
            borderWidth: 1,
            barPercentage: 0.6,
            categoryPercentage: 0.7,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              font: { family: "'Inter', sans-serif", size: 12 },
              color: '#1B1B1B',
            },
          },
          tooltip: {
            callbacks: {
              label: (context) => ` ${context.dataset.label}: ${formatNumber(context.raw)}`,
            },
          },
        },
        scales: {
          x: {
            grid: { color: '#D9D3C5', drawTicks: true },
            ticks: {
              font: { family: "'Inter', sans-serif", weight: '600' },
              color: '#1B1B1B',
            },
          },
          y: {
            grid: { color: '#D9D3C5' },
            ticks: {
              font: { family: "'JetBrains Mono', monospace" },
              color: '#5B574F',
              callback: (value) => formatNumber(value),
            },
          },
        },
      },
    });
  }

  // 3. Load & Render SQLite Run Logs
  async function loadLogs() {
    try {
      const data = await fetchJSON('/api/runs?limit=50');
      const runs = data.runs || [];

      if (runs.length === 0) {
        logsEmpty.style.display = 'block';
        logsTableWrapper.style.display = 'none';
        return;
      }

      logsEmpty.style.display = 'none';
      logsTableWrapper.style.display = 'block';

      logsTableBody.innerHTML = runs.map(run => {
        let badgeHtml = '';
        if (run.race_detected) {
          badgeHtml = '<span class="badge badge-danger">Race (✕)</span>';
        } else if (run.mode === 'mutex') {
          badgeHtml = '<span class="badge badge-success">Safe (✓)</span>';
        } else {
          badgeHtml = '<span class="badge badge-neutral">Correct</span>';
        }

        return `
          <tr>
            <td>#${run.id}</td>
            <td style="font-size:0.8rem; color:var(--ink-soft);">${formatTimestamp(run.timestamp)}</td>
            <td style="text-transform:capitalize;">${run.operation}</td>
            <td>${run.mode === 'mutex' ? 'With Mutex' : 'Without Mutex'}</td>
            <td>${run.threads} &times; ${formatNumber(run.iterations)}</td>
            <td>${formatNumber(run.expected)}</td>
            <td style="font-weight:bold; color:${run.race_detected ? 'var(--danger)' : 'var(--success)'};">${formatNumber(run.actual)}</td>
            <td style="color:${run.lost_updates > 0 ? 'var(--danger)' : 'var(--ink-soft)'};">${formatNumber(run.lost_updates)}</td>
            <td>${badgeHtml}</td>
          </tr>
        `;
      }).join('');
    } catch (err) {
      console.error('Failed to load logs:', err);
    }
  }

  // 4. Form Submit
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const threads = parseInt(inputThreads.value, 10);
    const iterations = parseInt(inputIterations.value, 10);
    const operation = document.querySelector('input[name="operation"]:checked').value;

    if (isNaN(threads) || threads < 1 || threads > 64) {
      showToast('Threads must be between 1 and 64', 'danger');
      return;
    }
    if (isNaN(iterations) || iterations < 1 || iterations > 50000) {
      showToast('Iterations must be between 1 and 50,000', 'danger');
      return;
    }
    if (threads * iterations > 400000) {
      showToast('Threads × iterations cannot exceed 400,000', 'danger');
      return;
    }

    setButtonLoading(btnCompare, compProgress, true, 'Running comparison…');

    try {
      const payload = { threads, iterations, operation };
      const res = await fetchJSON('/api/compare', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      renderTable(res);
      renderChart(res.no_mutex, res.mutex);
      await loadLogs();
    } catch (err) {
      console.error(err);
    } finally {
      setButtonLoading(btnCompare, compProgress, false);
    }
  });

  // 5. Clear Logs Handler
  btnClearLogs.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to clear all simulation logs from the database?')) {
      return;
    }

    try {
      await fetchJSON('/api/runs', { method: 'DELETE' });
      showToast('All execution logs cleared successfully', 'success');
      await loadLogs();
    } catch (err) {
      console.error(err);
    }
  });

  // Initial log fetch
  loadLogs();
});
