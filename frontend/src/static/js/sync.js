document.addEventListener('DOMContentLoaded', () => {
  if (!window.io) {
    return;
  }
  const socket = io({ withCredentials: true });
  const statusEl = document.getElementById('video-message');
  const playBtn = document.getElementById('play-btn');
  const pauseBtn = document.getElementById('pause-btn');
  const seekBtn = document.getElementById('seek-btn');
  const container = document.getElementById('player-container');

  let lastState = { status: 'paused', position_ms: 0, url: null };
  let lastStateAt = performance.now();

  const nowMs = () => performance.now();

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function currentPositionMs() {
    const base = lastState.position_ms || 0;
    if (lastState.status === 'playing') {
      return Math.max(0, base + (nowMs() - lastStateAt));
    }
    return Math.max(0, base);
  }

  function renderPlayer(url, isPlaying, positionMs) {
    if (!container) return;
    const target = new URL(url);
    target.searchParams.set('autoplay', isPlaying ? '1' : '0');
    const seconds = Math.floor(Math.max(0, positionMs || 0) / 1000);
    if (seconds > 0) {
      target.searchParams.set('t', String(seconds));
    } else {
      target.searchParams.delete('t');
    }
    let iframe = container.querySelector('iframe');
    if (!iframe) {
      iframe = document.createElement('iframe');
      iframe.setAttribute('allow', 'autoplay; fullscreen');
      iframe.setAttribute('frameborder', '0');
      iframe.style.width = '100%';
      iframe.style.height = '480px';
      container.appendChild(iframe);
    }
    const nextSrc = target.toString();
    if (iframe.src !== nextSrc) {
      iframe.src = nextSrc;
    }
  }

  socket.on('connect', () => setStatus('Connected'));
  socket.on('disconnect', () => setStatus('Disconnected - attempting reconnect'));

  socket.on('state', (state) => {
    lastState = state;
    lastStateAt = nowMs();
    const positionMs = state.position_ms || 0;
    setStatus(`Status: ${state.status} @ ${positionMs}ms`);
    if (state.url) {
      renderPlayer(state.url, state.status === 'playing', positionMs);
    }
  });

  function emitControl(type, position_ms) {
    const positionMs = position_ms ?? Math.round(currentPositionMs());
    socket.emit('control', { type, position_ms: positionMs });
  }

  if (playBtn) playBtn.addEventListener('click', () => emitControl('play'));
  if (pauseBtn) pauseBtn.addEventListener('click', () => emitControl('pause'));
  if (seekBtn) seekBtn.addEventListener('click', () => emitControl('seek', 10000));
});
