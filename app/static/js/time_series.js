// static/js/time_series.js
document.addEventListener('DOMContentLoaded', () => {
  const methodSelect = document.getElementById('method-select');
  const methodBlocks = document.querySelectorAll('.method');

  function showMethodBlock() {
    const val = methodSelect.value;
    methodBlocks.forEach(b => b.style.display = 'none');
    if (!val) return;
    const block = document.querySelector(`.method-${val}`);
    if (block) block.style.display = 'block';
  }

  methodSelect.addEventListener('change', showMethodBlock);
  showMethodBlock();

  // Disable submit button while running
  const form = document.querySelector('.ts-form');
  const runBtn = document.querySelector('.btn-run');
  form.addEventListener('submit', () => {
    runBtn.disabled = true;
    runBtn.textContent = 'Running...';
  });

  // ========== IMAGE DOWNLOAD FUNCTIONALITY ==========
  document.querySelectorAll('.download-img-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const imgId = this.getAttribute('data-target');
      const img = document.getElementById(imgId);
      
      if (!img) {
        console.error('Image not found:', imgId);
        return;
      }

      // Create a temporary link element
      const link = document.createElement('a');
      
      // Get the method name for better filename
      const methodName = methodSelect.value || 'timeseries';
      link.download = `${methodName}_analysis_datastats.png`;
      link.href = img.src;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Visual feedback
      const originalText = this.textContent;
      this.textContent = '✓ Downloaded!';
      this.style.background = 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)';
      this.style.color = 'white';
      
      setTimeout(() => {
        this.textContent = originalText;
        this.style.background = '';
        this.style.color = '';
      }, 2000);
    });
  });

  // Add smooth scroll to results when they appear
  const resultsSection = document.querySelector('.results');
  if (resultsSection) {
    resultsSection.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'start' 
    });
    
    // Add entrance animation
    const plotImg = document.getElementById('ts-plot-img');
    if (plotImg) {
      plotImg.style.opacity = '0';
      plotImg.style.transform = 'translateY(20px)';
      setTimeout(() => {
        plotImg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        plotImg.style.opacity = '1';
        plotImg.style.transform = 'translateY(0)';
      }, 100);
    }
  }
});