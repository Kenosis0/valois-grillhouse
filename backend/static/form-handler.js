/**
 * Shared form submission handler for all Valois Grillhouse forms.
 * Handles validation, submission, success/error feedback, and duplicate prevention.
 */

class FormHandler {
  constructor(formId, endpoint, fieldMapping) {
    this.form = document.getElementById(formId);
    this.endpoint = endpoint;
    this.fieldMapping = fieldMapping; // { htmlInputName: apiFieldName }
    this.isSubmitting = false;
    
    if (!this.form) {
      console.error(`Form with ID '${formId}' not found`);
      return;
    }
    
    this.init();
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
      const apiName = this.fieldMapping[htmlName] || htmlName;
      data[apiName] = htmlValue.trim();
    }
    
    return data;
  }
  
  /**
   * Validate required fields client-side.
   */
  validateClientSide(data, requiredFields) {
    const errors = [];
    for (let field of requiredFields) {
      if (!data[field] || data[field].trim() === '') {
        errors.push(`${field} is required`);
      }
    }
    return errors;
  }
  
  /**
   * Display validation error message to user.
   */
  showError(message) {
    // Remove old error if exists
    const oldError = this.form.querySelector('.form-error');
    if (oldError) oldError.remove();
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.style.cssText = `
      color: #dc3545;
      background-color: #f8d7da;
      border: 1px solid #f5c6cb;
      border-radius: 4px;
      padding: 12px;
      margin-bottom: 20px;
    `;
    errorDiv.textContent = message;
    
    this.form.insertBefore(errorDiv, this.form.firstChild);
  }
  
  /**
   * Display success message to user.
   */
  showSuccess(message) {
    // Remove old success if exists
    const oldSuccess = this.form.querySelector('.form-success');
    if (oldSuccess) oldSuccess.remove();
    
    const successDiv = document.createElement('div');
    successDiv.className = 'form-success';
    successDiv.style.cssText = `
      color: #155724;
      background-color: #d4edda;
      border: 1px solid #c3e6cb;
      border-radius: 4px;
      padding: 12px;
      margin-bottom: 20px;
    `;
    successDiv.textContent = message;
    
    this.form.insertBefore(successDiv, this.form.firstChild);
  }
  
  /**
   * Disable all form inputs during submission.
   */
  disableForm() {
    const inputs = this.form.querySelectorAll('input, textarea, select, button');
    inputs.forEach(input => input.disabled = true);
  }
  
  /**
   * Enable all form inputs after submission.
   */
  enableForm() {
    const inputs = this.form.querySelectorAll('input, textarea, select, button');
    inputs.forEach(input => input.disabled = false);
  }
  
  /**
   * Clear all form fields.
   */
  clearForm() {
    this.form.reset();
  }
  
  /**
   * Main form submission handler.
   */
  async handleSubmit(e) {
    e.preventDefault();
    
    // Prevent duplicate submissions
    if (this.isSubmitting) {
      return;
    }
    
    // Collect and validate data
    const data = this.collectData();
    const requiredFields = Object.values(this.fieldMapping);
    const errors = this.validateClientSide(data, requiredFields);
    
    if (errors.length > 0) {
      this.showError(errors.join('; '));
      return;
    }
    
    // Mark as submitting and disable form
    this.isSubmitting = true;
    this.disableForm();
    
    try {
      // Send to backend
      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      
      const result = await response.json();
      
      if (response.ok) {
        // Success
        this.showSuccess(result.message || 'Form submitted successfully.');
        this.clearForm();
      } else {
        // Error from server
        this.showError(result.error || 'An error occurred. Please try again.');
      }
    
    } catch (error) {
      // Network or parsing error
      this.showError('Network error. Please check your connection and try again.');
      console.error('Fetch error:', error);
    
    } finally {
      // Re-enable form
      this.isSubmitting = false;
      this.enableForm();
    }
  }
}
