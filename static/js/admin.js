document.addEventListener('DOMContentLoaded', function () {
  var body = document.body;

  function getCsrfToken() {
    var tokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return tokenInput ? tokenInput.value : '';
  }

  function postFormUrlEncoded(url, payload) {
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: payload
    }).then(function (r) { return r.json(); });
  }

  var sidebar = document.getElementById('adminSidebar');
  var overlay = document.getElementById('sidebarOverlay');
  var openBtn = document.getElementById('sidebarOpen');
  var closeBtn = document.getElementById('sidebarClose');

  function openSidebar() {
    if (!sidebar || !overlay) return;
    sidebar.classList.add('open');
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    if (openBtn) openBtn.setAttribute('aria-expanded', 'true');
    body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    if (!sidebar || !overlay) return;
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    if (openBtn) openBtn.setAttribute('aria-expanded', 'false');
    body.style.overflow = '';
  }

  if (openBtn) openBtn.addEventListener('click', openSidebar);
  if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
  if (overlay) overlay.addEventListener('click', closeSidebar);

  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      var message = el.getAttribute('data-confirm') || 'Lanjutkan?';
      if (!window.confirm(message)) e.preventDefault();
    });
  });

  document.addEventListener('click', function (e) {
    var closeAlertBtn = e.target.closest('[data-alert-close]');
    if (closeAlertBtn) {
      var alert = closeAlertBtn.closest('.admin-alert');
      if (alert) alert.remove();
    }
  });

  setTimeout(function () {
    document.querySelectorAll('.admin-alert').forEach(function (el) {
      el.style.transition = 'opacity 0.35s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 360);
    });
  }, 4500);

  var deleteModal = document.getElementById('deleteModal');
  var deleteForm = document.getElementById('deleteForm');
  var deleteTitle = document.getElementById('deleteModalTitle');
  var deleteText = document.getElementById('deleteModalText');
  var deleteCancelBtn = document.getElementById('deleteCancelBtn');
  var lastFocus = null;

  function openDeleteModal(url, name) {
    if (!deleteModal || !deleteForm) return;
    lastFocus = document.activeElement;
    deleteForm.action = url;
    if (deleteTitle) deleteTitle.textContent = 'Hapus ' + name + '?';
    if (deleteText) deleteText.textContent = 'Yakin ingin menghapus "' + name + '"? Tindakan ini tidak dapat dibatalkan.';
    deleteModal.classList.add('open');
    body.style.overflow = 'hidden';
    deleteModal.focus();
  }

  function closeDeleteModal() {
    if (!deleteModal) return;
    deleteModal.classList.remove('open');
    body.style.overflow = '';
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
  }

  document.addEventListener('click', function (e) {
    var deleteBtn = e.target.closest('[data-delete-url]');
    if (deleteBtn) {
      e.preventDefault();
      var deleteUrl = deleteBtn.getAttribute('data-delete-url');
      var deleteName = deleteBtn.getAttribute('data-delete-name') || 'item ini';
      openDeleteModal(deleteUrl, deleteName);
      return;
    }

    var statusBtn = e.target.closest('[data-order-action="status"]');
    if (statusBtn) {
      e.preventDefault();
      var orderId = statusBtn.getAttribute('data-order-id');
      var nextStatus = statusBtn.getAttribute('data-order-status');
      if (!orderId || !nextStatus) return;

      postFormUrlEncoded('/admin-panel/orders/' + orderId + '/status/', 'status=' + encodeURIComponent(nextStatus))
        .then(function (data) {
          if (!data || !data.success) return;
          var card = document.getElementById('orderCard' + orderId);
          if (card) {
            card.classList.add('is-removing');
            setTimeout(function () { card.remove(); }, 300);
          }
        })
        .catch(function () {});
      return;
    }

    var priceEditBtn = e.target.closest('[data-price-toggle]');
    if (priceEditBtn) {
      e.preventDefault();
      var orderIdFromToggle = priceEditBtn.getAttribute('data-price-toggle');
      togglePriceEdit(orderIdFromToggle, true);
      return;
    }

    var priceCancelBtn = e.target.closest('[data-price-cancel]');
    if (priceCancelBtn) {
      e.preventDefault();
      var orderIdFromCancel = priceCancelBtn.getAttribute('data-price-cancel');
      togglePriceEdit(orderIdFromCancel, false);
      return;
    }

    var removeDetailBtn = e.target.closest('[data-remove-row]');
    if (removeDetailBtn) {
      e.preventDefault();
      var row = removeDetailBtn.closest('[data-row]');
      if (row) row.remove();
      return;
    }

    var removePfBtn = e.target.closest('[data-remove-pf]');
    if (removePfBtn) {
      e.preventDefault();
      var pfRow = removePfBtn.closest('[data-pf-row]');
      if (pfRow) pfRow.remove();
      return;
    }
  });

  if (deleteCancelBtn) {
    deleteCancelBtn.addEventListener('click', closeDeleteModal);
  }
  if (deleteModal) {
    deleteModal.addEventListener('click', function (e) {
      if (e.target === deleteModal) closeDeleteModal();
    });
  }

  document.addEventListener('submit', function (e) {
    var priceForm = e.target.closest('[data-price-form]');
    if (!priceForm) return;
    e.preventDefault();

    var orderId = priceForm.getAttribute('data-price-form');
    var input = priceForm.querySelector('input[name="price"]');
    if (!orderId || !input) return;

    postFormUrlEncoded('/admin-panel/orders/' + orderId + '/price/', 'price=' + encodeURIComponent(input.value))
      .then(function (data) {
        if (!data || !data.success) return;
        var display = document.getElementById('priceDisplay' + orderId);
        if (display) {
          display.textContent = 'Rp' + Number(data.price).toLocaleString('id-ID');
        }
        togglePriceEdit(orderId, false);
      })
      .catch(function () {});
  });

  function togglePriceEdit(orderId, showEdit) {
    if (!orderId) return;
    var display = document.getElementById('priceDisplay' + orderId);
    var form = document.getElementById('priceForm' + orderId);
    if (!display || !form) return;

    if (showEdit) {
      display.classList.add('is-hidden');
      form.classList.remove('is-hidden');
      var formInput = form.querySelector('input[name="price"]');
      if (formInput) formInput.focus();
      return;
    }

    display.classList.remove('is-hidden');
    form.classList.add('is-hidden');
  }

  var websiteTabs = Array.prototype.slice.call(document.querySelectorAll('.website-tab'));
  var websitePanels = Array.prototype.slice.call(document.querySelectorAll('.tab-panel'));

  function activateWebsiteTab(tabName, updateHash) {
    var targetPanel = document.getElementById('tab-' + tabName);
    if (!targetPanel) return;

    websiteTabs.forEach(function (tab) {
      var isActive = tab.getAttribute('data-tab') === tabName;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    websitePanels.forEach(function (panel) {
      var isCurrent = panel.id === 'tab-' + tabName;
      panel.classList.toggle('active', isCurrent);
      panel.hidden = !isCurrent;
    });

    if (updateHash) {
      history.replaceState(null, '', '#' + tabName);
    }
  }

  if (websiteTabs.length) {
    websiteTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        activateWebsiteTab(tab.getAttribute('data-tab'), true);
      });
    });

    var hash = window.location.hash.replace('#', '');
    if (hash) {
      activateWebsiteTab(hash, false);
    } else {
      var activeTab = websiteTabs.find(function (tab) { return tab.classList.contains('active'); });
      if (activeTab) activateWebsiteTab(activeTab.getAttribute('data-tab'), false);
    }
  }

  var salesChartCanvas = document.getElementById('salesChart');
  document.querySelectorAll('.period-form .period-select').forEach(function (el) {
    el.addEventListener('change', function () {
      var form = el.closest('form');
      if (form) form.submit();
    });
  });

  if (salesChartCanvas && typeof Chart !== 'undefined') {
    var salesUrl = salesChartCanvas.dataset.salesUrl || '/admin-panel/dashboard/sales-data/';
    var month = salesChartCanvas.dataset.month;
    var year = salesChartCanvas.dataset.year;

    var salesChart = new Chart(salesChartCanvas, {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          data: [],
          borderColor: '#C9A456',
          backgroundColor: 'rgba(201,164,86,0.18)',
          borderWidth: 2,
          fill: true,
          tension: 0.45,
          pointRadius: 2,
          pointHoverRadius: 5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                return ' Rp ' + Number(ctx.parsed.y || 0).toLocaleString('id-ID');
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { font: { family: 'Nunito', size: 11 }, color: '#999' }
          },
          y: {
            grid: { color: 'rgba(0,0,0,0.05)' },
            ticks: {
              font: { family: 'Nunito', size: 11 },
              color: '#999',
              callback: function (v) {
                if (v >= 1000000) return (v / 1000000).toFixed(0) + 'jt';
                if (v >= 1000) return (v / 1000).toFixed(0) + 'k';
                return v;
              }
            }
          }
        }
      }
    });

    fetch(salesUrl + '?month=' + encodeURIComponent(month) + '&year=' + encodeURIComponent(year))
      .then(function (r) { return r.json(); })
      .then(function (data) {
        salesChart.data.labels = data.labels || [];
        salesChart.data.datasets[0].data = data.data || [];
        salesChart.update();
      })
      .catch(function () {});
  }

  var detailRowsWrap = document.getElementById('detailRows');
  var addDetailRowBtn = document.getElementById('addDetailRow');
  if (detailRowsWrap && addDetailRowBtn) {
    var detailCount = detailRowsWrap.querySelectorAll('[data-row]').length;
    addDetailRowBtn.addEventListener('click', function () {
      var row = document.createElement('div');
      row.className = 'detail-row';
      row.setAttribute('data-row', '');
      row.innerHTML = [
        '<div class="form-row">',
        '<div class="form-group"><input type="text" name="detail_' + detailCount + '-label" class="form-control" placeholder="Label (mis: Main Flowers)"></div>',
        '<div class="form-group"><textarea name="detail_' + detailCount + '-content" class="form-control form-textarea" rows="2" placeholder="Deskripsi detail..."></textarea></div>',
        '<button type="button" class="btn-remove-row" data-remove-row aria-label="Hapus detail">&#10005;</button>',
        '</div>'
      ].join('');
      detailRowsWrap.appendChild(row);
      detailCount += 1;
    });
  }

  var pfRowsWrap = document.getElementById('pfRows');
  var addPfRowBtn = document.getElementById('addPfRow');
  if (pfRowsWrap && addPfRowBtn) {
    var pfCount = pfRowsWrap.querySelectorAll('[data-pf-row]').length;
    addPfRowBtn.addEventListener('click', function () {
      var row = document.createElement('div');
      row.className = 'pf-row';
      row.setAttribute('data-pf-row', '');
      row.innerHTML = [
        '<div class="form-row form-row-pf">',
        '<div class="form-group"><input type="text" name="pf_' + pfCount + '-item" class="form-control" placeholder="Item perfect for..."></div>',
        '<button type="button" class="btn-remove-row" data-remove-pf aria-label="Hapus perfect for">&#10005;</button>',
        '</div>'
      ].join('');
      pfRowsWrap.appendChild(row);
      pfCount += 1;
    });
  }

  var productSelect = document.getElementById('productSelect');
  var productNameField = document.getElementById('productNameField');
  var priceField = document.getElementById('priceField');

  if (productSelect && productNameField) {
    productSelect.addEventListener('change', function () {
      var opt = this.options[this.selectedIndex];
      if (!opt || !opt.value) return;

      productNameField.value = opt.text.trim();

      var directPrice = opt.dataset.price;
      if (directPrice && priceField) {
        priceField.value = directPrice;
        return;
      }

      if (!priceField) return;

      fetch('/admin-panel/products/?pk=' + encodeURIComponent(opt.value) + '&json=1')
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (data) {
          if (data && data.price) priceField.value = data.price;
        })
        .catch(function () {});
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeSidebar();
      closeDeleteModal();
    }
  });
});
