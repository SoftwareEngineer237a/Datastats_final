// Clustering Analysis Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const form = document.querySelector('form');
    const algorithmSelect = document.getElementById('algorithmSelect');
    const kmeansOptions = document.getElementById('kmeans-options');
    const hacOptions = document.getElementById('hac-options');
    const submitButton = document.querySelector('.btn.btn-primary');
    const checkboxes = document.querySelectorAll('input[name="columns"]');
    
    // Create checkbox containers for better styling
    function createCheckboxContainers() {
        const checkboxContainer = document.createElement('div');
        checkboxContainer.className = 'checkbox-container';
        
        // Find the first checkbox and its parent
        const firstCheckbox = document.querySelector('input[name="columns"]');
        if (firstCheckbox) {
            const parent = firstCheckbox.parentNode;
            
            // Move all checkboxes to the new container
            checkboxes.forEach(checkbox => {
                const checkboxItem = document.createElement('div');
                checkboxItem.className = 'checkbox-item';
                
                // Clone the checkbox and its text
                const newCheckbox = checkbox.cloneNode(true);
                const label = document.createElement('label');
                label.textContent = checkbox.nextSibling.textContent.trim();
                label.setAttribute('for', newCheckbox.id || Math.random().toString(36).substr(2, 9));
                newCheckbox.id = label.getAttribute('for');
                
                checkboxItem.appendChild(newCheckbox);
                checkboxItem.appendChild(label);
                checkboxContainer.appendChild(checkboxItem);
                
                // Remove original checkbox and its br tag
                if (checkbox.nextSibling && checkbox.nextSibling.nodeType === Node.TEXT_NODE) {
                    checkbox.nextSibling.remove();
                }
                if (checkbox.nextSibling && checkbox.nextSibling.tagName === 'BR') {
                    checkbox.nextSibling.remove();
                }
                checkbox.remove();
            });
            
            // Insert the container after the label
            const label = parent.querySelector('label');
            if (label) {
                label.parentNode.insertBefore(checkboxContainer, label.nextSibling);
            }
        }
    }

    // Initialize checkbox containers
    createCheckboxContainers();

    // Algorithm selection toggle
    function toggleAlgorithmOptions() {
        const selectedAlgorithm = algorithmSelect.value;
        
        if (selectedAlgorithm === 'kmeans') {
            kmeansOptions.style.display = 'block';
            hacOptions.style.display = 'none';
            
            // Add smooth reveal animation
            kmeansOptions.style.opacity = '0';
            kmeansOptions.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                kmeansOptions.style.opacity = '1';
                kmeansOptions.style.transform = 'translateY(0)';
            }, 10);
        } else if (selectedAlgorithm === 'hac') {
            kmeansOptions.style.display = 'none';
            hacOptions.style.display = 'block';
            
            // Add smooth reveal animation
            hacOptions.style.opacity = '0';
            hacOptions.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                hacOptions.style.opacity = '1';
                hacOptions.style.transform = 'translateY(0)';
            }, 10);
        }
    }

    // Initial setup
    toggleAlgorithmOptions();

    // Add event listener for algorithm selection
    algorithmSelect.addEventListener('change', toggleAlgorithmOptions);

    // Checkbox selection validation
    function validateCheckboxSelection() {
        const checkedBoxes = document.querySelectorAll('input[name="columns"]:checked');
        const submitBtn = document.querySelector('.btn.btn-primary');
        
        if (checkedBoxes.length < 2) {
            submitBtn.disabled = true;
            submitBtn.style.background = 'linear-gradient(135deg, #bdc3c7 0%, #95a5a6 100%)';
            submitBtn.style.cursor = 'not-allowed';
            submitBtn.title = 'Please select at least 2 columns for clustering';
            return false;
        } else {
            submitBtn.disabled = false;
            submitBtn.style.background = 'linear-gradient(135deg, #e74c3c 0%, #f39c12 100%)';
            submitBtn.style.cursor = 'pointer';
            submitBtn.title = '';
            return true;
        }
    }

    // Add event listeners to all checkboxes
    document.addEventListener('change', function(e) {
        if (e.target.name === 'columns') {
            validateCheckboxSelection();
            
            // Visual feedback for checkbox selection
            const checkboxItem = e.target.closest('.checkbox-item');
            if (checkboxItem) {
                if (e.target.checked) {
                    checkboxItem.style.background = 'linear-gradient(135deg, rgba(231, 76, 60, 0.1) 0%, rgba(243, 156, 18, 0.1) 100%)';
                    checkboxItem.style.borderColor = 'rgba(231, 76, 60, 0.4)';
                    checkboxItem.style.transform = 'scale(1.02)';
                } else {
                    checkboxItem.style.background = 'rgba(255, 255, 255, 0.8)';
                    checkboxItem.style.borderColor = 'rgba(231, 76, 60, 0.1)';
                    checkboxItem.style.transform = 'scale(1)';
                }
            }
        }
    });

    // Initial validation
    validateCheckboxSelection();

    // Form submission handling
    form.addEventListener('submit', function(e) {
        // Validate checkbox selection
        if (!validateCheckboxSelection()) {
            e.preventDefault();
            alert('Please select at least 2 columns for clustering analysis.');
            return false;
        }

        // Show loading state
        const originalButtonText = submitButton.textContent;
        submitButton.textContent = 'Running Analysis...';
        submitButton.classList.add('form-loading');
        form.classList.add('form-loading');

        // Add loading animation
        submitButton.style.background = 'linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%)';
        submitButton.style.cursor = 'not-allowed';
    });

    // Number input validation
    const numberInput = document.querySelector('input[name="n_clusters"]');
    if (numberInput) {
        numberInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value < 2 || value > 10) {
                this.setCustomValidity('Number of clusters must be between 2 and 10');
                this.style.borderColor = '#e74c3c';
            } else {
                this.setCustomValidity('');
                this.style.borderColor = '#2ecc71';
            }
        });

        // Add increment/decrement buttons
        const numberContainer = document.createElement('div');
        numberContainer.style.position = 'relative';
        numberContainer.style.display = 'inline-block';
        numberContainer.style.width = '100%';
        
        numberInput.parentNode.insertBefore(numberContainer, numberInput);
        numberContainer.appendChild(numberInput);
        
        // Style the number input for better UX
        numberInput.style.paddingRight = '3rem';
    }

    // Enhanced form interaction with visual feedback
    const formInputs = form.querySelectorAll('select, input[type="number"]');
    formInputs.forEach(input => {
        // Add focus effects
        input.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
            this.style.boxShadow = '0 0 0 4px rgba(231, 76, 60, 0.2), 0 8px 25px rgba(231, 76, 60, 0.15)';
        });

        input.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = 'none';
        });

        // Add change validation
        input.addEventListener('change', function() {
            if (this.checkValidity()) {
                this.style.borderColor = '#2ecc71';
            } else {
                this.style.borderColor = '#e74c3c';
            }
        });
    });

    // Smooth scroll to results if they exist
    const resultSection = document.querySelector('h4');
    if (resultSection) {
        resultSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
        // Add entrance animation to results
        resultSection.classList.add('results-enter');
        
        // Animate images
        const images = document.querySelectorAll('.img-fluid');
        images.forEach((img, index) => {
            img.style.opacity = '0';
            img.style.transform = 'translateY(30px)';
            setTimeout(() => {
                img.style.opacity = '1';
                img.style.transform = 'translateY(0)';
            }, 300 + (index * 200));
        });
    }

    // Add tooltip functionality for algorithm types
    const algorithmTooltips = {
        'kmeans': 'K-Means clustering partitions data into k clusters where each observation belongs to the cluster with the nearest mean.',
        'hac': 'Hierarchical clustering creates a tree of clusters (dendrogram) that can be cut at different levels to get different numbers of clusters.'
    };

    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'algorithm-tooltip';
    tooltip.style.cssText = `
        position: absolute;
        background: #2c3e50;
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        display: none;
        max-width: 300px;
        font-size: 14px;
        line-height: 1.5;
    `;
    document.body.appendChild(tooltip);

    // Show tooltip on hover
    algorithmSelect.addEventListener('mouseover', function() {
        const selectedAlgorithm = algorithmSelect.value;
        tooltip.textContent = algorithmTooltips[selectedAlgorithm] || '';
        tooltip.style.display = 'block';
        const rect = algorithmSelect.getBoundingClientRect();
        tooltip.style.left = `${rect.left + window.scrollX}px`;
        tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
    });

    // Hide tooltip on mouseout
    algorithmSelect.addEventListener('mouseout', function() {
        tooltip.style.display = 'none';
    });

    // Responsive tooltip positioning
    window.addEventListener('resize', function() {
        if (tooltip.style.display === 'block') {
            const rect = algorithmSelect.getBoundingClientRect();
            tooltip.style.left = `${rect.left + window.scrollX}px`;
            tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
        }
    });

    // ========== IMAGE DOWNLOAD FUNCTIONALITY ==========
    document.querySelectorAll('.download-img-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const imgId = this.getAttribute('data-target');
            const img = document.getElementById(imgId);
            
            if (!img) {
                console.error('Image not found:', imgId);
                return;
            }

            // Create a temporary link element
            const link = document.createElement('a');
            link.download = imgId + '_clustering_datastats.png';
            link.href = img.src;
            
            // Trigger download
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Visual feedback
            const originalText = this.textContent;
            this.textContent = '✓ Downloaded!';
            this.style.background = 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)';
            
            setTimeout(() => {
                this.textContent = originalText;
                this.style.background = '';
            }, 2000);
        });
    });
});