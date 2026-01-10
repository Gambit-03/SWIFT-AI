// ✅ COMPLETE Universal Action Handlers for Swift AI Platform
// Real backend integration for ALL interactive buttons

// Global notification system
function showNotification(title, message, type = 'success') {
    const alertClass = type === 'success' ? 'alert-success' : type === 'error' ? 'alert-danger' : 'alert-info';
    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        <strong>${title}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 5000);
}

// ===== PROFILE MANAGEMENT =====
async function updateProfile(formData) {
    try {
        const response = await fetch('/api/profile', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Profile Updated', 'Your profile has been updated successfully.');
            return result;
        }
    } catch (e) {
        showNotification('Error', 'Failed to update profile', 'error');
        console.error(e);
    }
}

async function uploadProfilePhoto(fileInput) {
    try {
        const formData = new FormData();
        formData.append('photo', fileInput.files[0]);

        const response = await fetch('/api/profile/photo', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Photo Uploaded', 'Profile photo updated successfully.');
            return result.photo_url;
        }
    } catch (e) {
        showNotification('Error', 'Failed to upload photo', 'error');
        console.error(e);
    }
}

async function changePassword(currentPassword, newPassword) {
    try {
        const response = await fetch('/api/profile/password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Password Changed', 'Your password has been updated successfully.');
            return true;
        }
    } catch (e) {
        showNotification('Error', 'Failed to change password', 'error');
        console.error(e);
    }
}

// ===== AUDIT LOGS =====
async function fetchAuditLogs(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const response = await fetch(`/api/audit/logs?${params}`);
        const logs = await response.json();
        return logs;
    } catch (e) {
        showNotification('Error', 'Failed to fetch audit logs', 'error');
        console.error(e);
        return [];
    }
}

async function exportAuditPDF(filters = {}) {
    try {
        const response = await fetch('/api/audit/export/pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filters })
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Export Complete', 'Audit logs exported as PDF.');
            window.open(result.download_url, '_blank');
            return result;
        }
    } catch (e) {
        showNotification('Error', 'Failed to export PDF', 'error');
        console.error(e);
    }
}

async function exportAuditCSV(filters = {}) {
    try {
        const response = await fetch('/api/audit/export/csv', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filters })
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Export Complete', 'Audit logs exported as CSV.');
            window.open(result.download_url, '_blank');
            return result;
        }
    } catch (e) {
        showNotification('Error', 'Failed to export CSV', 'error');
        console.error(e);
    }
}

// ===== INTEGRATIONS MANAGEMENT =====
async function fetchIntegrations() {
    try {
        const response = await fetch('/api/integrations');
        const integrations = await response.json();
        return integrations;
    } catch (e) {
        showNotification('Error', 'Failed to fetch integrations', 'error');
        console.error(e);
        return [];
    }
}

async function addIntegration(formData) {
    try {
        const response = await fetch('/api/integrations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Integration Added', `${result.integration.name} is now active.`);
            return result.integration;
        }
    } catch (e) {
        showNotification('Error', 'Failed to add integration', 'error');
        console.error(e);
    }
}

async function updateIntegration(integrationId, formData) {
    try {
        const response = await fetch(`/api/integrations/${integrationId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Integration Updated', 'Integration has been updated.');
            return true;
        }
    } catch (e) {
        showNotification('Error', 'Failed to update integration', 'error');
        console.error(e);
    }
}

async function deleteIntegration(integrationId) {
    try {
        const response = await fetch(`/api/integrations/${integrationId}`, {
            method: 'DELETE'
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Integration Deleted', 'Integration has been removed.');
            return true;
        }
    } catch (e) {
        showNotification('Error', 'Failed to delete integration', 'error');
        console.error(e);
    }
}

async function testIntegration(integrationId) {
    try {
        const response = await fetch(`/api/integrations/${integrationId}/test`, {
            method: 'POST'
        });
        const result = await response.json();
        if (result.success) {
            const status = result.result.status;
            showNotification('Test Complete', `Integration test ${status}. Response time: ${result.result.response_time}`,
                status === 'Success' ? 'success' : 'error');
            return result.result;
        }
    } catch (e) {
        showNotification('Error', 'Failed to test integration', 'error');
        console.error(e);
    }
}

// ===== USER MANAGEMENT =====
async function fetchUsers() {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        return users;
    } catch (e) {
        showNotification('Error', 'Failed to fetch users', 'error');
        console.error(e);
        return [];
    }
}

async function createUser(formData) {
    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            const msg = result.user.invitation_sent
                ? `User created and invitation sent to ${result.user.email}`
                : `User ${result.user.name} created successfully`;
            showNotification('User Created', msg);
            return result.user;
        }
    } catch (e) {
        showNotification('Error', 'Failed to create user', 'error');
        console.error(e);
    }
}

async function updateUser(userId, formData) {
    try {
        const response = await fetch(`/api/users/${userId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            showNotification('User Updated', 'User information has been updated.');
            return true;
        }
    } catch (e) {
        showNotification('Error', 'Failed to update user', 'error');
        console.error(e);
    }
}

async function deleteUser(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`, {
            method: 'DELETE'
        });
        const result = await response.json();
        if (result.success) {
            showNotification('User Deleted', 'User has been removed from the system.');
            return true;
        }
    } catch (e) {
        showNotification('Error', 'Failed to delete user', 'error');
        console.error(e);
    }
}

async function blockUser(userId) {
    try {
        const response = await fetch(`/api/users/${userId}/block`, {
            method: 'POST'
        });
        const result = await response.json();
        if (result.success) {
            showNotification('User Blocked', 'User has been blocked successfully.');
            return true;
        }
    } catch (e) {
        showNotification('Error', 'Failed to block user', 'error');
        console.error(e);
    }
}

async function sendMessage(userId, subject, body) {
    try {
        const response = await fetch(`/api/users/${userId}/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ subject, body })
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Message Sent', 'Your message has been delivered.');
            return true;
        }
    } catch (e) {
        showNotification('Error', 'Failed to send message', 'error');
        console.error(e);
    }
}

async function resendInvitation(userId) {
    try {
        const response = await fetch(`/api/users/${userId}/resend-invitation`, {
            method: 'POST'
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Invitation Sent', 'Invitation has been resent to the user.');
            return true;
        }
    } catch (e) {
        showNotification('Error', 'Failed to resend invitation', 'error');
        console.error(e);
    }
}

// ===== EXISTING FUNCTIONS (from previous implementation) =====
async function createRule(formData) {
    try {
        const response = await fetch('/api/rules', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Rule Created', `Rule "${result.rule.name}" has been created successfully.`);
            return result.rule;
        }
    } catch (e) {
        showNotification('Error', 'Failed to create rule', 'error');
        console.error(e);
    }
}

async function generateReport(formData) {
    try {
        const response = await fetch('/api/reports/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Report Generated', `Report "${result.report.name}" is ready for download.`);
            window.open(result.download_url, '_blank');
            return result.report;
        }
    } catch (e) {
        showNotification('Error', 'Failed to generate report', 'error');
        console.error(e);
    }
}

async function exportData(dataType, format = 'PDF', filters = {}) {
    try {
        const response = await fetch(`/api/export/${dataType}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ format, filters })
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Export Complete', `${dataType} data exported as ${format}.`);
            window.open(result.download_url, '_blank');
            return result.export;
        }
    } catch (e) {
        showNotification('Error', 'Failed to export data', 'error');
        console.error(e);
    }
}

async function createAlert(formData) {
    try {
        const response = await fetch('/api/alerts/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            showNotification('Alert Created', `Manual alert ${result.alert.transaction_id} created.`);
            return result.alert;
        }
    } catch (e) {
        showNotification('Error', 'Failed to create alert', 'error');
        console.error(e);
    }
}

async function createProfile(formData, type = 'customer') {
    try {
        const endpoint = type === 'customer' ? '/api/customers/create' : '/api/users';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            const name = result.profile?.name || result.user?.name;
            showNotification('Profile Created', `${name} has been added to the system.`);
            return result.profile || result.user;
        }
    } catch (e) {
        showNotification('Error', 'Failed to create profile', 'error');
        console.error(e);
    }
}

// ===== UNIVERSAL MODAL HANDLER =====
function showActionModal(title, message, formFields = [], onConfirm) {
    const modal = document.getElementById('actionModal');
    if (!modal) return;

    document.getElementById('actionModalTitle').innerText = title;
    document.getElementById('actionModalMessage').innerText = message;

    const formContainer = document.getElementById('actionModalForm');
    if (formFields.length > 0) {
        formContainer.style.display = 'block';
        formContainer.innerHTML = formFields.map(field => `
            <div class="mb-3">
                <label class="form-label small fw-bold">${field.label}</label>
                ${field.type === 'textarea'
                ? `<textarea class="form-control" id="${field.id}" placeholder="${field.placeholder || ''}"></textarea>`
                : field.type === 'select'
                    ? `<select class="form-control" id="${field.id}">
                        ${field.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
                       </select>`
                    : `<input type="${field.type || 'text'}" class="form-control" id="${field.id}" placeholder="${field.placeholder || ''}">`
            }
            </div>
        `).join('');
    } else {
        formContainer.style.display = 'none';
    }

    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();

    document.getElementById('confirmActionBtn').onclick = async function () {
        const btn = this;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        btn.disabled = true;

        const formData = {};
        formFields.forEach(field => {
            formData[field.id] = document.getElementById(field.id).value;
        });

        await onConfirm(formData);

        btn.innerHTML = 'Proceed';
        btn.disabled = false;
        bsModal.hide();
    };
}

// ===== STREAM CONTROL =====
let streamPaused = false;
let streamInterval = null;

function toggleStream(fetchFunction, intervalMs = 2000) {
    const btn = document.getElementById('streamToggleBtn');
    if (!btn) return;

    if (streamPaused) {
        streamPaused = false;
        btn.innerHTML = '<i class="fas fa-pause me-2"></i>Pause Stream';
        btn.classList.remove('btn-success');
        btn.classList.add('btn-warning');
        streamInterval = setInterval(fetchFunction, intervalMs);
        showNotification('Stream Resumed', 'Live data streaming has been resumed.');
    } else {
        streamPaused = true;
        btn.innerHTML = '<i class="fas fa-play me-2"></i>Resume Stream';
        btn.classList.remove('btn-warning');
        btn.classList.add('btn-success');
        clearInterval(streamInterval);
        showNotification('Stream Paused', 'Live data streaming has been paused.');
    }
}

// ===== FILTER HANDLER =====
function applyFilters(filterData, fetchFunction) {
    showNotification('Filters Applied', 'Data has been filtered based on your criteria.');
    fetchFunction(filterData);
}

// Export all functions for global use
window.SwiftAI = {
    // Profile
    updateProfile,
    uploadProfilePhoto,
    changePassword,
    // Audit
    fetchAuditLogs,
    exportAuditPDF,
    exportAuditCSV,
    // Integrations
    fetchIntegrations,
    addIntegration,
    updateIntegration,
    deleteIntegration,
    testIntegration,
    // Users
    fetchUsers,
    createUser,
    updateUser,
    deleteUser,
    blockUser,
    sendMessage,
    resendInvitation,
    // Existing
    createRule,
    generateReport,
    exportData,
    createAlert,
    createProfile,
    showActionModal,
    toggleStream,
    applyFilters,
    showNotification
};
