/* ═══════════════════════════
   ASARI — Public JS
   ═══════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Mobile Menu ──
  const overlay = document.getElementById('menuOverlay');
  const openBtn = document.getElementById('menuOpenBtn');
  const closeBtn = document.getElementById('menuCloseBtn');

  if (openBtn && overlay) {
    openBtn.addEventListener('click', () => {
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  }
  if (closeBtn && overlay) {
    closeBtn.addEventListener('click', closeMenu);
  }
  if (overlay) {
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeMenu();
    });
  }

  function closeMenu() {
    if (overlay) {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  // ── Submenu Toggle ──
  document.querySelectorAll('[data-submenu-toggle]').forEach(btn => {
    btn.addEventListener('click', function () {
      const target = document.getElementById(this.dataset.submenuToggle);
      if (target) {
        target.classList.toggle('open');
        const icon = this.querySelector('.submenu-icon');
        if (icon) icon.textContent = target.classList.contains('open') ? '−' : '+';
      }
    });
  });

  // ── Terms Accordion ──
  document.querySelectorAll('.terms-section-header').forEach(header => {
    header.addEventListener('click', function () {
      const body = this.nextElementSibling;
      const isOpen = body.classList.contains('open');

      // Close all others
      document.querySelectorAll('.terms-section-body').forEach(b => b.classList.remove('open'));
      document.querySelectorAll('.terms-section-header').forEach(h => h.classList.remove('open'));

      if (!isOpen) {
        body.classList.add('open');
        this.classList.add('open');
      }
    });

    // Open first one
    const idx = [...document.querySelectorAll('.terms-section-header')].indexOf(header);
    if (idx === 0) {
      header.classList.add('open');
      const body = header.nextElementSibling;
      if (body) body.classList.add('open');
    }
  });

  // ── Auto-dismiss messages ──
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    });
  }, 4000);

  // ── Search form ──
  const searchForm = document.getElementById('searchForm');
  const searchInput = document.getElementById('searchInput');
  const searchToggle = document.getElementById('searchToggle');
  const searchBar = document.getElementById('searchBarWrapper');

  if (searchToggle && searchBar) {
    searchToggle.addEventListener('click', () => {
      searchBar.classList.toggle('visible');
      if (searchBar.classList.contains('visible') && searchInput) {
        searchInput.focus();
      }
    });
  }
});

// ── WhatsApp Order ──
function orderViaWhatsApp(phone, message) {
  const encoded = encodeURIComponent(message);
  window.open(`https://wa.me/${phone}?text=${encoded}`, '_blank');
}
