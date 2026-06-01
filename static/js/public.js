/* ═══════════════════════════════════════
   ASARI — Public JS
   ═══════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  /* ── Mobile Menu ───────────────────────────────────────── */
  const overlay  = document.getElementById('menuOverlay');
  const openBtn  = document.getElementById('menuOpenBtn');
  const closeBtn = document.getElementById('menuCloseBtn');

  function openMenu() {
    if (!overlay) return;
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    if (openBtn) openBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    if (!overlay) return;
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    if (openBtn) openBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  if (openBtn)  openBtn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);

  // Click on backdrop (outside menu-panel) closes the menu
  if (overlay) {
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeMenu();
    });
  }

  // ESC closes menu
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeMenu(); closeSearch(); }
  });

  // Close menu on resize to desktop
  window.addEventListener('resize', function () {
    if (window.innerWidth >= 1024) closeMenu();
  });

  /* ── Submenu Toggle (mobile drawer) ───────────────────── */
  document.querySelectorAll('[data-submenu-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const target = document.getElementById(this.dataset.submenuToggle);
      if (!target) return;
      const isOpen = target.classList.contains('open');
      // Close all other submenus
      document.querySelectorAll('.menu-sub.open').forEach(function (sub) {
        sub.classList.remove('open');
        var icon = sub.previousElementSibling
                      ? sub.previousElementSibling.querySelector('.submenu-icon')
                      : null;
        if (icon) icon.textContent = '+';
      });
      if (!isOpen) {
        target.classList.add('open');
        const icon = this.querySelector('.submenu-icon');
        if (icon) icon.textContent = '−';
      }
    });
  });

  /* ── Search bar ────────────────────────────────────────── */
  const searchToggle = document.getElementById('searchToggle');
  const searchBar    = document.getElementById('searchBarWrapper');
  const searchInput  = document.getElementById('searchInput');

  function openSearch() {
    if (!searchBar) return;
    searchBar.classList.add('visible');
    searchBar.setAttribute('aria-hidden', 'false');
    if (searchToggle) searchToggle.setAttribute('aria-expanded', 'true');
    setTimeout(function () { if (searchInput) searchInput.focus(); }, 280);
  }

  function closeSearch() {
    if (!searchBar) return;
    searchBar.classList.remove('visible');
    searchBar.setAttribute('aria-hidden', 'true');
    if (searchToggle) searchToggle.setAttribute('aria-expanded', 'false');
  }

  if (searchToggle) {
    searchToggle.addEventListener('click', function () {
      searchBar && searchBar.classList.contains('visible')
        ? closeSearch()
        : openSearch();
    });
  }

  /* ── Scroll shadow on navbar ───────────────────────────── */
  var navbar = document.getElementById('siteNavbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  /* ── Terms Accordion ───────────────────────────────────── */
  document.querySelectorAll('.terms-section-header').forEach(function (header, idx) {
    header.addEventListener('click', function () {
      var body   = this.nextElementSibling;
      var isOpen = body.classList.contains('open');

      document.querySelectorAll('.terms-section-body').forEach(function (b) { b.classList.remove('open'); });
      document.querySelectorAll('.terms-section-header').forEach(function (h) { h.classList.remove('open'); });

      if (!isOpen) {
        body.classList.add('open');
        this.classList.add('open');
      }
    });

    // Open first one by default
    if (idx === 0) {
      header.classList.add('open');
      var body = header.nextElementSibling;
      if (body) body.classList.add('open');
    }
  });

  /* ── Auto-dismiss flash messages ──────────────────────── */
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity    = '0';
      setTimeout(function () { el.remove(); }, 400);
    });
  }, 4000);

});

/* ── WhatsApp Order ─────────────────────────────────────── */
function orderViaWhatsApp(phone, message) {
  window.open('https://wa.me/' + phone + '?text=' + encodeURIComponent(message), '_blank');
}