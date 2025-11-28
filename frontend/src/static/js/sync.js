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

  socket.on('connect', () => setStatus('Connected'));
  socket.on('disconnect', () => setStatus('Disconnected - attempting reconnect'));

  socket.on('state', (state) => {
    setStatus(`Status: ${state.status} @ ${state.position_ms || 0}ms`);
    if (state.url && container && !container.querySelector('iframe')) {
      container.innerHTML = `<iframe src=\"${state.url}\" allowfullscreen frameborder=\"0\" width=\"100%\" height=\"480\"></iframe>`;
    }
  });

  function emitControl(type, position_ms) {
    socket.emit('control', { type, position_ms });
  }

  if (playBtn) playBtn.addEventListener('click', () => emitControl('play'));
  if (pauseBtn) pauseBtn.addEventListener('click', () => emitControl('pause'));
  if (seekBtn) seekBtn.addEventListener('click', () => emitControl('seek', 10000));
});
