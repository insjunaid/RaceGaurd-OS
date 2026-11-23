/**
 * prevention.js - Race Prevention view controller
 */

document.addEventListener('DOMContentLoaded', async () => {
  const emptySection = document.getElementById('prevention-empty');
  const cardContainer = document.getElementById('prevention-card-container');

  const prevOp = document.getElementById('prev-op');
  const prevThreads = document.getElementById('prev-threads');
  const prevIters = document.getElementById('prev-iters');
  const prevDuration = document.getElementById('prev-duration');
  const prevExpected = document.getElementById('prev-expected');
  const prevActual = document.getElementById('prev-actual');
  const prevLost = document.getElementById('prev-lost');
  const prevTimestamp = document.getElementById('prev-timestamp');
  const prevId = document.getElementById('prev-id');

  const btnRunAgain = document.getElementById('btn-run-again-mutex');
  const prevProgress = document.getElementById('prev-progress');

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
      mode: 'mutex',
    };

    emptySection.style.display = 'none';
    cardContainer.style.display = 'block';

    prevOp.textContent = run.operation;
    prevThreads.textContent = run.threads;
    prevIters.textContent = formatNumber(run.iterations);
    prevDuration.textContent = formatDuration(run.duration_ms);
    prevExpected.textContent = formatNumber(run.expected);
    prevActual.textContent = formatNumber(run.actual);
    prevLost.textContent = formatNumber(run.lost_updates);
    prevTimestamp.textContent = formatTimestamp(run.timestamp);
    prevId.textContent = run.id;
  }

  // Initial load: fetch latest mutex run
  try {
    const data = await fetchJSON('/api/runs/latest?mode=mutex');
    renderRun(data);
  } catch (err) {
    console.error('Failed to load latest synchronized run:', err);
    emptySection.style.display = 'block';
  }

  // Run Again button
  btnRunAgain.addEventListener('click', async () => {
    if (!currentParams) return;

    setButtonLoading(btnRunAgain, prevProgress, true, 'Running threads…');
    try {
      const updated = await fetchJSON('/api/simulate', {
        method: 'POST',
        body: JSON.stringify(currentParams),
      });
      renderRun(updated);
    } catch (err) {
      console.error(err);
    } finally {
      setButtonLoading(btnRunAgain, prevProgress, false);
    }
  });
});
