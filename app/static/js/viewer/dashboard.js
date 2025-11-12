// Analyst Dashboard JavaScript - Interactive Features and Analytics

class DashboardManager {
  constructor() {
    this.initializeEventListeners();
    this.initializeAnimations();
    this.initializeCharts();
    this.initializeRealTimeUpdates();
    this.initializeKeyboardNavigation();
    this.initializeTheme();
  }

  // Initialize all event listeners
  initializeEventListeners() {
    document.addEventListener('DOMContentLoaded', () => {
      this.setupStatCardInteractions();
      this.setupButtonAnimations();
      this.setupTableInteractions();
      this.setupSearchFunctionality();
      this.setupModalHandlers();
    });

    // Handle window resize for responsive adjustments
    window.addEventListener('resize', this.debounce(this.handleResize.bind(this), 250));
    
    // Handle scroll events for animations
    window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 16));
  }

  // Setup stat card interactions with enhanced analytics
  setupStatCardInteractions() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach((card, index) => {
      // Add click handlers for detailed views
      card.addEventListener('click', (e) => {
        this.showStatDetails(index, card);
        this.trackEvent('stat_card_click', { card_index: index });
      });

      // Add hover effects with data fetching
      card.addEventListener('mouseenter', (e) => {
        this.enhanceStatCard(card, index);
      });

      // Add keyboard navigation
      card.setAttribute('tabindex', '0');
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          card.click();
        }
      });

      // Animate on viewport entry
      this.observeElement(card, () => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
          card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
        }, index * 100);
      });
    });
  }

  // Enhanced stat card with tooltip and micro-animations
  enhanceStatCard(card, index) {
    const tooltip = this.createTooltip(index);
    if (tooltip) {
      card.appendChild(tooltip);
      
      setTimeout(() => {
        tooltip.style.opacity = '1';
        tooltip.style.transform = 'translateY(-10px)';
      }, 100);

      card.addEventListener('mouseleave', () => {
        tooltip.style.opacity = '0';
        tooltip.style.transform = 'translateY(0)';
        setTimeout(() => tooltip.remove(), 300);
      }, { once: true });
    }
  }

  // Create dynamic tooltips for stat cards
  createTooltip(index) {
    const tooltips = [
      'Total datasets uploaded and processed',
      'Comprehensive analyses completed',
      'Last dataset upload timestamp',
      'Successfully generated reports',
      'Reports awaiting completion'
    ];

    const tooltip = document.createElement('div');
    tooltip.className = 'stat-tooltip';
    tooltip.textContent = tooltips[index] || 'Statistical information';
    
    tooltip.style.cssText = `
      position: absolute;
      bottom: 100%;
      left: 50%;
      transform: translateX(-50%) translateY(0);
      background: rgba(30, 41, 59, 0.95);
      color: white;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.875rem;
      white-space: nowrap;
      opacity: 0;
      transition: all 0.3s ease;
      pointer-events: none;
      z-index: 1000;
      backdrop-filter: blur(10px);
    `;

    // Add arrow
    const arrow = document.createElement('div');
    arrow.style.cssText = `
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      border: 6px solid transparent;
      border-top-color: rgba(30, 41, 59, 0.95);
    `;
    tooltip.appendChild(arrow);

    return tooltip;
  }

  // Setup interactive button animations
  setupButtonAnimations() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
      // Add ripple effect
      button.addEventListener('click', (e) => {
        this.createRippleEffect(e, button);
      });

      // Add loading state for async operations
      if (button.textContent.includes('Upload') || button.textContent.includes('Generate')) {
        button.addEventListener('click', () => {
          this.addLoadingState(button);
        });
      }
    });
  }

  // Create ripple effect on button click
  createRippleEffect(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background: rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      transform: scale(0);
      animation: ripple 0.6s ease-out;
      pointer-events: none;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
  }

  // Add CSS animation for ripple effect
  initializeAnimations() {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes ripple {
        to {
          transform: scale(2);
          opacity: 0;
        }
      }
      
      @keyframes slideInUp {
        from {
          transform: translateY(30px);
          opacity: 0;
        }
        to {
          transform: translateY(0);
          opacity: 1;
        }
      }
      
      @keyframes fadeInScale {
        from {
          transform: scale(0.95);
          opacity: 0;
        }
        to {
          transform: scale(1);
          opacity: 1;
        }
      }
      
      .animate-slide-up {
        animation: slideInUp 0.6s ease-out;
      }
      
      .animate-fade-scale {
        animation: fadeInScale 0.4s ease-out;
      }
    `;
    document.head.appendChild(style);
  }

  // Setup enhanced table interactions
  setupTableInteractions() {
    const table = document.querySelector('.table');
    if (!table) return;

    // Add sorting functionality
    const headers = table.querySelectorAll('thead th');
    headers.forEach((header, index) => {
      if (index < headers.length - 1) { // Skip actions column
        header.style.cursor = 'pointer';
        header.addEventListener('click', () => {
          this.sortTable(table, index);
        });
        
        // Add sort indicator
        const indicator = document.createElement('span');
        indicator.className = 'sort-indicator';
        indicator.innerHTML = ' ⇅';
        indicator.style.opacity = '0.5';
        header.appendChild(indicator);
      }
    });

    // Enhanced row interactions
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
      row.addEventListener('click', (e) => {
        if (!e.target.closest('.btn')) {
          this.highlightRow(row);
        }
      });
    });
  }

  // Table sorting functionality
  sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const header = table.querySelectorAll('thead th')[columnIndex];
    const indicator = header.querySelector('.sort-indicator');
    
    const isAscending = !header.classList.contains('sort-desc');
    
    // Reset all sort indicators
    table.querySelectorAll('.sort-indicator').forEach(ind => {
      ind.innerHTML = ' ⇅';
      ind.parentElement.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Set current sort indicator
    indicator.innerHTML = isAscending ? ' ↑' : ' ↓';
    header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
    
    rows.sort((a, b) => {
      const aText = a.cells[columnIndex].textContent.trim();
      const bText = b.cells[columnIndex].textContent.trim();
      
      // Handle different data types
      const aVal = this.parseValue(aText);
      const bVal = this.parseValue(bText);
      
      if (aVal < bVal) return isAscending ? -1 : 1;
      if (aVal > bVal) return isAscending ? 1 : -1;
      return 0;
    });
    
    // Animate table update
    tbody.style.opacity = '0.7';
    setTimeout(() => {
      rows.forEach(row => tbody.appendChild(row));
      tbody.style.opacity = '1';
    }, 150);
  }

  // Parse different value types for sorting
  parseValue(text) {
    // Try to parse as date
    const dateMatch = text.match(/\d{4}-\d{2}-\d{2}/);
    if (dateMatch) return new Date(dateMatch[0]);
    
    // Try to parse as number
    const number = parseFloat(text.replace(/,/g, ''));
    if (!isNaN(number)) return number;
    
    // Return as lowercase string
    return text.toLowerCase();
  }

  // Add search functionality
  setupSearchFunctionality() {
    // Create search input if it doesn't exist
    const searchContainer = document.createElement('div');
    searchContainer.className = 'search-container mb-3';
    searchContainer.innerHTML = `
      <div class="input-group">
        <span class="input-group-text">🔍</span>
        <input type="text" class="form-control" placeholder="Search datasets, reports, or activities..." id="dashboard-search">
      </div>
    `;
    
    const table = document.querySelector('.table');
    if (table) {
      table.parentElement.insertBefore(searchContainer, table);
      
      const searchInput = document.getElementById('dashboard-search');
      searchInput.addEventListener('input', this.debounce((e) => {
        this.filterContent(e.target.value);
      }, 300));
    }
  }

  // Filter dashboard content based on search
  filterContent(searchTerm) {
    const term = searchTerm.toLowerCase();
    
    // Filter table rows
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
      const text = row.textContent.toLowerCase();
      const shouldShow = text.includes(term);
      row.style.display = shouldShow ? '' : 'none';
      
      if (shouldShow && term) {
        row.classList.add('highlight-match');
      } else {
        row.classList.remove('highlight-match');
      }
    });
    
    // Filter activity logs
    const activityItems = document.querySelectorAll('.list-group-item');
    activityItems.forEach(item => {
      const text = item.textContent.toLowerCase();
      const shouldShow = text.includes(term);
      item.style.display = shouldShow ? '' : 'none';
    });
  }

  // Setup modal handlers (stub for future modals)
  setupModalHandlers() {
    // Implement modal logic if needed
  }

  // Initialize charts (stub for future chart integrations)
  initializeCharts() {
    // Implement chart logic if needed
  }

  // Initialize real-time updates
  initializeRealTimeUpdates() {
    // Simulate real-time stat updates
    setInterval(() => {
      this.updateStats();
    }, 30000); // Update every 30 seconds

    // Add connection status indicator
    this.createConnectionStatus();
  }

  // Update statistics with animation
  updateStats() {
    const statCards = document.querySelectorAll('.stat-card strong');
    statCards.forEach(stat => {
      const currentValue = parseInt(stat.textContent) || 0;
      const change = Math.floor(Math.random() * 3); // Random small increase
      
      if (change > 0) {
        this.animateNumber(stat, currentValue, currentValue + change);
      }
    });
  }

  // Animate number changes
  animateNumber(element, start, end) {
    const duration = 1000;
    const steps = 30;
    const stepValue = (end - start) / steps;
    let current = start;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current += stepValue;
      element.textContent = Math.round(current);
      
      if (step >= steps) {
        clearInterval(timer);
        element.textContent = end;
        
        // Add flash effect
        element.style.color = '#16a34a';
        setTimeout(() => {
          element.style.color = '';
        }, 500);
      }
    }, duration / steps);
  }

  // Create connection status indicator
  createConnectionStatus() {
    const indicator = document.createElement('div');
    indicator.className = 'connection-status';
    indicator.innerHTML = `
      <div class="status-dot"></div>
      <span>Connected</span>
    `;
    
    indicator.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: rgba(22, 163, 74, 0.1);
      color: #16a34a;
      padding: 8px 12px;
      border-radius: 20px;
      font-size: 0.875rem;
      display: flex;
      align-items: center;
      gap: 6px;
      z-index: 1000;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(22, 163, 74, 0.2);
    `;
    
    const dot = indicator.querySelector('.status-dot');
    dot.style.cssText = `
      width: 8px;
      height: 8px;
      background: #16a34a;
      border-radius: 50%;
      animation: pulse 2s infinite;
    `;
    
    document.body.appendChild(indicator);
  }

  // Initialize keyboard navigation
  initializeKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      // Quick access shortcuts
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case 'k':
            e.preventDefault();
            document.getElementById('dashboard-search')?.focus();
            break;
          case 'u':
            e.preventDefault();
            document.querySelector('a[href*="upload"]')?.click();
            break;
        }
      }
      
      // Tab navigation enhancements
      if (e.key === 'Tab') {
        const focusedElement = document.activeElement;
        if (focusedElement.classList.contains('stat-card')) {
          focusedElement.style.outline = '2px solid var(--primary-color)';
          focusedElement.style.outlineOffset = '2px';
        }
      }
    });
  }

  // Initialize theme and appearance
  initializeTheme() {
    // Detect system theme preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Add theme toggle if needed
    const themeToggle = document.createElement('button');
    themeToggle.className = 'theme-toggle';
    themeToggle.innerHTML = '🌙';
    themeToggle.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: var(--card-background);
      border: 1px solid var(--border-color);
      font-size: 1.5rem;
      cursor: pointer;
      transition: var(--transition);
      z-index: 1000;
      box-shadow: var(--shadow-md);
    `;
    
    themeToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark-theme');
      themeToggle.innerHTML = document.body.classList.contains('dark-theme') ? '☀️' : '🌙';
    });
    
    document.body.appendChild(themeToggle);
  }

  // Utility functions
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

  // Intersection Observer for animations
  observeElement(element, callback) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          callback();
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    
    observer.observe(element);
  }

  // Handle responsive behavior
  handleResize() {
    // Adjust layouts for different screen sizes
    const screenWidth = window.innerWidth;
    const statCards = document.querySelectorAll('.stat-card');
    
    if (screenWidth < 768) {
      statCards.forEach(card => {
        card.style.marginBottom = '1rem';
      });
    }
  }

  // Handle scroll effects
  handleScroll() {
    const scrollTop = window.pageYOffset;
    
    // Add parallax effect to dashboard title
    const title = document.querySelector('.dashboard-title');
    if (title) {
      title.style.transform = `translateY(${scrollTop * 0.1}px)`;
    }
  }

  // Track events for analytics
  trackEvent(eventName, data) {
    // Send to analytics service
    console.log(`Event: ${eventName}`, data);
    // In production: analytics.track(eventName, data);
  }

  // Show detailed stat information
  showStatDetails(index, card) {
    // Implementation for detailed stat view
    console.log(`Showing details for stat card ${index}`);
    // In production: open modal or navigate to detailed view
  }

  // Add loading state to buttons
  addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    button.disabled = true;
    
    // Simulate async operation
    setTimeout(() => {
      button.innerHTML = originalText;
      button.disabled = false;
    }, 2000);
  }

  // Highlight selected table row
  highlightRow(row) {
    // Remove previous highlights
    document.querySelectorAll('.table tbody tr.selected').forEach(r => {
      r.classList.remove('selected');
    });
    
    // Add highlight to clicked row
    row.classList.add('selected');
    
    // Add selected row styles
    row.style.backgroundColor = '#e0e7ff';
    row.style.fontWeight = 'bold';
  }
}

// Initialize dashboard manager
new DashboardManager();

// viewer/dashboard.js

document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ Viewer Dashboard JS Loaded");

    animateKPICards();
    animateDistributionBars();
    initGraphPreviewModal();
    setupFallbackImages();
    enhanceActionCards();
});

/* ------------------------------------------
   KPI Card Hover & Click Animation
--------------------------------------------*/
function animateKPICards() {
    const cards = document.querySelectorAll(".kpi-card");

    cards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.style.transform = "scale(1.04)";
            card.style.transition = "0.25s ease";
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "scale(1)";
        });

        card.addEventListener("click", () => {
            card.style.transform = "scale(0.97)";
            setTimeout(() => card.style.transform = "scale(1.04)", 150);
        });
    });
}

/* ------------------------------------------
   Smooth Animated Percent Bars
--------------------------------------------*/
function animateDistributionBars() {
    document.querySelectorAll(".bar-fill").forEach(bar => {
        const width = bar.style.width;
        bar.style.width = "0%";

        setTimeout(() => {
            bar.style.transition = "width 1s ease";
            bar.style.width = width;
        }, 200);
    });
}

/* ------------------------------------------
   Graph Preview Modal
--------------------------------------------*/
function initGraphPreviewModal() {
    const images = document.querySelectorAll(".graph-preview img");

    if (images.length === 0) return;

    // Modal structure
    const modal = document.createElement("div");
    modal.id = "img-modal";
    modal.style = `
        display:none; position:fixed; inset:0; 
        background:rgba(0,0,0,0.85); 
        justify-content:center; align-items:center; z-index:9999;
    `;
    modal.innerHTML = `
        <img id="modal-img" style="max-width:90%; max-height:85%; border:3px solid white; border-radius:8px;">
        <span id="modal-close" style="position:absolute; top:20px; right:30px; font-size:30px; color:white; cursor:pointer;">✖</span>
    `;
    document.body.appendChild(modal);

    const modalImg = document.getElementById("modal-img");
    const modalClose = document.getElementById("modal-close");

    images.forEach(img => {
        img.style.cursor = "zoom-in";
        img.addEventListener("click", () => {
            modalImg.src = img.src;
            modal.style.display = "flex";
        });
    });

    modalClose.onclick = () => modal.style.display = "none";
    modal.onclick = e => { if (e.target === modal) modal.style.display = "none"; };
}

/* ------------------------------------------
   Graceful Fallback for Broken Images
--------------------------------------------*/
function setupFallbackImages() {
    document.querySelectorAll("img").forEach(img => {
        img.onerror = () => {
            img.src = "/static/img/placeholder-image.png";
        };
    });
}

/* ------------------------------------------
   Improve Quick-Action Cards (UX Feedback)
--------------------------------------------*/
function enhanceActionCards() {
    document.querySelectorAll(".action-card[onclick]").forEach(card => {
        card.addEventListener("click", () => {
            const message = card.querySelector("h4").innerText + " feature coming soon!";
            alert(message);
        });
    });
}
