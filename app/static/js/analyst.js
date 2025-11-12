// analyst.js - Interactive dashboard enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Stat card hover effect (for touch devices)
    document.querySelectorAll('.stat-card').forEach(function(card) {
        card.addEventListener('touchstart', function() {
            card.classList.add('hovered');
        });
        card.addEventListener('touchend', function() {
            card.classList.remove('hovered');
        });
    });

    // Animate stat numbers (if desired, can be extended)
    document.querySelectorAll('.stat-card strong').forEach(function(el) {
        const target = parseInt(el.textContent.replace(/\D/g, ''));
        if (!isNaN(target)) {
            let count = 0;
            const step = Math.ceil(target / 30);
            const interval = setInterval(() => {
                count += step;
                if (count >= target) {
                    el.textContent = target;
                    clearInterval(interval);
                } else {
                    el.textContent = count;
                }
            }, 20);
        }
    });

    // Button ripple effect
    document.querySelectorAll('.btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            let ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = (e.clientX - btn.getBoundingClientRect().left) + 'px';
            ripple.style.top = (e.clientY - btn.getBoundingClientRect().top) + 'px';
            btn.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
});

// Ripple effect CSS (inject if not present)
if (!document.getElementById('ripple-style')) {
    const style = document.createElement('style');
    style.id = 'ripple-style';
    style.textContent = `
    .btn { position: relative; overflow: hidden; }
    .ripple {
        position: absolute;
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
        background: rgba(59,130,246,0.25);
        pointer-events: none;
        width: 100px;
        height: 100px;
        left: 50%;
        top: 50%;
        margin-left: -50px;
        margin-top: -50px;
    }
    @keyframes ripple {
        to {
            transform: scale(2.5);
            opacity: 0;
        }
    }
    `;
    document.head.appendChild(style);
}
// Smooth scroll, alerts, or interactive components can be added here.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Analyst layout ready.");
});
