/**
 * RedTox - Main JavaScript functionality
 */

/**
 * Reveals a toxic comment when the 'Reveal Comment' button is clicked.
 * @param {HTMLElement} button - The button element that was clicked.
 */
function revealComment(button) {
    const commentDiv = button.closest('.comment');
    const warningDiv = commentDiv.querySelector('.toxic-warning');
    const contentDiv = commentDiv.querySelector('.comment-content');
    
    // Hide warning and show content
    warningDiv.style.display = 'none';
    contentDiv.style.display = 'block';
}

/**
 * Initialize threshold slider functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize threshold slider on results page
    const thresholdSlider = document.getElementById('thresholdSlider');
    const thresholdValue = document.getElementById('thresholdValue');
    const viewWithThreshold = document.getElementById('viewWithThreshold');
    
    if (thresholdSlider && thresholdValue && viewWithThreshold) {
        thresholdSlider.addEventListener('input', function() {
            const value = parseFloat(this.value).toFixed(2);
            thresholdValue.textContent = value;
            
            // Update URL with threshold parameter
            const url = new URL(viewWithThreshold.href);
            url.searchParams.set('threshold', value);
            viewWithThreshold.href = url.toString();
        });
    }
    
    // Initialize threshold slider on thread view page
    const threadThresholdSlider = document.getElementById('thresholdSlider');
    const threadThresholdValue = document.getElementById('thresholdValue');
    const applyThresholdButton = document.getElementById('applyThreshold');
    
    if (threadThresholdSlider && threadThresholdValue && applyThresholdButton) {
        threadThresholdSlider.addEventListener('input', function() {
            const value = parseFloat(this.value).toFixed(2);
            threadThresholdValue.textContent = value;
        });
        
        applyThresholdButton.addEventListener('click', function() {
            const value = threadThresholdSlider.value;
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('threshold', value);
            window.location.href = currentUrl.toString();
        });
    }

    // Add animation effects to cards on hover
    const animateCards = () => {
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px)';
                card.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '0 4px 25px rgba(0, 0, 0, 0.25)';
            });
        });
    };
    
    // Add smooth transitions to stat cards
    const animateStatCards = () => {
        document.querySelectorAll('.stat-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'scale(1.03)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'scale(1)';
            });
        });
    };
    
    // Initialize tooltips from Bootstrap
    const initTooltips = () => {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    };
    
    // Add a subtle entrance animation to cards
    const addEntranceAnimations = () => {
        const cards = document.querySelectorAll('.card, .stat-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 + (index * 100));
        });
    };
    
    // Initialize interactive elements
    animateCards();
    animateStatCards();
    initTooltips();
    addEntranceAnimations();
    
    // Initialize toxic content toggles
    initToxicToggles();
});

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Add hover effects to cards
 */
function animateCards() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 6px 15px rgba(0, 0, 0, 0.6)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.5)';
        });
    });
}

/**
 * Add hover effects to stat cards
 */
function animateStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.05)';
            this.style.boxShadow = '0 6px 15px rgba(0, 0, 0, 0.6)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.5)';
        });
    });
}

/**
 * Add entrance animations to elements
 */
function addEntranceAnimations() {
    const cards = document.querySelectorAll('.card, .stat-card');
    
    cards.forEach((card, index) => {
        // Set initial styles
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease';
        
        // Apply staggered animation delay based on index
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 100));
    });
}

/**
 * Initialize toxic content toggle buttons
 */
function initToxicToggles() {
    const toggleButtons = document.querySelectorAll('.toggle-content');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const comment = this.closest('.comment');
            const toxicContent = comment.querySelector('.toxic-content');
            const isVisible = toxicContent.style.display !== 'none';
            
            if (isVisible) {
                toxicContent.style.display = 'none';
                this.textContent = 'Show Content';
                this.classList.remove('btn-danger');
                this.classList.add('btn-outline-danger');
            } else {
                toxicContent.style.display = 'block';
                this.textContent = 'Hide Content';
                this.classList.remove('btn-outline-danger');
                this.classList.add('btn-danger');
            }
        });
    });
}

/**
 * Update URL with new threshold value
 * @param {string} baseUrl - Base URL without threshold
 * @param {string} thresholdValue - Current threshold value
 * @param {HTMLElement} linkElement - Element to update href
 */
function updateThresholdLink(baseUrl, thresholdValue, linkElement) {
    if (!linkElement) return;
    
    // Extract the current URL parts
    const url = new URL(linkElement.href, window.location.origin);
    
    // Set the threshold parameter
    url.searchParams.set('threshold', thresholdValue);
    
    // Update the href
    linkElement.href = url.toString();
} 