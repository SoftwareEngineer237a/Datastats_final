// Regression Analysis Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.regression-form');
    const modelTypeSelect = document.querySelector('select[name="model_type"]');
    const degreeInput = document.querySelector('input[name="degree"]');
    const xColumnSelect = document.querySelector('select[name="x_column"]');
    const yColumnSelect = document.querySelector('select[name="y_column"]');
    const submitButton = document.querySelector('button[type="submit"]');

    // 📌 Toggle degree input visibility
    function toggleDegreeInput() {
        if (modelTypeSelect.value === 'polynomial') {
            degreeInput.closest('label').style.display = 'block';
            degreeInput.previousElementSibling.style.display = 'block';
            degreeInput.required = true;
        } else {
            degreeInput.closest('label').style.display = 'none';
            degreeInput.previousElementSibling.style.display = 'none';
            degreeInput.required = false;
        }
    }

    // 📌 Toggle Y column selection mode (single vs multiple)
    function toggleYSelection() {
        if (modelTypeSelect.value === 'multiple_linear') {
            yColumnSelect.setAttribute('multiple', 'multiple');
            yColumnSelect.size = 6; // show more rows
        } else {
            yColumnSelect.removeAttribute('multiple');
            yColumnSelect.size = 1;
        }
    }

    // Initial state
    toggleDegreeInput();
    toggleYSelection();

    // Event listeners
    modelTypeSelect.addEventListener('change', () => {
        toggleDegreeInput();
        toggleYSelection();
    });

    // 📌 Prevent selecting same column for X and Y
    function validateColumnSelection() {
        const xValue = xColumnSelect.value;
        const selectedYs = Array.from(yColumnSelect.selectedOptions).map(opt => opt.value);

        if (xValue && selectedYs.includes(xValue)) {
            alert('X and Y columns must be different. Please select different columns.');
            return false;
        }
        return true;
    }

    xColumnSelect.addEventListener('change', validateColumnSelection);
    yColumnSelect.addEventListener('change', validateColumnSelection);

    // 📌 Form submission
    form.addEventListener('submit', function(e) {
        if (!validateColumnSelection()) {
            e.preventDefault();
            return false;
        }

        const originalText = submitButton.textContent;
        submitButton.textContent = 'Running Analysis...';
        submitButton.disabled = true;
        submitButton.style.background = 'linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%)';
        submitButton.style.cursor = 'not-allowed';
    });

    // 📌 Validation for polynomial degree
    degreeInput.addEventListener('input', function() {
        const value = parseInt(this.value);
        if (value < 2 || value > 10) {
            this.setCustomValidity('Degree must be between 2 and 10');
        } else {
            this.setCustomValidity('');
        }
    });

    // 📌 Highlight valid/invalid input
    const formInputs = form.querySelectorAll('select, input');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 6px rgba(52,152,219,0.5)';
        });
        input.addEventListener('blur', function() {
            this.style.boxShadow = 'none';
        });
        input.addEventListener('change', function() {
            this.style.borderColor = this.checkValidity() ? '#27ae60' : '#e74c3c';
        });
    });

    // 📌 Smooth scroll to results
    const resultSection = document.querySelector('h3');
    if (resultSection) {
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // 📌 Tooltips for model types
    const tooltips = {
        'linear': 'Best for straight-line relationships between variables',
        'polynomial': 'Good for curved or non-linear patterns in your data',
        'logistic': 'Used for binary predictions (yes/no, true/false outcomes)',
        'ridge': 'Linear regression with regularization to prevent overfitting',
        'lasso': 'Linear regression that can automatically select important features',
        'multiple_linear': 'Allows one X variable to predict multiple Y variables simultaneously'
    };

    const tooltip = document.createElement('div');
    tooltip.className = 'model-tooltip';
    tooltip.style.cssText = `
        position: absolute;
        background: #2c3e50;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.9rem;
        max-width: 300px;
        z-index: 1000;
        display: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        pointer-events: none;
    `;
    document.body.appendChild(tooltip);

    modelTypeSelect.addEventListener('mousemove', function(e) {
        const selectedValue = this.value;
        if (selectedValue && tooltips[selectedValue]) {
            tooltip.textContent = tooltips[selectedValue];
            tooltip.style.display = 'block';
            tooltip.style.left = e.pageX + 10 + 'px';
            tooltip.style.top = e.pageY - 30 + 'px';
        } else {
            tooltip.style.display = 'none';
        }
    });

    modelTypeSelect.addEventListener('mouseleave', function() {
        tooltip.style.display = 'none';
    });

    // 📌 Animate result rows
    const resultsTable = document.querySelector('.table');
    if (resultsTable) {
        const rows = resultsTable.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.style.opacity = '0';
            row.style.transform = 'translateY(20px)';
            row.style.transition = `opacity 0.3s ease ${index * 0.1}s, transform 0.3s ease ${index * 0.1}s`;

            setTimeout(() => {
                row.style.opacity = '1';
                row.style.transform = 'translateY(0)';
            }, 100);
        });
    }
});
