/**
 * detection.js - Race Detection view controller
 */

document.addEventListener('DOMContentLoaded', async () => {
  const emptySection = document.getElementById('detection-empty');
  const cardContainer = document.getElementById('detection-card-container');

  const detOp = document.getElementById('det-op');
  const detThreads = document.getElementById('det-threads');
  const detIters = document.getElementById('det-iters');
  const detDuration = document.getElementById('det-duration');
  const detExpected = document.getElementById('det-expected');
  const detActual = document.getElementById('det-actual');
  const detLost = document.getElementById('det-lost');
  const detTimestamp = document.getElementById('det-timestamp');
  const detId = document.getElementById('det-id');

  const btnRunAgain = document.getElementById('btn-run-again');
  const detProgress = document.getElementById('det-progress');

  let currentParams = null;

  function renderRun(run) {
    if (!run || !run.id) {
      emptySection.style.display = 'block';
      cardContainer.style.display = 'none';
      return;
    }

    currentParams = {
      threads: run.threads,
      operation: run.operation,
      iterations: run.iterations,
      mode: 'no_mutex',
    };

    emptySection.style.display = 'none';
    cardContainer.style.display = 'block';

    detOp.textContent = run.operation;
    detThreads.textContent = run.threads;
    detIters.textContent = formatNumber(run.iterations);
    detDuration.textContent = formatDuration(run.duration_ms);
    detExpected.textContent = formatNumber(run.expected);
    detActual.textContent = formatNumber(run.actual);
    detLost.textContent = formatNumber(run.lost_updates);
    detTimestamp.textContent = formatTimestamp(run.timestamp);
    detId.textContent = run.id;
  }

  // Initial load: fetch latest no_mutex run
  try {
    const data = await fetchJSON('/api/runs/latest?mode=no_mutex');
    renderRun(data);
  } catch (err) {
    console.error('Failed to load latest unsynchronized run:', err);
    emptySection.style.display = 'block';
  }

  // Run Again button
  btnRunAgain.addEventListener('click', async () => {
    if (!currentParams) return;

    setButtonLoading(btnRunAgain, detProgress, true, 'Running threads…');
    try {
      const updated = await fetchJSON('/api/simulate', {
        method: 'POST',
        body: JSON.stringify(currentParams),
      });
      renderRun(updated);
    } catch (err) {
      console.error(err);
    } finally {
      setButtonLoading(btnRunAgain, detProgress, false);
    }
  });
});
