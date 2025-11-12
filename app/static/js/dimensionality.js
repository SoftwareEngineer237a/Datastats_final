document.addEventListener("DOMContentLoaded", () => {
    const methodSelect = document.getElementById('method-select');
    
    // Listen to download buttons
    document.querySelectorAll('.download-img-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const imgId = btn.getAttribute('data-target');
            const img = document.getElementById(imgId);
            if (!img) return;

            const link = document.createElement('a');
            link.download = imgId + "_datastats.png";
            link.href = img.src;
            link.click();
        });
    });
});