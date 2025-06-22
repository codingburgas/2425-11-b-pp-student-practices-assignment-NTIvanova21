// Modern Flash Messages JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize flash messages
    initializeFlashMessages();
});

function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach((message, index) => {
        // Add delay for staggered animation
        message.style.animationDelay = `${index * 0.1}s`;
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            dismissFlashMessage(message);
        }, 5000);
        
        // Add click to dismiss functionality
        const closeBtn = message.querySelector('.flash-message-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissFlashMessage(message);
            });
        }
        
        // Add hover pause functionality
        let timeoutId;
        message.addEventListener('mouseenter', () => {
            clearTimeout(timeoutId);
            const progressBar = message.querySelector('.flash-message-progress-bar');
            if (progressBar) {
                progressBar.style.animationPlayState = 'paused';
            }
        });
        
        message.addEventListener('mouseleave', () => {
            const progressBar = message.querySelector('.flash-message-progress-bar');
            if (progressBar) {
                progressBar.style.animationPlayState = 'running';
            }
            timeoutId = setTimeout(() => {
                dismissFlashMessage(message);
            }, 2000); // Give 2 more seconds after hover
        });
    });
}

function dismissFlashMessage(message) {
    if (message.classList.contains('removing')) return;
    
    message.classList.add('removing');
    
    setTimeout(() => {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
        }
    }, 300);
}

// Function to create and show a new flash message programmatically
function showFlashMessage(message, category = 'info') {
    const container = document.querySelector('.flash-messages-container');
    if (!container) {
        createFlashContainer();
    }
    
    const messageElement = createFlashMessageElement(message, category);
    document.querySelector('.flash-messages-container').appendChild(messageElement);
    
    // Initialize the new message
    initializeFlashMessages();
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages-container';
    document.body.appendChild(container);
}

function createFlashMessageElement(message, category) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `flash-message ${category}`;
    
    const icons = {
        'success': '✓',
        'error': '✕',
        'warning': '⚠',
        'info': 'ℹ',
        'danger': '✕'
    };
    
    const icon = icons[category] || icons['info'];
    
    messageDiv.innerHTML = `
        <div class="flash-message-content">
            <div class="flash-message-icon">${icon}</div>
            <p class="flash-message-text">${message}</p>
            <button class="flash-message-close" aria-label="Close message">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="flash-message-progress">
            <div class="flash-message-progress-bar"></div>
        </div>
    `;
    
    return messageDiv;
}

// Export functions for global use
window.FlashMessages = {
    show: showFlashMessage,
    dismiss: dismissFlashMessage
}; 