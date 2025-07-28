// Copy to clipboard functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize toast
    const toastElement = document.getElementById('copyToast');
    const toast = new bootstrap.Toast(toastElement);

    // Add click event listeners to all copy buttons
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            
            // Use the modern Clipboard API
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    showCopySuccess();
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                    fallbackCopyText(textToCopy);
                });
            } else {
                // Fallback for older browsers or non-HTTPS
                fallbackCopyText(textToCopy);
            }
        });
    });

    function showCopySuccess() {
        toast.show();
        
        // Add visual feedback to the button
        const button = event.target.closest('.copy-btn');
        const originalIcon = button.innerHTML;
        button.innerHTML = '<i class="bi bi-check"></i>';
        button.classList.add('btn-success');
        button.classList.remove('btn-outline-primary', 'btn-outline-success', 'btn-outline-danger');
        
        setTimeout(() => {
            button.innerHTML = originalIcon;
            button.classList.remove('btn-success');
            if (button.closest('.card-header').classList.contains('bg-primary')) {
                button.classList.add('btn-outline-primary');
            } else if (button.closest('.card-header').classList.contains('bg-success')) {
                button.classList.add('btn-outline-success');
            } else if (button.closest('.card-header').classList.contains('bg-danger')) {
                button.classList.add('btn-outline-danger');
            }
        }, 1000);
    }

    function fallbackCopyText(text) {
        // Create a temporary textarea element
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            showCopySuccess();
        } catch (err) {
            console.error('Failed to copy text: ', err);
            alert('Failed to copy text. Please select and copy manually.');
        } finally {
            document.body.removeChild(textArea);
        }
    }

    // Auto-focus on the concept textarea when page loads
    const conceptTextarea = document.getElementById('concept');
    if (conceptTextarea) {
        conceptTextarea.focus();
    }

    // Add some visual enhancements for better UX
    document.querySelectorAll('textarea[readonly], input[readonly]').forEach(element => {
        element.addEventListener('click', function() {
            this.select();
        });
    });

    // Add hover effects for copy buttons
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.setAttribute('title', 'Click to copy');
        });
    });
});

// Form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[action*="generate"]');
    if (form) {
        form.addEventListener('submit', function(e) {
            const conceptInput = document.getElementById('concept');
            if (conceptInput && conceptInput.value.trim().length < 3) {
                e.preventDefault();
                alert('Please enter a more detailed creative concept (at least 3 characters).');
                conceptInput.focus();
                return false;
            }
            
            // Show loading state
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Generating...';
                submitButton.disabled = true;
            }
        });
    }
});
