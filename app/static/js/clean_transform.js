document.addEventListener("DOMContentLoaded", function () {
    console.log("Clean & Transform page loaded.");

    // Example: Highlight all form sections on focus
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(input => {
        input.addEventListener('focus', () => {
            input.closest('.form-section').style.borderColor = '#0284c7';
        });
        input.addEventListener('blur', () => {
            input.closest('.form-section').style.borderColor = '#0c4a6e';
        });
    });
}); 
