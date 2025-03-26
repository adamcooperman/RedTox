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
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length) {
        [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
}

/**
 * Add hover animation effects to cards
 */
function animateCards() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.6)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.5)';
        });
    });
}

/**
 * Add hover animation effects to stat cards
 */
function animateStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.6)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.5)';
        });
    });
}

/**
 * Add entrance animations to elements
 */
function addEntranceAnimations() {
    const elements = document.querySelectorAll('.card, .stat-card, .comment');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        // Add a staggered delay based on index
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 100 + (index * 50)); // 100ms base delay + 50ms per item
    });
}

/**
 * Initialize toggle buttons for toxic content 
 */
function initToxicToggles() {
    // Global toggle for all toxic content
    const globalToggleBtn = document.querySelector('.toggle-toxic-btn');
    if (globalToggleBtn) {
        globalToggleBtn.addEventListener('click', function() {
            const state = this.getAttribute('data-state');
            const toxicContents = document.querySelectorAll('.toxic-content');
            const toxicWarnings = document.querySelectorAll('.toxic-warning');
            const toggleButtons = document.querySelectorAll('.toggle-content');
            
            if (state === 'hide') {
                // Show all toxic content
                toxicContents.forEach(content => content.style.display = 'block');
                toxicWarnings.forEach(warning => warning.style.display = 'none');
                toggleButtons.forEach(btn => {
                    btn.textContent = 'Hide Content';
                    btn.classList.remove('btn-outline-danger');
                    btn.classList.add('btn-danger');
                });
                
                this.innerHTML = '<i class="bi bi-eye me-1"></i>Hide All Toxic Comments';
                this.setAttribute('data-state', 'show');
            } else {
                // Hide all toxic content
                toxicContents.forEach(content => content.style.display = 'none');
                toxicWarnings.forEach(warning => warning.style.display = 'block');
                toggleButtons.forEach(btn => {
                    btn.textContent = 'Show Content';
                    btn.classList.remove('btn-danger');
                    btn.classList.add('btn-outline-danger');
                });
                
                this.innerHTML = '<i class="bi bi-eye-slash me-1"></i>Show All Toxic Comments';
                this.setAttribute('data-state', 'hide');
            }
        });
    }
    
    // Individual toggle buttons
    const toggleButtons = document.querySelectorAll('.toggle-content');
    if (toggleButtons.length > 0) {
        console.log('Initializing ' + toggleButtons.length + ' toggle buttons');
        
        toggleButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault(); // Prevent default button behavior
                console.log('Toggle button clicked');
                
                const warningDiv = this.closest('.toxic-warning');
                const commentDiv = this.closest('.comment');
                const contentDiv = commentDiv.querySelector('.toxic-content');
                
                console.log('Warning div:', warningDiv);
                console.log('Content div:', contentDiv);
                
                if (contentDiv.style.display === 'none' || getComputedStyle(contentDiv).display === 'none') {
                    // Show content
                    contentDiv.style.display = 'block';
                    this.textContent = 'Hide Content';
                    this.classList.remove('btn-outline-danger');
                    this.classList.add('btn-danger');
                } else {
                    // Hide content
                    contentDiv.style.display = 'none';
                    this.textContent = 'Show Content';
                    this.classList.remove('btn-danger');
                    this.classList.add('btn-outline-danger');
                }
            });
        });
    }
}

/**
 * Update URL with new threshold value
 */
function updateThresholdLink(threshold) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('threshold', threshold);
    window.location.href = currentUrl.toString();
} 