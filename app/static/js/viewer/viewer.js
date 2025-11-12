// Basic interactivity for the Viewer layout
document.addEventListener("DOMContentLoaded", () => {
    console.log("Viewer layout loaded ✅");

    // Highlight active menu item
    const currentUrl = window.location.href;
    document.querySelectorAll(".menu-item").forEach(item => {
        if (currentUrl.includes(item.getAttribute("href"))) {
            item.classList.add("active");
            item.style.background = "rgba(255,255,255,0.25)";
        }
    });
});
