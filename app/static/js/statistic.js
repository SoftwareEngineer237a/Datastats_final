// Modern Interactive JavaScript for Descriptive Statistics
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Descriptive Statistics enhancements...');
    
    // Initialize all features
    initializeSearchFilter();
    initializeTableEnhancements();
    initializeTooltips();
    initializeSortingFeatures();
    initializeButtonEnhancements();
    initializeAnimationObserver();
    initializeKeyboardNavigation();
    initializeStatisticalHighlights();
    
    console.log('✨ All enhancements loaded successfully!');

    // Search Filter Implementation
    function initializeSearchFilter() {
        const firstTableWrapper = document.querySelector('.table-wrapper');
        if (!firstTableWrapper) return;

        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'search-input';
        searchInput.placeholder = '🔍 Search in tables... (try column names or values)';
        searchInput.setAttribute('aria-label', 'Search table data');
        
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterTables(this.value.trim());
                announceSearchResults(this.value.trim());
            }, 300);
        });

        // Add search shortcuts
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                this.value = '';
                filterTables('');
                this.blur();
            }
        });

        searchContainer.appendChild(searchInput);
        firstTableWrapper.parentNode.insertBefore(searchContainer, firstTableWrapper);
        
        console.log('🔍 Search filter initialized');
    }

    function filterTables(searchTerm) {
        const tables = document.querySelectorAll('.table');
        const lowerSearchTerm = searchTerm.toLowerCase();
        let totalVisible = 0;

        tables.forEach(table => {
            const rows = table.querySelectorAll('tbody tr');
            let visibleInTable = 0;

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const matches = !searchTerm || text.includes(lowerSearchTerm);
                
                if (matches) {
                    row.style.display = '';
                    row.style.animation = searchTerm ? 'fadeIn 0.3s ease-out' : '';
                    visibleInTable++;
                    totalVisible++;
                    
                    // Highlight matching text
                    if (searchTerm) {
                        highlightSearchTerm(row, searchTerm);
                    } else {
                        removeHighlights(row);
                    }
                } else {
                    row.style.display = 'none';
                }
            });

            // Show/hide table based on visible rows
            const wrapper = table.closest('.table-wrapper');
            if (wrapper) {
                wrapper.style.opacity = visibleInTable > 0 ? '1' : '0.5';
            }
        });

        return totalVisible;
    }

    function highlightSearchTerm(row, term) {
        const cells = row.querySelectorAll('td');
        cells.forEach(cell => {
            if (!cell.querySelector('.highlight')) {
                const text = cell.textContent;
                const regex = new RegExp(`(${term})`, 'gi');
                const highlightedText = text.replace(regex, '<span class="highlight">$1</span>');
                if (highlightedText !== text) {
                    cell.innerHTML = highlightedText;
                }
            }
        });
    }

    function removeHighlights(row) {
        const highlights = row.querySelectorAll('.highlight');
        highlights.forEach(highlight => {
            const parent = highlight.parentNode;
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        });
    }

    function announceSearchResults(term) {
        const existingAnnouncement = document.getElementById('search-announcement');
        if (existingAnnouncement) {
            existingAnnouncement.remove();
        }

        if (term) {
            const announcement = document.createElement('div');
            announcement.id = 'search-announcement';
            announcement.setAttribute('aria-live', 'polite');
            announcement.style.cssText = `
                position: absolute;
                left: -9999px;
                width: 1px;
                height: 1px;
                overflow: hidden;
            `;
            
            const visibleRows = document.querySelectorAll('.table tbody tr[style=""], .table tbody tr:not([style])').length;
            announcement.textContent = `Found ${visibleRows} matching rows for "${term}"`;
            document.body.appendChild(announcement);
        }
    }

    // Table Enhancement Functions
    function initializeTableEnhancements() {
        const tables = document.querySelectorAll('.table');
        
        tables.forEach((table, index) => {
            enhanceTableAccessibility(table, index);
            addRowInteractions(table);
            addColumnHighlighting(table);
            markNumericCells(table);
        });

        console.log(`📊 Enhanced ${tables.length} tables`);
    }

    function enhanceTableAccessibility(table, index) {
        table.setAttribute('role', 'table');
        table.setAttribute('aria-label', `Data table ${index + 1}`);
        
        const headers = table.querySelectorAll('thead th');
        headers.forEach((header, i) => {
            header.id = `header-${index}-${i}`;
            header.setAttribute('scope', 'col');
        });

        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, rowIndex) => {
            row.setAttribute('tabindex', '0');
            row.setAttribute('role', 'row');
            row.setAttribute('aria-rowindex', rowIndex + 1);
            
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, cellIndex) => {
                cell.setAttribute('role', 'gridcell');
                cell.setAttribute('headers', `header-${index}-${cellIndex}`);
            });
        });
    }

    function addRowInteractions(table) {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            // Mouse interactions
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.01)';
                this.style.zIndex = '10';
                createRippleEffect(this);
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.zIndex = '1';
            });

            // Click interactions
            row.addEventListener('click', function(e) {
                if (e.target.tagName !== 'INPUT') {
                    selectRow(this);
                    showRowStats(this);
                }
            });

            // Keyboard interactions
            row.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        });
    }

    function createRippleEffect(element) {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(37, 99, 235, 0.3);
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
            left: 50%;
            top: 50%;
            width: 20px;
            height: 20px;
            margin-left: -10px;
            margin-top: -10px;
        `;
        
        element.style.position = 'relative';
        element.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }

    function selectRow(row) {
        // Remove previous selection
        const previouslySelected = document.querySelectorAll('.table tbody tr.selected');
        previouslySelected.forEach(r => r.classList.remove('selected'));
        
        // Add selection to current row
        row.classList.add('selected');
        row.style.animation = 'pulse 0.5s ease-in-out';
        
        // Announce selection to screen readers
        const rowIndex = Array.from(row.parentNode.children).indexOf(row) + 1;
        announceToScreenReader(`Row ${rowIndex} selected`);
    }

    function addColumnHighlighting(table) {
        const headers = table.querySelectorAll('thead th');
        
        headers.forEach((header, columnIndex) => {
            header.addEventListener('mouseenter', function() {
                highlightColumn(table, columnIndex, true);
            });
            
            header.addEventListener('mouseleave', function() {
                highlightColumn(table, columnIndex, false);
            });
        });
    }

    function highlightColumn(table, columnIndex, highlight) {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const cell = row.cells[columnIndex];
            if (cell) {
                if (highlight) {
                    cell.style.background = 'rgba(37, 99, 235, 0.1)';
                    cell.style.borderLeft = '2px solid #60a5fa';
                    cell.style.borderRight = '2px solid #60a5fa';
                    cell.style.transform = 'scale(1.02)';
                } else {
                    cell.style.background = '';
                    cell.style.borderLeft = '';
                    cell.style.borderRight = '';
                    cell.style.transform = '';
                }
            }
        });
    }

    function markNumericCells(table) {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            cells.forEach(cell => {
                const value = cell.textContent.trim();
                if (isNumeric(value)) {
                    cell.setAttribute('data-type', 'number');
                    cell.setAttribute('data-value', parseFloat(value));
                    addNumberFormatting(cell, parseFloat(value));
                }
            });
        });
    }

    function addNumberFormatting(cell, value) {
        // Add visual indicators for different number ranges
        if (value < 0) {
            cell.style.color = '#dc2626';
        }
    }
})