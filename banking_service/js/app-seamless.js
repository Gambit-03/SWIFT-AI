
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        if (themeIcon) {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.add('dark-mode');
        if (themeIcon) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
        localStorage.setItem('theme', 'dark');
    }
}

function showAction(title, message, showForm = false) {
    const modalElement = document.getElementById('actionModal');
    if (!modalElement) {
        console.warn('Action Modal container not found in document');
        alert(message);
        return;
    }

    document.getElementById('actionModalTitle').innerText = title;
    document.getElementById('actionModalMessage').innerText = message;

    const formElement = document.getElementById('actionModalForm');
    if (formElement) formElement.style.display = showForm ? 'block' : 'none';

    const modal = new bootstrap.Modal(modalElement);
    modal.show();

    const confirmBtn = document.getElementById('confirmActionBtn');
    if (confirmBtn) {
        confirmBtn.onclick = function () {
            const btn = this;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            btn.disabled = true;
            setTimeout(() => {
                const modalInstance = bootstrap.Modal.getInstance(modalElement);
                if (modalInstance) modalInstance.hide();

                showNotification('Complete', 'System updated successfully');

                btn.innerHTML = 'Proceed';
                btn.disabled = false;
            }, 1500);
        };
    }
}

function showNotification(title, message) {
    const notification = document.createElement('div');
    notification.className = 'toast-notification';
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-check-circle text-success me-3 fs-3"></i>
            <div>
                <strong class="d-block">${title}</strong>
                <small>${message}</small>
            </div>
        </div>
    `;
    document.body.appendChild(notification);

    setTimeout(() => notification.classList.add('show'), 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

function setupNavigation() {
    const path = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link, .dropdown-item');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === path) {
            link.classList.add('active');
            const parent = link.closest('.dropdown');
            if (parent) {
                const toggler = parent.querySelector('.dropdown-toggle');
                if (toggler) toggler.classList.add('active');
            }
        } else if (path === 'bank-portal.html' && href === '#') {
            // Handle "More" dropdown when in bank portal if necessary
        } else {
            link.classList.remove('active');
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
    }
    setupNavigation();
});
