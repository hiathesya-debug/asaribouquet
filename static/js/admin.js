/* ═══════════════════════════
   ASARI — Admin JS
   ═══════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Sidebar ──
  const sidebarEl    = document.getElementById('adminSidebar');
  const sidebarOver  = document.getElementById('sidebarOverlay');
  const sidebarOpen  = document.getElementById('sidebarOpen');
  const sidebarClose = document.getElementById('sidebarClose');

  function openSidebar() {
    sidebarEl && sidebarEl.classList.add('open');
    sidebarOver && sidebarOver.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    sidebarEl && sidebarEl.classList.remove('open');
    sidebarOver && sidebarOver.classList.remove('open');
    document.body.style.overflow = '';
  }

  sidebarOpen && sidebarOpen.addEventListener('click', openSidebar);
  sidebarClose && sidebarClose.addEventListener('click', closeSidebar);
  sidebarOver && sidebarOver.addEventListener('click', closeSidebar);

  // ── Sidebar submenu ──
  document.querySelectorAll('[data-sidebar-toggle]').forEach(btn => {
    btn.addEventListener('click', function () {
      const target = document.getElementById(this.dataset.sidebarToggle);
      if (target) {
        target.classList.toggle('open');
        const icon = this.querySelector('.sidebar-toggle-icon');
        if (icon) icon.textContent = target.classList.contains('open') ? '−' : '+';
      }
    });
  });

  // ── Sales chart ──
  const chartCanvas = document.getElementById('salesChart');
  if (chartCanvas) {
    const month = chartCanvas.dataset.month;
    const year = chartCanvas.dataset.year;

    fetch(`/admin-panel/dashboard/sales-data/?month=${month}&year=${year}`)
      .then(r => r.json())
      .then(data => {
        new Chart(chartCanvas, {
          type: 'line',
          data: {
            labels: data.labels,
            datasets: [{
              data: data.data,
              fill: true,
              backgroundColor: 'rgba(201,164,86,0.20)',
              borderColor: 'rgba(201,164,86,0.9)',
              borderWidth: 2,
              tension: 0.4,
              pointRadius: 0,
              pointHoverRadius: 4,
              pointHoverBackgroundColor: '#C9A456',
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  label: ctx => `Rp ${Number(ctx.raw).toLocaleString('id-ID')}`
                }
              }
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: { font: { size: 10 }, color: '#aaa' }
              },
              y: {
                grid: { color: 'rgba(0,0,0,0.05)' },
                ticks: {
                  font: { size: 10 }, color: '#aaa',
                  callback: v => `${v / 1000}k`
                }
              }
            }
          }
        });
      })
      .catch(console.error);
  }

  // ── Order status update (AJAX) ──
  document.querySelectorAll('[data-order-status]').forEach(btn => {
    btn.addEventListener('click', function () {
      const orderId = this.dataset.orderId;
      const newStatus = this.dataset.orderStatus;
      const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
      if (!csrf) return;

      const card = this.closest('.order-card');

      fetch(`/admin-panel/orders/${orderId}/status/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrf.value,
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: `status=${newStatus}`
      })
        .then(r => r.json())
        .then(data => {
          if (data.success && card) {
            card.style.transition = 'opacity 0.3s';
            card.style.opacity = '0';
            setTimeout(() => {
              card.remove();
              updateCountBadge(newStatus);
            }, 300);
          }
        })
        .catch(console.error);
    });
  });

  function updateCountBadge(status) {
    const badge = document.querySelector(`[data-count-badge="${status}"]`);
    if (badge) {
      const n = parseInt(badge.textContent || '0');
      badge.textContent = Math.max(0, n - 1);
    }
  }

  // ── Inline price edit ──
  document.querySelectorAll('.price-edit-toggle').forEach(btn => {
    btn.addEventListener('click', function () {
      const wrap = this.closest('.order-price-wrap');
      const display = wrap.querySelector('.price-display');
      const editWrap = wrap.querySelector('.order-price-edit');
      if (display && editWrap) {
        display.style.display = 'none';
        editWrap.style.display = 'flex';
        const inp = editWrap.querySelector('input');
        if (inp) inp.focus();
      }
    });
  });

  document.querySelectorAll('.price-save-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const wrap = this.closest('.order-price-wrap');
      const form = wrap.querySelector('form');
      if (!form) return;
      const orderId = btn.dataset.orderId;
      const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
      const priceInput = form.querySelector('input[name=price]');
      if (!priceInput || !csrf) return;

      fetch(`/admin-panel/orders/${orderId}/price/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrf.value,
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: `price=${priceInput.value}`
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            const display = wrap.querySelector('.price-display');
            const editWrap = wrap.querySelector('.order-price-edit');
            if (display) {
              display.textContent = 'Rp ' + Number(data.price).toLocaleString('id-ID');
              display.style.display = '';
            }
            if (editWrap) editWrap.style.display = 'none';
          }
        })
        .catch(console.error);
    });
  });

  // ── Delete confirmation modal ──
  const deleteModal = document.getElementById('deleteModal');
  const deleteForm = document.getElementById('deleteForm');
  const deleteModalTitle = document.getElementById('deleteModalTitle');
  const deleteModalText = document.getElementById('deleteModalText');

  document.querySelectorAll('[data-delete-url]').forEach(btn => {
    btn.addEventListener('click', function () {
      const url = this.dataset.deleteUrl;
      const name = this.dataset.deleteName || 'item ini';
      if (deleteForm) deleteForm.action = url;
      if (deleteModalTitle) deleteModalTitle.textContent = `Hapus ${name}?`;
      if (deleteModalText) deleteModalText.textContent = `Yakin ingin menghapus "${name}"? Tindakan ini tidak dapat dibatalkan.`;
      openModal(deleteModal);
    });
  });

  document.getElementById('deleteCancelBtn') && document.getElementById('deleteCancelBtn').addEventListener('click', () => closeModal(deleteModal));
  deleteModal && deleteModal.addEventListener('click', function (e) {
    if (e.target === deleteModal) closeModal(deleteModal);
  });

  function openModal(modal) {
    if (modal) {
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }
  function closeModal(modal) {
    if (modal) {
      modal.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  // ── Dynamic product detail rows ──
  const detailContainer = document.getElementById('detailsContainer');
  let detailCount = detailContainer ? detailContainer.querySelectorAll('.dynamic-detail-row').length : 0;

  document.getElementById('addDetailRow') && document.getElementById('addDetailRow').addEventListener('click', function () {
    if (!detailContainer) return;
    const row = document.createElement('div');
    row.className = 'dynamic-detail-row';
    row.innerHTML = `
      <input type="text" name="detail_${detailCount}-label" class="form-control" placeholder="Label">
      <textarea name="detail_${detailCount}-content" class="form-control" rows="2" placeholder="Deskripsi..."></textarea>
      <button type="button" class="btn-remove-row" onclick="this.closest('.dynamic-detail-row').remove()">✕</button>
    `;
    detailContainer.appendChild(row);
    detailCount++;
  });

  const pfContainer = document.getElementById('pfContainer');
  let pfCount = pfContainer ? pfContainer.querySelectorAll('.dynamic-pf-row').length : 0;

  document.getElementById('addPfRow') && document.getElementById('addPfRow').addEventListener('click', function () {
    if (!pfContainer) return;
    const row = document.createElement('div');
    row.className = 'dynamic-pf-row';
    row.innerHTML = `
      <input type="text" name="pf_${pfCount}-item" class="form-control" placeholder="Perfect for...">
      <button type="button" class="btn-remove-row" onclick="this.closest('.dynamic-pf-row').remove()">✕</button>
    `;
    pfContainer.appendChild(row);
    pfCount++;
  });

  // ── Management Website tabs ──
  document.querySelectorAll('.mw-tab').forEach(tab => {
    tab.addEventListener('click', function () {
      document.querySelectorAll('.mw-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.mw-tab-panel').forEach(p => p.classList.remove('active'));
      this.classList.add('active');
      const target = document.getElementById(this.dataset.tab);
      if (target) target.classList.add('active');
    });
  });

  // ── Auto-dismiss messages ──
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    });
  }, 4000);

  // ── Product auto-fill name from product select ──
  const productSelect = document.getElementById('id_product');
  const productNameInput = document.getElementById('id_product_name');
  const productPriceInput = document.getElementById('id_price');

  if (productSelect && productNameInput) {
    productSelect.addEventListener('change', function () {
      const opt = this.options[this.selectedIndex];
      if (opt && opt.value) {
        productNameInput.value = opt.text;
        const price = opt.dataset.price;
        if (price && productPriceInput) productPriceInput.value = price;
      }
    });
  }

  // Patch: add data-price to product options via dataset
  // (See template for select enrichment)
});
