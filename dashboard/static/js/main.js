// SkiOx Dashboard - Main JavaScript

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    setupWebsocket();
    setupAutoRefresh();
    setupEventHandlers();
}

/**
 * Setup WebSocket connection for real-time updates
 */
function setupWebsocket() {
    // Placeholder for WebSocket implementation
    // This would connect to a WebSocket server for real-time updates
    console.log('WebSocket support ready');
}

/**
 * Setup auto-refresh intervals
 */
function setupAutoRefresh() {
    // Different refresh rates for different components
    setInterval(refreshSystemStatus, 5000);     // Every 5 seconds
    setInterval(refreshBatteryStatus, 5000);    // Every 5 seconds
    setInterval(refreshAlerts, 10000);          // Every 10 seconds
    setInterval(refreshComponentStatus, 10000); // Every 10 seconds
}

/**
 * Setup event handlers
 */
function setupEventHandlers() {
    // Add global event listeners
    document.addEventListener('click', handleGlobalClick);
    document.addEventListener('keydown', handleGlobalKeydown);
}

/**
 * Refresh system status
 */
function refreshSystemStatus() {
    fetch('/api/system/current_status/')
        .then(response => response.json())
        .then(data => {
            updateSystemStatus(data);
        })
        .catch(error => console.warn('System status unavailable:', error));
}

/**
 * Refresh battery status
 */
function refreshBatteryStatus() {
    fetch('/api/battery/current_battery/')
        .then(response => response.json())
        .then(data => {
            updateBatteryStatus(data);
        })
        .catch(error => console.warn('Battery status unavailable:', error));
}

/**
 * Refresh alerts
 */
function refreshAlerts() {
    fetch('/api/alerts/unresolved_alerts/')
        .then(response => response.json())
        .then(data => {
            updateAlertsDisplay(data);
        })
        .catch(error => console.warn('Alerts unavailable:', error));
}

/**
 * Refresh component status
 */
function refreshComponentStatus() {
    fetch('/api/components/active_components/')
        .then(response => response.json())
        .then(data => {
            updateComponentsDisplay(data);
        })
        .catch(error => console.warn('Components unavailable:', error));
}

/**
 * Update system status display
 */
function updateSystemStatus(data) {
    // Update system state badge
    const stateElements = document.querySelectorAll('[data-system-state]');
    stateElements.forEach(el => {
        el.textContent = data.system_state_display;
        el.className = 'badge bg-' + getStateColor(data.system_state);
    });

    // Update oxygen delivery status
    const oxygenElements = document.querySelectorAll('[data-oxygen-status]');
    oxygenElements.forEach(el => {
        el.textContent = data.oxygen_delivery_active ? 'Active' : 'Inactive';
        el.className = 'badge bg-' + (data.oxygen_delivery_active ? 'danger' : 'success');
    });
}

/**
 * Update battery status display
 */
function updateBatteryStatus(data) {
    const batteryElements = document.querySelectorAll('[data-battery-percentage]');
    batteryElements.forEach(el => {
        const percentage = data.battery_percentage;
        el.textContent = percentage + '%';
        el.style.width = percentage + '%';
        el.className = 'progress-bar bg-' + getBatteryColor(percentage);
    });
}

/**
 * Update alerts display
 */
function updateAlertsDisplay(alerts) {
    const alertBadge = document.querySelector('[data-alerts-count]');
    if (alertBadge) {
        const count = alerts.length;
        alertBadge.textContent = count;
        alertBadge.style.display = count > 0 ? 'inline-block' : 'none';
    }
}

/**
 * Update components display
 */
function updateComponentsDisplay(components) {
    const componentCount = document.querySelector('[data-active-components]');
    if (componentCount) {
        componentCount.textContent = components.length;
    }
}

/**
 * Get color class for system state
 */
function getStateColor(state) {
    const colors = {
        'IDLE': 'secondary',
        'MONITORING': 'info',
        'DELIVERING': 'warning',
        'ERROR': 'danger',
        'SHUTDOWN': 'dark'
    };
    return colors[state] || 'secondary';
}

/**
 * Get color class for battery percentage
 */
function getBatteryColor(percentage) {
    if (percentage > 60) return 'success';
    if (percentage > 30) return 'warning';
    return 'danger';
}

/**
 * Handle global clicks
 */
function handleGlobalClick(event) {
    // Handle any global click events
    const target = event.target;

    // Close dropdowns on click outside
    if (!target.closest('.dropdown-menu')) {
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });
    }
}

/**
 * Handle global keydown
 */
function handleGlobalKeydown(event) {
    // Close modals on Escape key
    if (event.key === 'Escape') {
        document.querySelectorAll('.modal.show').forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        });
    }

    // Global keyboard shortcuts
    if (event.ctrlKey || event.metaKey) {
        if (event.key === 'k' || event.key === 'K') {
            event.preventDefault();
            // Open search/command palette
        }
        if (event.key === 'r' || event.key === 'R') {
            event.preventDefault();
            // Refresh dashboard
            location.reload();
        }
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const alertContainer = document.querySelector('.messages') || 
                          document.querySelector('.container-fluid');
    if (alertContainer) {
        alertContainer.insertAdjacentHTML('afterbegin', alertHtml);
    }
}

/**
 * Format date
 */
function formatDate(date) {
    return new Date(date).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

/**
 * Format time
 */
function formatTime(date) {
    return new Date(date).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

/**
 * Debounce function
 */
function debounce(func, wait) {
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

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * API helper functions
 */
const API = {
    /**
     * Make API request
     */
    request: async (url, options = {}) => {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        };

        const fetchOptions = { ...defaultOptions, ...options };
        try {
            const response = await fetch(url, fetchOptions);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    /**
     * GET request
     */
    get: (url) => API.request(url),

    /**
     * POST request
     */
    post: (url, data) => API.request(url, {
        method: 'POST',
        body: JSON.stringify(data)
    }),

    /**
     * PUT request
     */
    put: (url, data) => API.request(url, {
        method: 'PUT',
        body: JSON.stringify(data)
    }),

    /**
     * PATCH request
     */
    patch: (url, data) => API.request(url, {
        method: 'PATCH',
        body: JSON.stringify(data)
    }),

    /**
     * DELETE request
     */
    delete: (url) => API.request(url, { method: 'DELETE' })
};

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Export functions for use in other modules
window.dashboardUtils = {
    showNotification,
    formatDate,
    formatTime,
    debounce,
    throttle,
    API,
    getCookie
};
