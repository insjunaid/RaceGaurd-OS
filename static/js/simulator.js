/**
 * simulator.js - Interactive Thread Simulator controller
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('simulator-form');
  const inputThreads = document.getElementById('input-threads');
  const inputIterations = document.getElementById('input-iterations');
  const previewLine = document.getElementById('preview-line');
  const threadWarning = document.getElementById('thread-warning');
  const btnRun = document.getElementById('btn-run');
  const runProgress = document.getElementById('run-progress');

  const resultEmpty = document.getElementById('result-empty');
  const resultContent = document.getElementById('result-content');
  const statusCardBox = document.getElementById('status-card-box');

  const resExpected = document.getElementById('res-expected');
  const resActual = document.getElementById('res-actual');
  const resLost = document.getElementById('res-lost');
  const resDuration = document.getElementById('res-duration');
  const resId = document.getElementById('res-id');
  const resTime = document.getElementById('res-time');

  // 1. Live Preview Line calculation
  function updatePreview() {
    const threads = parseInt(inputThreads.value, 10) || 0;
    const iters = parseInt(inputIterations.value, 10) || 0;
    const op = document.querySelector('input[name="operation"]:checked')?.value || 'increment';

    // Toggle 1-thread warning
    if (threads === 1) {
      threadWarning.style.display = 'block';
    } else {
      threadWarning.style.display = 'none';
    }

    const totalOps = threads * iters;
    if (op === 'increment') {
      previewLine.innerHTML = `Expected: 0 + ${threads} &times; ${formatNumber(iters)} = <strong>${formatNumber(totalOps)}</strong>`;
    } else {
      previewLine.innerHTML = `Expected: ${formatNumber(totalOps)} &minus; ${threads} &times; ${formatNumber(iters)} = <strong>0</strong>`;
    }
  }

  // Bind input listeners
  inputThreads.addEventListener('input', updatePreview);
  inputIterations.addEventListener('input', updatePreview);
  document.querySelectorAll('input[name="operation"]').forEach(r => r.addEventListener('change', updatePreview));
  updatePreview(); // initial calculation

  // 2. Submit Simulation Form
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const threads = parseInt(inputThreads.value, 10);
    const iterations = parseInt(inputIterations.value, 10);
    const operation = document.querySelector('input[name="operation"]:checked').value;
    const mode = document.querySelector('input[name="mode"]:checked').value;

    // Client-side validation
    if (isNaN(threads) || threads < 1 || threads > 64) {
      showToast('Number of threads must be between 1 and 64', 'danger');
      return;
    }
    if (isNaN(iterations) || iterations < 1 || iterations > 50000) {
      showToast('Iterations per thread must be between 1 and 50,000', 'danger');
      return;
    }
    if (threads * iterations > 400000) {
      showToast('Total operations (threads × iterations) cannot exceed 400,000', 'danger');
      return;
    }

    setButtonLoading(btnRun, runProgress, true, 'Running threads…');

    try {
      const payload = { threads, iterations, operation, mode };
      const res = await fetchJSON('/api/simulate', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      // Render results
      resultEmpty.style.display = 'none';
      resultContent.style.display = 'block';

      if (res.race_detected) {
        statusCardBox.innerHTML = `
          <div class="frame danger" style="padding:20px 24px;">
            <div class="status-header">
              <span class="status-icon" style="font-size:1.3rem;">✕</span>
              <h3 class="status-title" style="color:var(--danger);">Race Condition Detected!</h3>
            </div>
            <p class="status-body" style="margin-bottom:0;">
              Threads overwrote each other's updates. The final value does not match the expected result.
            </p>
          </div>
        `;
        resActual.className = 'stat-number danger';
        resLost.className = 'stat-number danger';
      } else {
        const msg = res.mode === 'mutex'
          ? "Mutex lock ensures only one thread enters the critical section at a time, giving the exact expected value."
          : "Single-thread execution naturally avoids race conditions.";
        statusCardBox.innerHTML = `
          <div class="frame success" style="padding:20px 24px;">
            <div class="status-header">
              <span class="status-icon" style="font-size:1.3rem;">✓</span>
              <h3 class="status-title" style="color:var(--success);">Race Condition Prevented!</h3>
            </div>
            <p class="status-body" style="margin-bottom:0;">${msg}</p>
          </div>
        `;
        resActual.className = 'stat-number success';
        resLost.className = 'stat-number success';
      }

      resExpected.textContent = formatNumber(res.expected);
      resActual.textContent = formatNumber(res.actual);
      resLost.textContent = formatNumber(res.lost_updates);
      resDuration.textContent = formatDuration(res.duration_ms);
      resId.textContent = res.id;
      resTime.textContent = formatTimestamp(res.timestamp);

    } catch (err) {
      console.error(err);
    } finally {
      setButtonLoading(btnRun, runProgress, false);
    }
  });
});
