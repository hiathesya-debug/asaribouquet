document.addEventListener('DOMContentLoaded', function () {
  var overlay = document.getElementById('menuOverlay');
  var openBtn = document.getElementById('menuOpenBtn');
  var closeBtn = document.getElementById('menuCloseBtn');
  var searchToggle = document.getElementById('searchToggle');
  var searchBar = document.getElementById('searchBarWrapper');
  var searchInput = document.getElementById('searchInput');

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

  function openSearch() {
    if (!searchBar) return;
    searchBar.classList.add('visible');
    searchBar.setAttribute('aria-hidden', 'false');
    if (searchToggle) searchToggle.setAttribute('aria-expanded', 'true');
    setTimeout(function () {
      if (searchInput) searchInput.focus();
    }, 280);
  }

  function closeSearch() {
    if (!searchBar) return;
    searchBar.classList.remove('visible');
    searchBar.setAttribute('aria-hidden', 'true');
    if (searchToggle) searchToggle.setAttribute('aria-expanded', 'false');
  }

  if (openBtn) openBtn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);

  if (overlay) {
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeMenu();
    });
  }

  if (searchToggle) {
    searchToggle.addEventListener('click', function () {
      if (searchBar && searchBar.classList.contains('visible')) {
        closeSearch();
      } else {
        openSearch();
      }
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeMenu();
      closeSearch();
    }
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth >= 1024) closeMenu();
  });

  document.querySelectorAll('.menu-panel [data-submenu-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.getElementById(btn.dataset.submenuToggle);
      if (!target) return;
      var isOpen = target.classList.contains('open');

      document.querySelectorAll('.menu-sub.open').forEach(function (sub) {
        sub.classList.remove('open');
        var toggle = sub.previousElementSibling;
        if (toggle) {
          toggle.setAttribute('aria-expanded', 'false');
          var toggleIcon = toggle.querySelector('.submenu-icon');
          if (toggleIcon) toggleIcon.textContent = '+';
        }
      });

      if (!isOpen) {
        target.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
        var icon = btn.querySelector('.submenu-icon');
        if (icon) icon.textContent = '-';
      } else {
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  });

  var navbar = document.getElementById('siteNavbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  document.querySelectorAll('[data-accordion]').forEach(function (accordion) {
    var header = accordion.querySelector('.terms-accordion-header');
    var body = accordion.querySelector('.terms-accordion-body');
    var viewBtn = accordion.querySelector('[data-view-btn]');
    var chevron = accordion.querySelector('.terms-chevron');
    var showLess = accordion.querySelector('[data-terms-collapse]');
    if (!header || !body) return;

    function openAccordion() {
      accordion.classList.add('open');
      body.hidden = false;
      header.setAttribute('aria-expanded', 'true');
      if (viewBtn) viewBtn.hidden = true;
      if (chevron) chevron.innerHTML = '&#8743;';
    }

    function closeAccordion() {
      accordion.classList.remove('open');
      body.hidden = true;
      header.setAttribute('aria-expanded', 'false');
      if (viewBtn) viewBtn.hidden = false;
      if (chevron) chevron.innerHTML = '&#8744;';
    }

    if (accordion.classList.contains('open')) {
      openAccordion();
    } else {
      closeAccordion();
    }

    header.addEventListener('click', function () {
      if (accordion.classList.contains('open')) {
        closeAccordion();
      } else {
        openAccordion();
      }
    });

    if (viewBtn) viewBtn.addEventListener('click', openAccordion);
    if (showLess) showLess.addEventListener('click', closeAccordion);
  });

  document.querySelectorAll('[data-wa-order]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var phone = btn.getAttribute('data-wa-number');
      var message = btn.getAttribute('data-wa-message') || '';
      if (!phone) return;
      window.open('https://wa.me/' + phone + '?text=' + encodeURIComponent(message), '_blank');
    });
  });

  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(function () {
        el.remove();
      }, 400);
    });
  }, 4000);
});
