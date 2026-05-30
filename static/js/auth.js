/* ============================================================
   PayTrack — Auth Pages JavaScript
   Handles: password toggle, strength meter, form validation,
   submit loading state, input animation, CSRF awareness
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. PASSWORD VISIBILITY TOGGLE ── */
  document.querySelectorAll('.toggle-pass').forEach(btn => {
    btn.addEventListener('click', () => {
      const wrap  = btn.closest('.field-input-wrap');
      const input = wrap.querySelector('.field-input');
      const isText = input.type === 'text';
      input.type = isText ? 'password' : 'text';
      btn.textContent = isText ? '👁' : '🙈';
    });
  });

  /* ── 2. PASSWORD STRENGTH METER ── */
  const passInput = document.getElementById('id_password1') || document.getElementById('id_password');
  const strengthBar = document.querySelector('.strength-bar');
  const strengthLabel = document.querySelector('.strength-label');

  if (passInput && strengthBar) {
    passInput.addEventListener('input', () => {
      const val = passInput.value;
      const score = getStrengthScore(val);
      updateStrengthUI(score);
    });
  }

  function getStrengthScore(password) {
    let score = 0;
    if (!password) return 0;
    if (password.length >= 8)  score++;
    if (password.length >= 12) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    return Math.min(score, 4);
  }

  function updateStrengthUI(score) {
    if (!strengthBar) return;
    const segs = strengthBar.querySelectorAll('.strength-seg');
    const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
    const classes = ['', 'weak', 'fair', 'good', 'strong'];
    const colors = ['', '#ef4444', '#f59e0b', '#60a5fa', '#10b981'];

    segs.forEach((seg, i) => {
      seg.className = 'strength-seg';
      if (i < score) seg.classList.add(classes[score]);
    });
    if (strengthLabel) {
      strengthLabel.textContent = score > 0 ? labels[score] : '';
      strengthLabel.style.color = colors[score];
    }
  }

  /* ── 3. LIVE PASSWORD MATCH INDICATOR ── */
  const pass1 = document.getElementById('id_password1');
  const pass2 = document.getElementById('id_password2');

  if (pass1 && pass2) {
    function checkMatch() {
      if (!pass2.value) return;
      const match = pass1.value === pass2.value;
      pass2.classList.toggle('error', !match);
      let hint = pass2.parentElement.parentElement.querySelector('.match-hint');
      if (!hint) {
        hint = document.createElement('p');
        hint.className = 'field-error match-hint';
        pass2.parentElement.after(hint);
      }
      if (!match) {
        hint.textContent = 'Passwords do not match';
        hint.style.display = 'flex';
      } else {
        hint.style.display = 'none';
      }
    }
    pass2.addEventListener('input', checkMatch);
    pass1.addEventListener('input', () => { if (pass2.value) checkMatch(); });
  }

  /* ── 4. SUBMIT BUTTON LOADING STATE ── */
  document.querySelectorAll('.auth-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      const btn = form.querySelector('.btn-auth');
      if (!btn) return;

      // Basic HTML5 validation check
      if (!form.checkValidity()) return;

      // Password match guard
      if (pass1 && pass2 && pass1.value !== pass2.value) return;

      btn.classList.add('loading');
      btn.disabled = true;

      // Safety fallback — re-enable after 8s in case of slow network
      setTimeout(() => {
        btn.classList.remove('loading');
        btn.disabled = false;
      }, 8000);
    });
  });

  /* ── 5. INPUT FOCUS ANIMATIONS ── */
  document.querySelectorAll('.field-input').forEach(input => {
    const group = input.closest('.field-group');
    if (!group) return;

    input.addEventListener('focus', () => {
      group.style.transform = 'translateY(-1px)';
      group.style.transition = 'transform 0.2s ease';
    });
    input.addEventListener('blur', () => {
      group.style.transform = 'translateY(0)';
    });
  });

  /* ── 6. RESEND COOLDOWN TIMER ── */
  const resendBtn = document.getElementById('resend-btn');
  if (resendBtn) {
    const COOLDOWN = 60;
    let timer = null;

    // Check if cooldown is active from sessionStorage
    const lastSent = sessionStorage.getItem('paytrack_resend_ts');
    if (lastSent) {
      const elapsed = Math.floor((Date.now() - parseInt(lastSent)) / 1000);
      if (elapsed < COOLDOWN) startCooldown(COOLDOWN - elapsed);
    }

    resendBtn.closest('form')?.addEventListener('submit', () => {
      sessionStorage.setItem('paytrack_resend_ts', Date.now().toString());
      startCooldown(COOLDOWN);
    });

    function startCooldown(seconds) {
      resendBtn.disabled = true;
      let remaining = seconds;
      resendBtn.textContent = `Resend in ${remaining}s`;
      timer = setInterval(() => {
        remaining--;
        resendBtn.textContent = `Resend in ${remaining}s`;
        if (remaining <= 0) {
          clearInterval(timer);
          resendBtn.disabled = false;
          resendBtn.textContent = 'Resend verification email';
        }
      }, 1000);
    }
  }

  /* ── 7. AUTO-DISMISS DJANGO MESSAGES ── */
  document.querySelectorAll('.messages li').forEach(msg => {
    setTimeout(() => {
      msg.style.transition = 'opacity 0.5s, transform 0.5s';
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(-8px)';
      setTimeout(() => msg.remove(), 500);
    }, 5000);
  });

  /* ── 8. STAGGER CARD CHILDREN ON LOAD ── */
  const card = document.querySelector('.auth-card');
  if (card) {
    const items = card.querySelectorAll('.auth-card-icon, .auth-card-title, .auth-card-sub, .auth-alert, .auth-form > *, .auth-status-icon, .auth-steps, .auth-footer-text');
    items.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(14px)';
      el.style.transition = `opacity 0.5s ease ${0.1 + i * 0.07}s, transform 0.5s ease ${0.1 + i * 0.07}s`;
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        });
      });
    });
  }

});