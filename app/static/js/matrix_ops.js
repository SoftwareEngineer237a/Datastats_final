// static/js/matrix_ops.js
document.addEventListener('DOMContentLoaded', () => {
  const methodSelect = document.getElementById('method');
  const corrBlock   = document.querySelector('.method-correlation');
  const covBlock    = document.querySelector('.method-covariance');
  const form        = document.querySelector('.matrix-form');
  const runBtn      = document.querySelector('.btn-run');

  function toggleBlocks() {
    const m = methodSelect.value;
    corrBlock.style.display = (m === 'correlation') ? 'block' : 'none';
    covBlock.style.display  = (m === 'covariance')  ? 'block' : 'none';
  }

  methodSelect.addEventListener('change', toggleBlocks);
  toggleBlocks();

  // Basic validation: at least 2 columns selected
  form.addEventListener('submit', (e) => {
    const checked = form.querySelectorAll('input[name="columns"]:checked');
    if (checked.length < 2) {
      e.preventDefault();
      showNotice('Please select at least two numeric columns.');
      return;
    }
    // Disable button while running
    runBtn.disabled = true;
    runBtn.textContent = 'Computing...';
  });

  function showNotice(msg) {
    let n = document.querySelector('.matrix-notice');
    if (!n) {
      n = document.createElement('div');
      n.className = 'matrix-notice';
      n.style.cssText = 'position:fixed;top:16px;right:16px;background:#0ea5e9;color:#fff;padding:10px 14px;border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.15);z-index:10000;font:500 14px system-ui;';
      document.body.appendChild(n);
    }
    n.textContent = msg;
    setTimeout(() => { if (n) n.remove(); }, 3200);
  }
});
