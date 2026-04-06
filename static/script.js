// Task Pilot - Enhanced JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    initializeApp();

    // Add loading screen fade out
    setTimeout(() => {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.style.display = 'none';
        }
    }, 2500);

    // Add smooth scrolling
    initializeSmoothScrolling();

    // Add form enhancements
    initializeFormEnhancements();

    // Add task card animations
    initializeTaskAnimations();

    // Add progress bar animations
    initializeProgressAnimations();
});

function initializeApp() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }

    // Add intersection observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-in-left');
            }
        });
    }, observerOptions);

    // Observe elements for scroll animations
    document.querySelectorAll('.task-card, .form-container, .progress-section').forEach(el => {
        observer.observe(el);
    });
}

function initializeSmoothScrolling() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeFormEnhancements() {
    // Add floating label effect
    const formInputs = document.querySelectorAll('.form-input');

    formInputs.forEach(input => {
        // Add focus/blur handlers
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });

        // Check initial state
        if (input.value) {
            input.parentElement.classList.add('focused');
        }

        // Add input validation feedback
        input.addEventListener('input', function() {
            validateInput(this);
        });
    });

    // Enhance buttons with ripple effect
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
    });
}

function validateInput(input) {
    const value = input.value.trim();
    const isValid = value.length > 0;

    input.classList.toggle('valid', isValid);
    input.classList.toggle('invalid', !isValid && input.hasAttribute('required'));
}

function createRippleEffect(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple-effect');

    element.appendChild(ripple);

    setTimeout(() => {
        ripple.remove();
    }, 600);
}

function initializeTaskAnimations() {
    // Add hover effects for task cards
    document.querySelectorAll('.task-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add click animations for action buttons
    document.querySelectorAll('.task-actions .btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
}

function initializeProgressAnimations() {
    // Animate progress bars on page load
    document.querySelectorAll('.progress-fill').forEach(fill => {
        const width = fill.style.width;
        fill.style.width = '0%';
        setTimeout(() => {
            fill.style.width = width;
        }, 500);
    });

    // Animate task progress bars
    document.querySelectorAll('.task-progress-fill').forEach(fill => {
        const width = fill.style.width;
        fill.style.width = '0%';
        setTimeout(() => {
            fill.style.width = width;
        }, 800);
    });
}

// Utility functions
function showAlert(message, type = 'success', duration = 3000) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        ${message}
    `;

    const container = document.querySelector('.content-wrapper');
    container.insertBefore(alert, container.firstChild);

    // Animate in
    setTimeout(() => alert.classList.add('bounce-in'), 10);

    // Auto remove
    setTimeout(() => {
        alert.style.animation = 'slideDown 0.3s ease-in reverse';
        setTimeout(() => alert.remove(), 300);
    }, duration);
}

function toggleLoading(element, show = true) {
    if (show) {
        element.classList.add('loading');
        element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        element.disabled = true;
    } else {
        element.classList.remove('loading');
        element.disabled = false;
    }
}

// Add CSS for additional animations
const additionalStyles = `
<style>
.form-group.focused .form-label {
    color: var(--primary);
    transform: translateY(-2px);
    font-weight: 600;
}

.form-input.valid {
    border-color: var(--success);
}

.form-input.invalid {
    border-color: var(--error);
}

.ripple-effect {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    transform: scale(0);
    animation: ripple 0.6s linear;
    pointer-events: none;
}

@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.btn.loading {
    pointer-events: none;
    position: relative;
}

.btn.loading::after {
    content: '';
    position: absolute;
    width: 16px;
    height: 16px;
    margin: auto;
    border: 2px solid transparent;
    border-top-color: currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

.task-card.completed {
    opacity: 0.7;
}

.task-card.completed .task-title {
    text-decoration: line-through;
    color: var(--gray-500);
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
`;

// Inject additional styles
document.head.insertAdjacentHTML('beforeend', additionalStyles);

// Export functions for global use
window.TaskPilot = {
    showAlert,
    toggleLoading
};