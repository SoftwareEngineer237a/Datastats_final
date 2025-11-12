// Modern Bank Registration Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Initialize the registration form
    const form = document.querySelector('form');
    const inputs = document.querySelectorAll('.form-input');
    const submitButton = document.querySelector('.btn-submit');
    const passwordInput = document.querySelector('#password');
    const confirmPasswordInput = document.querySelector('#confirm_password');
    
    // Password strength configuration
    const passwordStrengthConfig = {
        minLength: 8,
        requireUppercase: true,
        requireLowercase: true,
        requireNumbers: true,
        requireSpecialChars: true
    };
    
    // Animation and interaction handlers
    initializeAnimations();
    initializeFormValidation();
    initializePasswordStrength();
    initializeFormSubmission();
    initializeAccessibility();
    
    /**
     * Initialize smooth animations and interactions
     */
    function initializeAnimations() {
        // Stagger form field animations
        inputs.forEach((input, index) => {
            input.parentElement.style.animationDelay = `${index * 0.1}s`;
        });
        
        // Add floating label effect
        inputs.forEach(input => {
            // Create floating label if input has placeholder
            if (input.placeholder) {
                createFloatingLabel(input);
            }
            
            // Add focus and blur animations
            input.addEventListener('focus', handleInputFocus);
            input.addEventListener('blur', handleInputBlur);
            input.addEventListener('input', handleInputChange);
        });
        
        // Add hover effects to form wrapper
        const formWrapper = document.querySelector('.form-wrapper');
        formWrapper.addEventListener('mouseenter', () => {
            formWrapper.style.transform = 'translateY(-2px)';
        });
        
        formWrapper.addEventListener('mouseleave', () => {
            formWrapper.style.transform = 'translateY(0)';
        });
    }
    
    /**
     * Create floating label for input fields
     */
    function createFloatingLabel(input) {
        const label = input.previousElementSibling;
        if (!label || label.tagName !== 'LABEL') return;
        
        const originalText = label.textContent;
        
        input.addEventListener('focus', () => {
            label.style.transform = 'translateY(-25px) scale(0.85)';
            label.style.color = 'var(--secondary-color)';
        });
        
        input.addEventListener('blur', () => {
            if (!input.value) {
                label.style.transform = 'translateY(0) scale(1)';
                label.style.color = 'var(--text-primary)';
            }
        });
        
        // Check initial state
        if (input.value) {
            label.style.transform = 'translateY(-25px) scale(0.85)';
            label.style.color = 'var(--secondary-color)';
        }
    }
    
    /**
     * Handle input focus events
     */
    function handleInputFocus(event) {
        const input = event.target;
        const formGroup = input.closest('.form-group');
        
        // Add focus class for styling
        formGroup.classList.add('focused');
        
        // Create ripple effect
        createRippleEffect(input);
        
        // Show input hints if needed
        showInputHints(input);
    }
    
    /**
     * Handle input blur events
     */
    function handleInputBlur(event) {
        const input = event.target;
        const formGroup = input.closest('.form-group');
        
        // Remove focus class
        formGroup.classList.remove('focused');
        
        // Validate input
        validateInput(input);
        
        // Hide input hints
        hideInputHints(input);
    }
    
    /**
     * Handle input change events
     */
    function handleInputChange(event) {
        const input = event.target;
        
        // Real-time validation
        validateInput(input);
        
        // Update password strength if it's a password field
        if (input.type === 'password' && input.id === 'password') {
            updatePasswordStrength(input.value);
        }
        
        // Check password confirmation
        if (input.id === 'confirm_password' || input.id === 'password') {
            checkPasswordMatch();
        }
        
        // Auto-resize text areas (if any)
        if (input.tagName === 'TEXTAREA') {
            autoResizeTextarea(input);
        }
    }
    
    /**
     * Create ripple effect on input focus
     */
    function createRippleEffect(input) {
        const ripple = document.createElement('div');
        ripple.className = 'input-ripple';
        
        // Style the ripple
        Object.assign(ripple.style, {
            position: 'absolute',
            top: '0',
            left: '0',
            width: '100%',
            height: '100%',
            background: 'rgba(74, 144, 226, 0.1)',
            borderRadius: 'var(--border-radius)',
            transform: 'scale(0)',
            transition: 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
            pointerEvents: 'none',
            zIndex: '-1'
        });
        
        // Add to input container
        const container = input.parentElement;
        container.style.position = 'relative';
        container.appendChild(ripple);
        
        // Animate ripple
        requestAnimationFrame(() => {
            ripple.style.transform = 'scale(1)';
        });
        
        // Remove ripple after animation
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }
    
    /**
     * Initialize form validation
     */
    function initializeFormValidation() {
        // Add real-time validation to all inputs
        inputs.forEach(input => {
            input.addEventListener('input', debounce(() => validateInput(input), 300));
            input.addEventListener('blur', () => validateInput(input));
        });
        
        // Custom validation rules
        const validationRules = {
            name: {
                required: true,
                minLength: 2,
                pattern: /^[a-zA-Z\s]+$/,
                message: 'Name must contain only letters and spaces'
            },
            email: {
                required: true,
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Please enter a valid email address'
            },
            password: {
                required: true,
                minLength: 8,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
                message: 'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
            },
            confirm_password: {
                required: true,
                match: 'password',
                message: 'Passwords do not match'
            },
            role: {
                required: true,
                message: 'Please select a role'
            }
        };
        
        // Store validation rules globally
        window.validationRules = validationRules;
    }
    
    /**
     * Validate individual input
     */
    function validateInput(input) {
        const rules = window.validationRules[input.name];
        if (!rules) return true;
        
        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';
        
        // Required validation
        if (rules.required && !value) {
            isValid = false;
            errorMessage = `${input.name.charAt(0).toUpperCase() + input.name.slice(1)} is required`;
        }
        
        // Min length validation
        if (isValid && rules.minLength && value.length < rules.minLength) {
            isValid = false;
            errorMessage = `${input.name.charAt(0).toUpperCase() + input.name.slice(1)} must be at least ${rules.minLength} characters`;
        }
        
        // Pattern validation
        if (isValid && rules.pattern && !rules.pattern.test(value)) {
            isValid = false;
            errorMessage = rules.message;
        }
        
        // Match validation (for password confirmation)
        if (isValid && rules.match) {
            const matchInput = document.querySelector(`#${rules.match}`);
            if (matchInput && value !== matchInput.value) {
                isValid = false;
                errorMessage = rules.message;
            }
        }
        
        // Update UI based on validation result
        updateInputValidationUI(input, isValid, errorMessage);
        
        return isValid;
    }
    
    /**
     * Update input validation UI
     */
    function updateInputValidationUI(input, isValid, errorMessage) {
        const formGroup = input.closest('.form-group');
        const existingError = formGroup.querySelector('.error-message');
        
        // Remove existing error message
        if (existingError) {
            existingError.remove();
        }
        
        // Update input classes
        input.classList.remove('valid', 'invalid');
        input.classList.add(isValid ? 'valid' : 'invalid');
        
        // Add error message if invalid
        if (!isValid && errorMessage) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = errorMessage;
            
            // Style error message
            Object.assign(errorDiv.style, {
                color: 'var(--error-color)',
                fontSize: '0.85em',
                marginTop: '5px',
                animation: 'slideInDown 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
            });
            
            formGroup.appendChild(errorDiv);
        }
    }
    
    /**
     * Initialize password strength indicator
     */
    function initializePasswordStrength() {
        if (!passwordInput) return;
        
        // Create password strength indicator
        const strengthContainer = document.createElement('div');
        strengthContainer.className = 'password-strength';
        
        const strengthBar = document.createElement('div');
        strengthBar.className = 'password-strength-bar';
        
        const strengthText = document.createElement('div');
        strengthText.className = 'password-strength-text';
        strengthText.style.cssText = `
            font-size: 0.8em;
            margin-top: 5px;
            font-weight: 500;
            transition: var(--transition);
        `;
        
        strengthContainer.appendChild(strengthBar);
        
        // Insert after password input
        passwordInput.parentElement.appendChild(strengthContainer);
        passwordInput.parentElement.appendChild(strength);
    }
})