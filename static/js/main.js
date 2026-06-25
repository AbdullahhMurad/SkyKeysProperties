/* SkyKeysProperties – main.js */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Mobile nav toggle ──────────────────────────────────── */
  const toggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
    // Close on link click
    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => navLinks.classList.remove('open'));
    });
  }

  /* ── Active nav link ────────────────────────────────────── */
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });

  /* ── Scroll reveal ──────────────────────────────────────── */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => entry.target.classList.add('visible'), i * 80);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(el => observer.observe(el));
  }

  /* ── Property filter tabs ───────────────────────────────── */
  const filterTabs = document.querySelectorAll('.filter-tab');
  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      filterTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const type = tab.dataset.filter; // 'all' | 'sale' | 'rent'
      const cards = document.querySelectorAll('.prop-card-wrap');

      cards.forEach(card => {
        if (type === 'all' || card.dataset.type === type) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });

      // Show empty state if nothing visible
      const visible = [...cards].filter(c => c.style.display !== 'none');
      const emptyState = document.getElementById('emptyState');
      if (emptyState) {
        emptyState.style.display = visible.length === 0 ? 'block' : 'none';
      }
    });
  });

  /* ── Contact form ───────────────────────────────────────── */
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const success = document.getElementById('formSuccess');
      const errorEl = document.getElementById('formError');

      btn.disabled = true;
      btn.textContent = 'Sending…';
      if (errorEl) errorEl.style.display = 'none';

      const data = {
        name:    form.name.value,
        email:   form.email.value,
        phone:   form.phone ? form.phone.value : '',
        subject: form.subject ? form.subject.value : 'General Inquiry',
        message: form.message.value,
      };

      try {
        const res = await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });

        if (res.ok) {
          form.reset();
          if (success) success.style.display = 'block';
        } else {
          throw new Error('Server error');
        }
      } catch {
        if (errorEl) { errorEl.textContent = 'Something went wrong. Please try again.'; errorEl.style.display = 'block'; }
      } finally {
        btn.disabled = false;
        btn.textContent = 'Send Message';
      }
    });
  }

});
