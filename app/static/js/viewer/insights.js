document.addEventListener("DOMContentLoaded", () => {
    console.log("Insights page ready ✅");

    // Animate highlight card numbers (e.g., weekly activity)
    document.querySelectorAll(".highlight p").forEach(el => {
        const finalValue = parseInt(el.textContent);
        let current = 0;

        const step = finalValue / 30;
        const interval = setInterval(() => {
            current += step;
            if (current >= finalValue) {
                el.textContent = finalValue;
                clearInterval(interval);
            } else {
                el.textContent = Math.floor(current);
            }
        }, 30);
    });

    // Hover animation on graph images
    document.querySelectorAll(".graph-preview img").forEach(img => {
        img.addEventListener("mouseover", () => img.style.transform = "scale(1.06)");
        img.addEventListener("mouseout", () => img.style.transform = "scale(1)");
        img.style.transition = "all .2s ease";
    });

    // Future: track recommended graph clicks
    document.querySelectorAll(".graph-preview").forEach(item => {
        item.addEventListener("click", () => {
            console.log("Graph clicked:", item.innerText);
            // TODO: send click data to backend for recommendations
        });
    });
});
