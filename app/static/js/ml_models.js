document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.ml-form');
    const xColumn = form.querySelector('select[name="x_column"]');
    const yColumn = form.querySelector('select[name="y_column"]');
    const submit = form.querySelector('button[type="submit"]');

    // Prevent same column for X and Y
    function validateXY() {
        if (xColumn.value && yColumn.value && xColumn.value === yColumn.value) {
            alert("X and Y columns must be different.");
            return false;
        }
        return true;
    }

    form.addEventListener('submit', (e) => {
        if (!validateXY()) {
            e.preventDefault();
        } else {
            submit.disabled = true;
            submit.textContent = 'Running...';
        }
    });
});
