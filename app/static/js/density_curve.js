/**
 * Density Curve Professional Enhancement Script
 * Modern, responsive, and user-friendly interactions
 */

class DensityCurveManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFormValidation();
        this.enhanceUserInteractions();
        console.log('Density Curve Manager initialized');
    }

    setupEventListeners() {
        // Form submission enhancement
        const form = document.querySelector('.density-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Download button functionality
        const downloadBtn = document.getElementById('download-btn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.downloadChart());
        }

        // Real-time color preview
        const colorInput = document.getElementById('color');
        if (colorInput) {
            colorInput.addEventListener('input', (e) => this.updateColorPreview(e));
        }

        // Column selection enhancement
        const columnSelect = document.getElementById('column');
        if (columnSelect) {
            columnSelect.addEventListener('change', (e) => this.handleColumnChange(e));
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }

    setupFormValidation() {
        const form = document.querySelector('.density-form');
        const submitBtn = form?.querySelector('button[type="submit"]');
        
        if (form && submitBtn) {
            const inputs = form.querySelectorAll('select, input[required]');
            
            inputs.forEach(input => {
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => {
                    this.clearFieldError(input);
                    this.updateSubmitButtonState(form, submitBtn);
                });
            });
            
            this.updateSubmitButtonState(form, submitBtn);
        }
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        if (field.required && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        }

        if (!isValid) {
            this.showFieldError(field, errorMessage);
        } else {
            this.clearFieldError(field);
        }

        return isValid;
    }

    showFieldError(field, message) {
        this.clearFieldError(field);
        
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            display: block;
            color: #dc2626;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        `;
        
        field.parentNode.appendChild(errorDiv);
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
    }

    updateSubmitButtonState(form, submitBtn) {
        const requiredFields = form.querySelectorAll('select[required], input[required]');
        const allValid = Array.from(requiredFields).every(field => field.value.trim() !== '');
        
        submitBtn.disabled = !allValid;
        submitBtn.style.opacity = allValid ? '1' : '0.6';
        submitBtn.style.cursor = allValid ? 'pointer' : 'not-allowed';
    }

    async handleFormSubmit(e) {
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const requiredFields = form.querySelectorAll('select[required], input[required]');
        
        // Validate all fields
        const allValid = Array.from(requiredFields).every(field => this.validateField(field));
        
        if (!allValid) {
            e.preventDefault();
            this.showToast('Please fill in all required fields correctly.', 'error');
            return;
        }

        // Add loading state
        this.setLoadingState(submitBtn, true);
        
        // Simulate processing for better UX
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Form will submit normally after this
    }

    setLoadingState(button, isLoading) {
        if (isLoading) {
            button.disabled = true;
            button.classList.add('loading');
            button.innerHTML = `
                <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                Generating...
            `;
        } else {
            button.disabled = false;
            button.classList.remove('loading');
            button.innerHTML = 'Generate Density Curve';
        }
    }

    downloadChart() {
        const img = document.getElementById('density-img');
        if (!img) {
            this.showToast('No chart available to download.', 'error');
            return;
        }

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const imgElement = new Image();
        
        imgElement.onload = () => {
            canvas.width = imgElement.width;
            canvas.height = imgElement.height;
            ctx.drawImage(imgElement, 0, 0);
            
            canvas.toBlob((blob) => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                const columnName = document.querySelector('h3 strong')?.textContent || 'density_curve';
                const timestamp = new Date().toISOString().slice(0, 19).replace(/[:]/g, '-');
                
                a.href = url;
                a.download = `density_curve_${columnName}_${timestamp}.png`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                this.showToast('Chart downloaded successfully!', 'success');
            });
        };
        
        imgElement.src = img.src;
    }

    updateColorPreview(e) {
        const color = e.target.value;
        // You could add real-time preview functionality here
        // For example, updating a preview element or the form border
        const form = document.querySelector('.density-form');
        if (form) {
            form.style.borderLeftColor = color;
        }
    }

    handleColumnChange(e) {
        const selectedValue = e.target.value;
        if (selectedValue) {
            this.showToast(`Selected column: ${selectedValue}`, 'info');
        }
    }

    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = document.querySelector('.density-form');
            if (form) {
                form.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        }
        
        // Ctrl/Cmd + S to download when results are shown
        if ((e.ctrlKey || e.metaKey) && e.key === 's' && document.getElementById('download-btn')) {
            e.preventDefault();
            this.downloadChart();
        }
    }

    showToast(message, type = 'info') {
        // Remove existing toasts
        const existingToasts = document.querySelectorAll('.custom-toast');
        existingToasts.forEach(toast => toast.remove());

        const toast = document.createElement('div');
        const typeStyles = {
            success: { background: '#10b981', icon: '✅' },
            error: { background: '#dc2626', icon: '❌' },
            info: { background: '#3b82f6', icon: 'ℹ️' },
            warning: { background: '#f59e0b', icon: '⚠️' }
        };

        const style = typeStyles[type] || typeStyles.info;

        toast.className = 'custom-toast';
        toast.innerHTML = `
            <span class="toast-icon">${style.icon}</span>
            <span class="toast-message">${message}</span>
        `;

        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${style.background};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 10000;
            font-weight: 500;
            animation: slideInRight 0.3s ease-out;
            max-width: 400px;
        `;

        document.body.appendChild(toast);

        // Auto remove after 4 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideOutRight 0.3s ease-in';
                setTimeout(() => toast.remove(), 300);
            }
        }, 4000);
    }

    enhanceUserInteractions() {
        // Add smooth scrolling to results
        const form = document.querySelector('.density-form');
        if (form && document.querySelector('#density-img')) {
            form.scrollIntoView({ behavior: 'smooth' });
        }

        // Add image zoom functionality
        const densityImg = document.getElementById('density-img');
        if (densityImg) {
            densityImg.style.cursor = 'zoom-in';
            densityImg.addEventListener('click', () => this.toggleImageZoom(densityImg));
        }
    }

    toggleImageZoom(img) {
        if (img.style.transform === 'scale(1.5)') {
            img.style.transform = 'scale(1)';
            img.style.cursor = 'zoom-in';
        } else {
            img.style.transform = 'scale(1.5)';
            img.style.cursor = 'zoom-out';
        }
    }
}

// Add CSS animations for toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .spinner-border {
        display: inline-block;
        width: 1rem;
        height: 1rem;
        vertical-align: text-bottom;
        border: 0.2em solid currentColor;
        border-right-color: transparent;
        border-radius: 50%;
        animation: spinner-border .75s linear infinite;
    }
    
    .visually-hidden {
        position: absolute !important;
        width: 1px !important;
        height: 1px !important;
        padding: 0 !important;
        margin: -1px !important;
        overflow: hidden !important;
        clip: rect(0,0,0,0) !important;
        white-space: nowrap !important;
        border: 0 !important;
    }
`;
document.head.appendChild(style);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DensityCurveManager();
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DensityCurveManager;
}