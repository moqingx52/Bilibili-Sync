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

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function renderPlayer(url, isPlaying) {
    if (!container) return;
    const target = new URL(url);
    target.searchParams.set('autoplay', isPlaying ? '1' : '0');
    let iframe = container.querySelector('iframe');
    if (!iframe) {
      iframe = document.createElement('iframe');
      iframe.setAttribute('allowfullscreen', '');
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
    setStatus(`Status: ${state.status} @ ${state.position_ms || 0}ms`);
    if (state.url) {
      renderPlayer(state.url, state.status === 'playing');
    }
  });

  function emitControl(type, position_ms) {
    socket.emit('control', { type, position_ms });
  }

  if (playBtn) playBtn.addEventListener('click', () => emitControl('play'));
  if (pauseBtn) pauseBtn.addEventListener('click', () => emitControl('pause'));
  if (seekBtn) seekBtn.addEventListener('click', () => emitControl('seek', 10000));
});
