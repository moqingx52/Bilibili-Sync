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
  const clockFormatter = new Intl.DateTimeFormat(undefined, {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  let lastState = { status: 'paused', position_ms: 0, url: null };
  let lastStateAt = performance.now();
  let connectionStatus = 'disconnected';
  let playedMs = 0;
  let playStartedAt = null;

  const nowMs = () => performance.now();

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function setControlsEnabled(enabled) {
    [playBtn, pauseBtn, seekBtn].forEach((btn) => {
      if (btn) btn.disabled = !enabled;
    });
  }

  setControlsEnabled(false);

  function currentPlayedMs() {
    const inFlight = playStartedAt ? nowMs() - playStartedAt : 0;
    return Math.max(0, playedMs + inFlight);
  }

  function handleStatusTransition(prevStatus, nextStatus) {
    const now = nowMs();
    if (prevStatus !== 'playing' && nextStatus === 'playing') {
      playStartedAt = now;
    } else if (prevStatus === 'playing' && nextStatus !== 'playing') {
      const elapsed = playStartedAt ? now - playStartedAt : 0;
      playedMs += Math.max(0, elapsed);
      playStartedAt = null;
    }
  }

  function resetPlaybackForNewVideo(url) {
    playedMs = 0;
    playStartedAt = null;
    lastState = { status: 'paused', position_ms: 0, url: url || null };
    lastStateAt = nowMs();
    setControlsEnabled(Boolean(url));
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
    // Always reset src so repeated seek commands take effect.
    iframe.src = nextSrc;
  }

  function describePlayback() {
    const positionSeconds = Math.round(currentPositionMs() / 1000);
    const clock = clockFormatter.format(new Date());
    const stateLabel = lastState.status || 'unknown';
    const videoLabel = lastState.url ? 'video loaded' : 'no video';
    return `${connectionStatus}: ${stateLabel} | t=${positionSeconds}s | played=${Math.round(currentPlayedMs() / 1000)}s | ${videoLabel} | ${clock}`;
  }

  function refreshStatus() {
    if (connectionStatus !== 'connected') {
      setStatus('Disconnected - attempting reconnect');
      return;
    }
    setStatus(describePlayback());
  }

  socket.on('connect', () => {
    connectionStatus = 'connected';
    refreshStatus();
  });
  socket.on('disconnect', () => {
    connectionStatus = 'disconnected';
    setStatus('Disconnected - attempting reconnect');
    setControlsEnabled(false);
  });

  socket.on('state', (state) => {
    const prevStatus = lastState.status;
    const prevUrl = lastState.url;
    const urlChanged = state.url && prevUrl && state.url !== prevUrl;
    const firstUrlSet = state.url && !prevUrl;
    if (urlChanged || firstUrlSet) {
      playedMs = 0;
      playStartedAt = null;
      setControlsEnabled(true);
    } else if (!state.url) {
      setControlsEnabled(false);
    }
    handleStatusTransition(prevStatus, state.status);
    lastState = state;
    lastStateAt = nowMs();
    const positionMs = state.position_ms || 0;
    refreshStatus();
    if (state.url) {
      renderPlayer(state.url, state.status === 'playing', positionMs);
    }
  });

  function emitControl(type, position_ms) {
    if (!lastState.url) {
      setStatus('Load a video before using playback controls');
      return;
    }
    const positionMs = position_ms ?? Math.round(currentPositionMs());
    socket.emit('control', { type, position_ms: positionMs });
  }

  // Reset local timer when a new video is loaded via HTTP endpoint.
  document.addEventListener('video:loaded', (event) => {
    const url = event.detail && event.detail.url;
    if (!url) return;
    resetPlaybackForNewVideo(url);
    refreshStatus();
  });

  if (playBtn) playBtn.addEventListener('click', () => emitControl('play'));
  if (pauseBtn) pauseBtn.addEventListener('click', () => emitControl('pause'));
  if (seekBtn) seekBtn.addEventListener('click', () => emitControl('seek', 10000));

  // Periodically show the local playback status (play/pause, seconds, current clock).
  setInterval(refreshStatus, 1000);
  refreshStatus();
});
