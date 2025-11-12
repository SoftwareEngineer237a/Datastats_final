// Inferential Statistics Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.inferential-form');
    const submitBtn = document.querySelector('.btn-submit');
    const columnSelect = document.querySelector('select[name="column"]');
    const popmeanInput = document.querySelector('input[name="popmean"]');
    const confidenceSelect = document.querySelector('select[name="confidence"]');

    // Form validation
    function validateForm() {
        let isValid = true;
        const errors = [];

        // Check if column is selected
        if (!columnSelect.value) {
            errors.push('Please select a numerical column');
            columnSelect.style.borderColor = '#dc2626';
            isValid = false;
        } else {
            columnSelect.style.borderColor = '#bfdbfe';
        }

        // Check if population mean is provided
        if (!popmeanInput.value || isNaN(parseFloat(popmeanInput.value))) {
            errors.push('Please enter a valid population mean');
            popmeanInput.style.borderColor = '#dc2626';
            isValid = false;
        } else {
            popmeanInput.style.borderColor = '#bfdbfe';
        }

        // Display errors if any
        if (errors.length > 0) {
            showNotification(errors.join('<br>'), 'error');
        }

        return isValid;
    }

    // Form submission handler
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            return;
        }

        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.textContent = 'Calculating...';
        submitBtn.disabled = true;

        // Add smooth scrolling to results (if they exist)
        setTimeout(() => {
            const resultsSection = document.querySelector('h3');
            if (resultsSection) {
                resultsSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }, 100);
    });

    // Real-time input validation
    columnSelect.addEventListener('change', function() {
        if (this.value) {
            this.style.borderColor = '#3b82f6';
            showFieldSuccess(this);
        }
    });

    popmeanInput.addEventListener('input', function() {
        if (this.value && !isNaN(parseFloat(this.value))) {
            this.style.borderColor = '#3b82f6';
            showFieldSuccess(this);
        } else {
            this.style.borderColor = '#dc2626';
        }
    });

    // Add tooltips to form elements
    addTooltips();

    // Highlight numerical results
    highlightNumbers();

    // Add interactive hover effects to result items
    addResultHoverEffects();

    // Auto-focus on first empty field
    autoFocusFirstEmptyField();
});

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = message;
    
    // Notification styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        max-width: 300px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: slideIn 0.3s ease-out;
    `;

    if (type === 'error') {
        notification.style.backgroundColor = '#dc2626';
        notification.style.borderLeft = '4px solid #b91c1c';
    } else if (type === 'success') {
        notification.style.backgroundColor = '#059669';
        notification.style.borderLeft = '4px solid #047857';
    } else {
        notification.style.backgroundColor = '#3b82f6';
        notification.style.borderLeft = '4px solid #2563eb';
    }

    document.body.appendChild(notification);

    // Auto remove after 4 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }
    }, 4000);
}

// Add success indicator to fields
function showFieldSuccess(field) {
    // Remove existing success indicator
    const existingIndicator = field.parentNode.querySelector('.success-indicator');
    if (existingIndicator) {
        existingIndicator.remove();
    }

    const indicator = document.createElement('span');
    indicator.className = 'success-indicator';
    indicator.innerHTML = '✓';
    indicator.style.cssText = `
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        color: #059669;
        font-weight: bold;
        font-size: 18px;
    `;

    field.parentNode.style.position = 'relative';
    field.parentNode.appendChild(indicator);

    // Remove after 2 seconds
    setTimeout(() => {
        if (indicator.parentNode) {
            indicator.remove();
        }
    }, 2000);
}

// Highlight numerical results
function highlightNumbers() {
    const resultElements = document.querySelectorAll('ul li');
    resultElements.forEach(element => {
        const text = element.innerHTML;
        // Highlight numbers (including decimals and negative numbers)
        const highlightedText = text.replace(
            /(-?\d+\.?\d*(?:e[+-]?\d+)?)/g, 
            '<span class="highlight-number">$1</span>'
        );
        element.innerHTML = highlightedText;
    });
}

// Add hover effects to result items
function addResultHoverEffects() {
    const resultItems = document.querySelectorAll('ul li');
    resultItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
            this.style.backgroundColor = '#f0f9ff';
            this.style.transition = 'all 0.2s ease';
            this.style.borderRadius = '6px';
            this.style.padding = '10px 15px';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
            this.style.backgroundColor = 'transparent';
            this.style.padding = '10px 0';
        });
    });
}

// Auto-focus on first empty required field
function autoFocusFirstEmptyField() {
    const requiredFields = document.querySelectorAll('[required]');
    for (let field of requiredFields) {
        if (!field.value) {
            field.focus();
            break;
        }
    }
}

// Add animation styles
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .pulse {
            animation: pulse 2s infinite;
        }
    `;
    document.head.appendChild(style);
}

// Initialize animation styles
addAnimationStyles();

// Copy result to clipboard functionality
// function addCopyToClipboard() {
//     const results = document.querySelectorAll('ul');
//     results.forEach((ul, index) => {
//         const copyBtn = document.createElement('button');
//         copyBtn.innerHTML = '📋 Copy Results';
//         copyBtn.className = 'copy-btn';
//         copyBtn.style.cssText = `
//             background: #f0f9ff;
//             border: 1px solid #3b82f6;
//             color: #1e40af;
//             padding: 8px 15px;
//             border-radius: 6px;
//             font-size: 12px;
//             cursor: pointer;
//             margin-top: 10px;
//             transition: all 0.2s ease;
//         `;

//         copyBtn.addEventListener('click', function() {
//             const text = Array.from(ul.querySelectorAll('li'))
//                 .map(li => li.textContent.trim())
//                 .join('\n');
            
//             navigator.clipboard.writeText(text).then(() => {
//                 showNotification('Results copied to clipboard!', 'success');
//                 this.innerHTML = '✓ Copied!';
//                 this.style.backgroundColor = '#dcfce7';
//                 this.style.borderColor = '#22c55e';
//                 this.style.color = '#15803d';
                
//                 setTimeout(() => {
//                     this.innerHTML = '📋 Copy Results';
//                     this.style.backgroundColor = '#f0f9ff';
//                     this.style.borderColor = '#3b82f6';
//                     this.style.color = '#1e40af';
//                 }, 2000);
//             });
//         });

//         copyBtn.addEventListener('mouseenter', function() {
//             this.style.backgroundColor = '#dbeafe';
//             this.style.transform = 'translateY(-1px)';
//         });

//         copyBtn.addEventListener('mouseleave', function() {
//             this.style.backgroundColor = '#f0f9ff';
//             this.style.transform = 'translateY(0)';
//         });

//         ul.appendChild(copyBtn);
//     });
// }

// Initialize copy to clipboard functionality when results are present
if (document.querySelector('ul')) {
    addCopyToClipboard();
}