/**
 * Shared form submission and mobile navigation handler for Valois Grillhouse.
 * Handles validation, submission, success/error feedback, duplicate prevention,
 * dynamic Curbside/Delivery mode switching, and mobile browser navigation.
 */

class FormHandler {
  constructor(formId, endpoint, fieldMapping) {
    this.form = document.getElementById(formId);
    this.endpoint = this.resolveEndpoint(endpoint);
    this.fieldMapping = fieldMapping; // { htmlInputName: apiFieldName }
    this.isSubmitting = false;
    
    if (!this.form) {
      console.error(`Form with ID '${formId}' not found`);
      return;
    }
    
    this.init();
  }
  
  /**
   * Resolve API endpoint so it works on localhost, LAN mobile testing, or file://
   */
  resolveEndpoint(endpoint) {
    try {
      if (window.location.protocol.startsWith('http') && endpoint.includes('127.0.0.1:5000')) {
        const host = window.location.hostname || '127.0.0.1';
        return endpoint.replace('127.0.0.1', host);
      }
    } catch (e) {
      // Fallback to original endpoint
    }
    return endpoint;
  }

  /**
   * Update endpoint and field mapping dynamically (used by Curbside / Delivery toggle).
   */
  setConfig(endpoint, fieldMapping) {
    this.endpoint = this.resolveEndpoint(endpoint);
    this.fieldMapping = fieldMapping;
  }
  
  init() {
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
  }
  
  /**
   * Collect form data and map to API field names.
   */
  collectData() {
    const formData = new FormData(this.form);
    const data = {};
    
    for (let [htmlName, htmlValue] of formData.entries()) {
      if (this.fieldMapping && !(htmlName in this.fieldMapping)) {
        continue;
      }
      const apiName = (this.fieldMapping && this.fieldMapping[htmlName]) || htmlName;
      data[apiName] = String(htmlValue).trim();
    }
    
    return data;
  }
  
  /**
   * Validate required fields client-side based on active required inputs.
   */
  validateClientSide(data) {
    const errors = [];
    for (let [htmlName, apiName] of Object.entries(this.fieldMapping)) {
      const fieldEl = this.form.elements[htmlName];
      const isRequired = fieldEl ? fieldEl.required && !fieldEl.disabled : true;
      if (isRequired && (!data[apiName] || data[apiName].trim() === '')) {
        errors.push(`${apiName.replace(/_/g, ' ')} is required`);
      }
    }
    return errors;
  }
  
  /**
   * Display validation error message to user.
   */
  showError(message) {
    const oldError = this.form.querySelector('.form-error');
    if (oldError) oldError.remove();
    const oldSuccess = this.form.querySelector('.form-success');
    if (oldSuccess) oldSuccess.remove();
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.style.cssText = `
      grid-column: 1 / -1;
      color: #842029;
      background-color: #f8d7da;
      border: 1px solid #f5c2c7;
      border-radius: 4px;
      padding: 12px 16px;
      margin-bottom: 10px;
      font-size: 0.92rem;
    `;
    errorDiv.textContent = message;
    
    this.form.insertBefore(errorDiv, this.form.firstChild);
  }
  
  /**
   * Display success message to user.
   */
  showSuccess(message) {
    const oldSuccess = this.form.querySelector('.form-success');
    if (oldSuccess) oldSuccess.remove();
    const oldError = this.form.querySelector('.form-error');
    if (oldError) oldError.remove();
    
    const successDiv = document.createElement('div');
    successDiv.className = 'form-success';
    successDiv.style.cssText = `
      grid-column: 1 / -1;
      color: #0f5132;
      background-color: #d1e7dd;
      border: 1px solid #badbcc;
      border-radius: 4px;
      padding: 12px 16px;
      margin-bottom: 10px;
      font-size: 0.92rem;
    `;
    successDiv.textContent = message;
    
    this.form.insertBefore(successDiv, this.form.firstChild);
  }
  
  /**
   * Disable all form inputs during submission.
   */
  disableForm() {
    const inputs = this.form.querySelectorAll('input, textarea, select, button');
    inputs.forEach(input => {
      input.dataset.wasDisabled = input.disabled ? 'true' : 'false';
      input.disabled = true;
    });
  }
  
  /**
   * Enable form inputs after submission, preserving intentionally disabled fields.
   */
  enableForm() {
    const inputs = this.form.querySelectorAll('input, textarea, select, button');
    inputs.forEach(input => {
      if (input.dataset.wasDisabled !== 'true') {
        input.disabled = false;
      }
      delete input.dataset.wasDisabled;
    });
  }
  
  /**
   * Clear all form fields.
   */
  clearForm() {
    this.form.reset();
    if (typeof this.onReset === 'function') {
      this.onReset();
    }
  }
  
  /**
   * Main form submission handler.
   */
  async handleSubmit(e) {
    e.preventDefault();
    
    if (this.isSubmitting) {
      return;
    }
    
    const data = this.collectData();
    const errors = this.validateClientSide(data);
    
    if (errors.length > 0) {
      this.showError(errors.join('; '));
      return;
    }
    
    this.isSubmitting = true;
    this.disableForm();
    
    try {
      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      
      const result = await response.json();
      
      if (response.ok) {
        this.showSuccess(result.message || 'Form submitted successfully.');
        this.clearForm();
      } else {
        this.showError(result.error || 'An error occurred. Please try again.');
      }
    
    } catch (error) {
      this.showError('Network error. Please make sure the backend server is running and try again.');
      console.error('Fetch error:', error);
    
    } finally {
      this.isSubmitting = false;
      this.enableForm();
    }
  }
}

/**
 * Initialize responsive mobile navigation bar across all pages.
 */
function initMobileNav() {
  const navbar = document.querySelector('.navbar');
  const nav = navbar ? navbar.querySelector('nav') : null;
  if (!navbar || !nav) return;

  // Avoid duplicate button injection
  if (navbar.querySelector('.nav-toggle')) return;

  const toggleBtn = document.createElement('button');
  toggleBtn.type = 'button';
  toggleBtn.className = 'nav-toggle';
  toggleBtn.setAttribute('aria-expanded', 'false');
  toggleBtn.setAttribute('aria-label', 'Toggle navigation menu');
  toggleBtn.innerHTML = '<span class="nav-toggle-bar"></span><span class="nav-toggle-bar"></span><span class="nav-toggle-bar"></span>';

  navbar.insertBefore(toggleBtn, nav);

  toggleBtn.addEventListener('click', () => {
    const isOpen = navbar.classList.toggle('nav-open');
    toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  // Close menu when clicking a link
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navbar.classList.remove('nav-open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    });
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navbar.classList.contains('nav-open')) {
      navbar.classList.remove('nav-open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });
}

document.addEventListener('DOMContentLoaded', initMobileNav);
