// Search page functionality
document.addEventListener('DOMContentLoaded', function() {
    initSearchPage();
    initFilters();
    initModal();
});

function initSearchPage() {
    console.log('Search page initialized');
    
    // Add loading animations
    const graphCards = document.querySelectorAll('.graph-card');
    graphCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Initialize tooltips
    initTooltips();
}

function initFilters() {
    // Real-time filter updates (optional)
    const filterInputs = document.querySelectorAll('input, select');
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Optional: Auto-submit form on filter change
            // this.form.submit();
        });
    });
    
    // Date validation
    const dateFrom = document.getElementById('date_from');
    const dateTo = document.getElementById('date_to');
    
    if (dateFrom && dateTo) {
        dateFrom.addEventListener('change', function() {
            if (dateTo.value && this.value > dateTo.value) {
                dateTo.value = this.value;
            }
        });
        
        dateTo.addEventListener('change', function() {
            if (dateFrom.value && this.value < dateFrom.value) {
                dateFrom.value = this.value;
            }
        });
    }
}

function initModal() {
    const modal = document.getElementById('graphModal');
    const closeBtn = modal.querySelector('.close');
    
    // Close modal when clicking X
    closeBtn.addEventListener('click', closeModal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
}

function viewGraph(graphId) {
    const graphCard = document.querySelector(`[onclick="viewGraph('${graphId}')"]`).closest('.graph-card');
    const graphTitle = graphCard.querySelector('.graph-title').textContent;
    const graphImage = graphCard.querySelector('img');
    
    if (graphImage) {
        const modal = document.getElementById('graphModal');
        const modalTitle = document.getElementById('modalGraphTitle');
        const modalImage = document.getElementById('modalGraphImage');
        
        modalTitle.textContent = graphTitle;
        modalImage.src = graphImage.src;
        modalImage.alt = graphTitle;
        
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal() {
    const modal = document.getElementById('graphModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function downloadGraph(graphId) {
    const graphCard = document.querySelector(`[onclick="downloadGraph('${graphId}')"]`).closest('.graph-card');
    const graphImage = graphCard.querySelector('img');
    const graphTitle = graphCard.querySelector('.graph-title').textContent;
    
    if (!graphImage || !graphImage.src) {
        showNotification('No image available for download', 'error');
        return;
    }
    
    // Show download feedback
    const button = event.target.closest('.btn-download');
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Downloading...';
    button.disabled = true;
    
    try {
        // Create a temporary link for download
        const link = document.createElement('a');
        link.href = graphImage.src;
        
        // Extract filename from URL or use graph title
        let filename = 'graph.png';
        if (graphImage.src) {
            const urlParts = graphImage.src.split('/');
            const existingFilename = urlParts[urlParts.length - 1];
            if (existingFilename && existingFilename !== 'placeholder-graph.png') {
                filename = existingFilename;
            } else {
                // Create a safe filename from graph title
                filename = graphTitle
                    .toLowerCase()
                    .replace(/[^a-z0-9]/g, '_')
                    .replace(/_+/g, '_')
                    .replace(/^_|_$/g, '') + '.png';
            }
        }
        
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Show success message after a short delay
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
            showNotification('Graph downloaded successfully!', 'success');
        }, 500);
        
    } catch (error) {
        console.error('Download failed:', error);
        button.innerHTML = originalText;
        button.disabled = false;
        showNotification('Download failed. Please try again.', 'error');
    }
}

function downloadCurrentGraph() {
    const modalImage = document.getElementById('modalGraphImage');
    const modalTitle = document.getElementById('modalGraphTitle').textContent;
    
    if (!modalImage || !modalImage.src) {
        showNotification('No image available for download', 'error');
        return;
    }
    
    try {
        // Create a temporary link for download
        const link = document.createElement('a');
        link.href = modalImage.src;
        
        // Create a safe filename from graph title
        const filename = modalTitle
            .toLowerCase()
            .replace(/[^a-z0-9]/g, '_')
            .replace(/_+/g, '_')
            .replace(/^_|_$/g, '') + '.png';
            
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showNotification('Graph downloaded successfully!', 'success');
        
    } catch (error) {
        console.error('Download failed:', error);
        showNotification('Download failed. Please try again.', 'error');
    }
}

function toggleFavorite(graphId) {
    const button = event.target.closest('.btn-favorite');
    const icon = button.querySelector('i');
    
    // Toggle favorite state
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas', 'text-yellow-500');
        showNotification('Added to favorites!', 'success');
    } else {
        icon.classList.remove('fas', 'text-yellow-500');
        icon.classList.add('far');
        showNotification('Removed from favorites!', 'info');
    }
    
    // In a real app, you would make an API call here
    console.log('Toggled favorite for graph:', graphId);
}

function initTooltips() {
    // Initialize any tooltips if needed
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            // Tooltip implementation can be added here
        });
    });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    return colors[type] || '#3b82f6';
}

// Quick search function
function quickSearch(query) {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.value = query;
        searchInput.form.submit();
    }
}

// Export search results
function exportSearchResults() {
    const searchParams = new URLSearchParams(window.location.search);
    const exportUrl = `/api/export/search?${searchParams.toString()}`;
    
    // Trigger download
    window.open(exportUrl, '_blank');
}

// Add CSS animations for notifications
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
    
    .graph-card {
        animation: fadeInUp 0.6s ease both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);