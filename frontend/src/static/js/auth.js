document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const loginError = document.getElementById('login-error');

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      loginError.textContent = '';

      const userIdInput = document.getElementById('user_id');
      const passwordInput = document.getElementById('password');
      const user_id = userIdInput.value.trim();
      const password = passwordInput.value;

      try {
        const resp = await fetch('/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id, password }),
        });

        if (resp.ok) {
          window.location.href = '/';
        } else {
          let msg = 'Login failed';
          try {
            const data = await resp.json();
            if (data && data.error) {
              msg = data.error;
            }
          } catch (_) {
            // ignore
          }
          loginError.textContent = msg;
        }
      } catch (err) {
        loginError.textContent = 'Network error';
      }
    });
  }

  const logoutForm = document.getElementById('logout-form');
  if (logoutForm) {
    logoutForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      await fetch('/logout', { method: 'POST' });
      window.location.href = '/login';
    });
  }
});
