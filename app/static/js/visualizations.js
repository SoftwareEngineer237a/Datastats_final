// visualizations.js

/**
 * Advanced Visualization Interface Controller
 * Handles dynamic form interactions, chart type specific options,
 * and provides enhanced user experience features
 */

class VizController {
  constructor() {
    this.elements = {};
    this.chartConfigs = {};
    this.isLoading = false;
    this.init();
  } 

  /**
   * Initialize the controller
   */
  init() {
    this.cacheElements();
    this.setupChartConfigs();
    this.bindEvents();
    this.initializeState();
    this.setupValidation();
    this.setupAccessibility();
    this.setupDownloadFunctionality();
  }

  /**
   * Cache DOM elements for performance
   */
  cacheElements() {
    this.elements = {
      // Form elements
      form: document.querySelector('.viz-form'),
      chartType: document.getElementById('chart_type'),
      subtype: document.getElementById('subtype'),
      sourceRadios: document.querySelectorAll('input[name="source"]'),
      analysisRow: document.querySelector('.analysis-source'),
      
      // Field selectors
      xField: document.getElementById('x'),
      yField: document.getElementById('y'),
      y2Field: document.getElementById('y2'),
      zField: document.getElementById('z'),
      groupField: document.getElementById('group'),
      sizeField: document.getElementById('size'),
      colorField: document.getElementById('color'),
      yMultiField: document.getElementById('y_multi'),
      
      // Option panels
      optionPanels: document.querySelectorAll('.options'),
      
      // Map specific elements
      mapSubtype: document.getElementById('map_subtype'),
      mapDot: document.querySelector('.map-dot'),
      mapChoropleth: document.querySelector('.map-choropleth'),
      
      // Interactive checkbox
      interactive: document.querySelector('input[name="interactive"]'),
      
      // Submit button
      submitBtn: document.querySelector('.btn-run'),
      
      // Fieldsets
      fieldsets: document.querySelectorAll('.fieldset')
    };
  }

  /**
   * Setup chart type configurations
   */
  setupChartConfigs() {
    this.chartConfigs = {
      bar: {
        requiredFields: ['x', 'y'],
        optionalFields: ['group', 'color'],
        subtypes: ['vertical', 'horizontal', 'stacked', 'grouped'],
        supportsInteractive: true,
        description: 'Compare categories with bars'
      },
      line: {
        requiredFields: ['x'],
        optionalFields: ['y', 'y_multi', 'group'],
        subtypes: ['simple', 'multiple', 'area'],
        supportsInteractive: true,
        description: 'Show trends over time or continuous data'
      },
      pie: {
        requiredFields: ['x', 'y'],
        optionalFields: [],
        subtypes: ['pie', 'donut', 'exploded'],
        supportsInteractive: false,
        description: 'Show parts of a whole'
      },
      scatter: {
        requiredFields: ['x', 'y'],
        optionalFields: ['size', 'color', 'group'],
        subtypes: ['scatter', 'bubble'],
        supportsInteractive: true,
        description: 'Explore relationships between variables'
      },
      hist: {
        requiredFields: ['x'],
        optionalFields: [],
        subtypes: ['hist', 'cumulative'],
        supportsInteractive: false,
        description: 'Show distribution of values'
      },
      box_violin: {
        requiredFields: ['y'],
        optionalFields: ['group'],
        subtypes: ['box', 'violin'],
        supportsInteractive: false,
        description: 'Compare distributions across groups'
      },
      heatmap: {
        requiredFields: ['y_multi'],
        optionalFields: [],
        subtypes: ['standard', 'clustered'],
        supportsInteractive: false,
        description: 'Show correlation patterns'
      },
      radar: {
        requiredFields: ['y_multi'],
        optionalFields: ['group'],
        subtypes: [],
        supportsInteractive: false,
        description: 'Compare multiple metrics'
      },
      treemap: {
        requiredFields: ['x', 'y'],
        optionalFields: ['parent'],
        subtypes: [],
        supportsInteractive: true,
        description: 'Hierarchical data visualization'
      },
      funnel: {
        requiredFields: ['x', 'y'],
        optionalFields: [],
        subtypes: [],
        supportsInteractive: true,
        description: 'Show conversion or process flow'
      },
      network: {
        requiredFields: [],
        optionalFields: ['source_col', 'target_col', 'weight_col', 'y_multi'],
        subtypes: [],
        supportsInteractive: false,
        description: 'Show relationships and connections'
      },
      waterfall: {
        requiredFields: ['x', 'y'],
        optionalFields: [],
        subtypes: [],
        supportsInteractive: false,
        description: 'Show cumulative effect of changes'
      },
      gantt: {
        requiredFields: ['x', 'start_col', 'end_col'],
        optionalFields: ['group'],
        subtypes: [],
        supportsInteractive: true,
        description: 'Project timeline visualization'
      },
      sankey: {
        requiredFields: ['source_col', 'target_col', 'value_col'],
        optionalFields: [],
        subtypes: [],
        supportsInteractive: true,
        description: 'Flow diagram'
      },
      map: {
        requiredFields: ['y'],
        optionalFields: ['geo_col', 'lat_col', 'lon_col'],
        subtypes: ['choropleth', 'dot'],
        supportsInteractive: true,
        description: 'Geographical data visualization'
      },
      dendrogram: {
        requiredFields: ['y_multi'],
        optionalFields: [],
        subtypes: [],
        supportsInteractive: false,
        description: 'Hierarchical clustering'
      },
      combo: {
        requiredFields: ['x', 'y', 'y2'],
        optionalFields: [],
        subtypes: [],
        supportsInteractive: false,
        description: 'Combine bar and line charts'
      },
      '3dscatter': {
        requiredFields: ['x', 'y', 'z'],
        optionalFields: ['color', 'size'],
        subtypes: [],
        supportsInteractive: true,
        description: '3D scatter plot'
      }
    };
  }

  /**
   * Bind event listeners
   */
  bindEvents() {
    // Source toggle
    this.elements.sourceRadios.forEach(radio => {
      radio.addEventListener('change', () => this.toggleSource());
    });

    // Chart type change
    if (this.elements.chartType) {
      this.elements.chartType.addEventListener('change', (e) => {
        this.onChartTypeChange(e.target.value);
      });
    }

    // Map subtype toggle
    if (this.elements.mapSubtype) {
      this.elements.mapSubtype.addEventListener('change', () => {
        this.toggleMapOptions();
      });
    }

    // Form submission
    if (this.elements.form) {
      this.elements.form.addEventListener('submit', (e) => {
        this.onFormSubmit(e);
      });
    }

    // Field highlighting on focus
    this.setupFieldHighlighting();

    // Real-time validation
    this.setupRealTimeValidation();

    // Keyboard shortcuts
    this.setupKeyboardShortcuts();
  }

  /**
   * Initialize component state
   */
  initializeState() {
    this.toggleSource();
    this.onChartTypeChange(this.elements.chartType?.value || '');
    this.toggleMapOptions();
    this.updateInteractiveAvailability();
  }

  /**
   * Toggle source selection (dataset vs analysis CSV)
   */
  toggleSource() {
    const selectedSource = document.querySelector('input[name="source"]:checked')?.value;
    const isAnalysisCsv = selectedSource === 'analysis_csv';
    
    if (this.elements.analysisRow) {
      this.elements.analysisRow.style.display = isAnalysisCsv ? 'block' : 'none';
      
      // Add animation class
      if (isAnalysisCsv) {
        this.elements.analysisRow.classList.add('slide-in');
        setTimeout(() => {
          this.elements.analysisRow.classList.remove('slide-in');
        }, 300);
      }
    }
  }

  /**
   * Handle chart type selection change
   */
  onChartTypeChange(chartType) {
    this.hideAllOptions();
    this.showRelevantOptions(chartType);
    this.updateSubtypeOptions(chartType);
    this.updateFieldRequirements(chartType);
    this.updateInteractiveAvailability();
    this.showChartDescription(chartType);
  }

  /**
   * Hide all option panels
   */
  hideAllOptions() {
    this.elements.optionPanels.forEach(panel => {
      panel.style.display = 'none';
      panel.classList.remove('active');
    });
  }

  /**
   * Show relevant options for chart type
   */
  showRelevantOptions(chartType) {
    const optionMap = {
      'bar': '.options-bar',
      'hist': '.options-hist',
      'radar': '.options-radar',
      'network': '.options-network',
      'gantt': '.options-gantt',
      'sankey': '.options-sankey',
      'map': '.options-map',
      'dendrogram': '.options-dendrogram'
    };

    const selector = optionMap[chartType];
    if (selector) {
      const panel = document.querySelector(selector);
      if (panel) {
        panel.style.display = 'block';
        panel.classList.add('active');
        
        // Trigger animation
        setTimeout(() => {
          panel.style.opacity = '1';
          panel.style.transform = 'translateY(0)';
        }, 10);
      }
    }
  }

  /**
   * Update subtype options based on chart type
   */
  updateSubtypeOptions(chartType) {
    if (!this.elements.subtype) return;

    const config = this.chartConfigs[chartType];
    if (!config || !config.subtypes.length) {
      this.elements.subtype.style.display = 'none';
      return;
    }

    this.elements.subtype.style.display = 'block';
    
    // Clear existing options except the first "(Auto)" option
    const autoOption = this.elements.subtype.querySelector('option[value=""]');
    this.elements.subtype.innerHTML = '';
    if (autoOption) {
      this.elements.subtype.appendChild(autoOption);
    }

    // Add chart-specific subtypes
    config.subtypes.forEach(subtype => {
      const option = document.createElement('option');
      option.value = subtype;
      option.textContent = this.capitalizeFirst(subtype);
      this.elements.subtype.appendChild(option);
    });
  }

  /**
   * Update field requirements and visual indicators
   */
  updateFieldRequirements(chartType) {
    const config = this.chartConfigs[chartType];
    if (!config) return;

    // Reset all field labels
    this.resetFieldLabels();

    // Mark required fields
    config.requiredFields.forEach(fieldName => {
      this.markFieldAsRequired(fieldName);
    });

    // Show/hide specific field groups
    this.toggleFieldVisibility(chartType);
  }

  /**
   * Reset field labels to default state
   */
  resetFieldLabels() {
    const fieldSelectors = ['x', 'y', 'y2', 'z', 'group', 'size', 'color', 'y_multi'];
    fieldSelectors.forEach(fieldId => {
      const field = document.getElementById(fieldId);
      if (field) {
        const label = field.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
          label.classList.remove('required', 'optional');
          label.innerHTML = label.innerHTML.replace(' *', '').replace(' (optional)', '');
        }
      }
    });
  }

  /**
   * Mark field as required
   */
  markFieldAsRequired(fieldName) {
    const field = document.getElementById(fieldName);
    if (field) {
      const label = field.previousElementSibling;
      if (label && label.tagName === 'LABEL') {
        label.classList.add('required');
        if (!label.innerHTML.includes(' *')) {
          label.innerHTML += ' <span style="color: var(--error-color);">*</span>';
        }
      }
    }
  }

  /**
   * Toggle field visibility based on chart type
   */
  toggleFieldVisibility(chartType) {
    const yMultiRow = document.querySelector('.y-multi');
    const showYMulti = ['line', 'heatmap', 'radar', 'dendrogram', 'network'].includes(chartType);
    
    if (yMultiRow) {
      yMultiRow.style.display = showYMulti ? 'block' : 'none';
    }

    // Show/hide Y2 field for combo charts
    const y2Col = this.elements.y2Field?.closest('.col');
    if (y2Col) {
      y2Col.style.display = chartType === 'combo' ? 'block' : 'none';
    }

    // Show/hide Z field for 3D charts
    const zCol = this.elements.zField?.closest('.col');
    if (zCol) {
      zCol.style.display = chartType === '3dscatter' ? 'block' : 'none';
    }
  }

  /**
   * Update interactive checkbox availability
   */
  updateInteractiveAvailability() {
    if (!this.elements.interactive) return;

    const chartType = this.elements.chartType?.value;
    const config = this.chartConfigs[chartType];
    const container = this.elements.interactive.closest('.col');

    if (config && config.supportsInteractive) {
      container.style.display = 'block';
      this.elements.interactive.disabled = false;
    } else {
      container.style.display = 'none';
      this.elements.interactive.checked = false;
      this.elements.interactive.disabled = true;
    }
  }

  /**
   * Show chart description
   */
  /**
   * Show chart description based on the chart type
   * @param {string} chartType - The type of chart
   */
  showChartDescription(chartType) {
    const config = this.chartConfigs[chartType];
    if (!config) return;

    // Remove existing description
    const existingDesc = document.querySelector('.chart-description');
    if (existingDesc) {
      existingDesc.remove();
    }

    // Add new description
    const chartFieldset = document.querySelector('.fieldset legend').parentElement;
    const desc = document.createElement('div');
    desc.className = 'chart-description';
    desc.innerHTML = `<p style="color: var(--text-muted); font-size: 0.875rem; margin-top: 0.5rem; font-style: italic;">${config.description}</p>`;
    
    const legend = chartFieldset.querySelector('legend');
    legend.parentNode.insertBefore(desc, legend.nextSibling);
  }

  /**
   * Toggle map-specific options
   */
  toggleMapOptions() {
    if (!this.elements.mapSubtype || !this.elements.mapDot || !this.elements.mapChoropleth) return;

    const subtype = this.elements.mapSubtype.value;

    // Toggle visibility based on selected subtype
    if (subtype === 'dot') {
      this.elements.mapDot.style.display = 'block';
      this.elements.mapChoropleth.style.display = 'none';
    } else if (subtype === 'choropleth') {
      this.elements.mapDot.style.display = 'none';
      this.elements.mapChoropleth.style.display = 'block';
    } else {
      this.elements.mapDot.style.display = 'none';
      this.elements.mapChoropleth.style.display = 'none';
    }
  }
  /**
 * Download functionality for generated charts
 */
setupDownloadFunctionality() {
  this.downloadHandlers = {
    image: this.downloadImageChart.bind(this),
    html: this.downloadHtmlChart.bind(this)
  };
  
  this.bindDownloadEvents();
}

/**
 * Bind events to download buttons
 */
bindDownloadEvents() {
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-download')) {
      const format = e.target.getAttribute('data-format');
      const type = e.target.getAttribute('data-type');
      this.handleDownload(format, type);
    }
  });
}

/**
 * Handle download request
 */
handleDownload(format, type) {
  const statusEl = document.querySelector('.download-status');
  const statusText = document.querySelector('.status-text');
  
  this.showStatus('Preparing download...', statusEl, statusText);
  
  try {
    const handler = this.downloadHandlers[type];
    if (handler) {
      handler(format);
    } else {
      this.downloadFallback(format);
    }
  } catch (error) {
    console.error('Download error:', error);
    this.showStatus('Download failed: ' + error.message, statusEl, statusText, 'error');
  }
}

/**
 * Download image-based charts (PNG, JPG, SVG)
 */
downloadImageChart(format) {
  const img = document.getElementById('generated-chart');
  if (!img) {
    throw new Error('No chart image found');
  }

  this.downloadImageElement(img, format);
}

/**
 * Download HTML/iframe charts (screenshot)
 */
downloadHtmlChart(format) {
  const iframe = document.getElementById('chart-iframe');
  if (!iframe || !iframe.contentWindow) {
    throw new Error('No interactive chart found');
  }

  this.captureIframeScreenshot(iframe, format);
}

/**
 * Download image element directly
 */
downloadImageElement(img, format) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  
  // Set canvas dimensions to image dimensions
  canvas.width = img.naturalWidth || img.width;
  canvas.height = img.naturalHeight || img.height;
  
  // Draw image on canvas
  ctx.drawImage(img, 0, 0);
  
  // Trigger download
  this.triggerCanvasDownload(canvas, format, 'chart');
}

/**
 * Capture iframe screenshot using html2canvas
 */
captureIframeScreenshot(iframe, format) {
  // Check if html2canvas is available
  if (typeof html2canvas === 'undefined') {
    this.loadHtml2Canvas().then(() => {
      this.captureIframeScreenshot(iframe, format);
    });
    return;
  }

  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
  
  html2canvas(iframeDoc.body, {
    allowTaint: true,
    useCORS: true,
    scale: 2, // Higher quality
    logging: false
  }).then(canvas => {
    this.triggerCanvasDownload(canvas, format, 'interactive-chart');
    this.showStatus('Download completed!', 
      document.querySelector('.download-status'), 
      document.querySelector('.status-text'), 
      'success');
  }).catch(error => {
    console.error('Screenshot capture failed:', error);
    this.showStatus('Screenshot failed. Try PNG download instead.', 
      document.querySelector('.download-status'), 
      document.querySelector('.status-text'), 
      'error');
  });
}

/**
 * Load html2canvas library dynamically
 */
loadHtml2Canvas() {
  return new Promise((resolve, reject) => {
    if (typeof html2canvas !== 'undefined') {
      resolve();
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

/**
 * Trigger download from canvas
 */
triggerCanvasDownload(canvas, format, filename) {
  const link = document.createElement('a');
  
  // Set appropriate MIME type and quality
  let mimeType, quality;
  switch (format) {
    case 'jpg':
    case 'jpeg':
      mimeType = 'image/jpeg';
      quality = 0.92;
      break;
    case 'png':
      mimeType = 'image/png';
      quality = 1.0;
      break;
    case 'svg':
      this.downloadAsSvg(canvas, filename);
      return;
    case 'pdf':
      this.downloadAsPdf(canvas, filename);
      return;
    default:
      mimeType = 'image/png';
  }

  // For raster formats
  link.download = `${filename}-${new Date().getTime()}.${format}`;
  link.href = canvas.toDataURL(mimeType, quality);
  link.click();
  
  this.showStatus('Download started!', 
    document.querySelector('.download-status'), 
    document.querySelector('.status-text'), 
    'success');
}

/**
 * Download as SVG (simplified - converts canvas to SVG)
 */
downloadAsSvg(canvas, filename) {
  const svg = this.canvasToSvg(canvas);
  const blob = new Blob([svg], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.download = `${filename}-${new Date().getTime()}.svg`;
  link.href = url;
  link.click();
  
  URL.revokeObjectURL(url);
}

/**
 * Convert canvas to SVG (basic implementation)
 */
canvasToSvg(canvas) {
  const width = canvas.width;
  const height = canvas.height;
  const dataUrl = canvas.toDataURL('image/png');
  
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
  <image href="${dataUrl}" width="${width}" height="${height}"/>
</svg>`;
}

/**
 * Download as PDF using jsPDF
 */
downloadAsPdf(canvas, filename) {
  if (typeof jspdf === 'undefined') {
    this.loadJsPdf().then(() => {
      this.downloadAsPdf(canvas, filename);
    });
    return;
  }

  const imgData = canvas.toDataURL('image/jpeg', 0.92);
  const pdf = new jspdf.jsPDF({
    orientation: canvas.width > canvas.height ? 'landscape' : 'portrait',
    unit: 'px',
    format: [canvas.width, canvas.height]
  });

  pdf.addImage(imgData, 'JPEG', 0, 0, canvas.width, canvas.height);
  pdf.save(`${filename}-${new Date().getTime()}.pdf`);
}

/**
 * Load jsPDF library dynamically
 */
loadJsPdf() {
  return new Promise((resolve, reject) => {
    if (typeof jspdf !== 'undefined') {
      resolve();
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

/**
 * Fallback download method
 */
downloadFallback(format) {
  const img = document.getElementById('generated-chart');
  if (img) {
    const link = document.createElement('a');
    link.download = `chart-${new Date().getTime()}.${format}`;
    link.href = img.src;
    link.click();
  } else {
    throw new Error('No chart available for download');
  }
}

/**
 * Show status message
 */
showStatus(message, container, textElement, type = 'info') {
  if (container && textElement) {
    container.style.display = 'block';
    textElement.textContent = message;
    textElement.className = `status-text ${type}`;
    
    // Auto-hide success messages
    if (type === 'success') {
      setTimeout(() => {
        container.style.display = 'none';
      }, 3000);
    }
  }
}
}

