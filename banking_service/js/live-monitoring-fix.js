// ✅ LIVE MONITORING - Stream Control & Filters
// Add this script to live-monitoring.html before </body>

let streamPaused = false;
let txnInterval, statsInterval;

function toggleStreamControl() {
    const btn = document.getElementById('streamToggleBtn');
    if (streamPaused) {
        // Resume
        streamPaused = false;
        btn.innerHTML = '<i class="fas fa-pause me-2"></i>Pause Stream';
        btn.classList.remove('btn-success');
        btn.classList.add('btn-warning');
        txnInterval = setInterval(fetchTransactions, 2000);
        statsInterval = setInterval(updateLiveStats, 4000);
        showNotification('Stream Resumed', 'Live monitoring resumed');
    } else {
        // Pause
        streamPaused = true;
        btn.innerHTML = '<i class="fas fa-play me-2"></i>Resume Stream';
        btn.classList.remove('btn-warning');
        btn.classList.add('btn-success');
        clearInterval(txnInterval);
        clearInterval(statsInterval);
        showNotification('Stream Paused', 'Live monitoring paused');
    }
}

function handleFilters() {
    const filters = prompt('Enter status filter (All/Blocked/Review/Approved):', 'All');
    if (filters) {
        showNotification('Filter Applied', `Showing ${filters} transactions`);
    }
}

function showNotification(title, message) {
    const notification = document.createElement('div');
    notification.className = 'alert alert-info alert-dismissible fade show position-fixed top-0 end-0 m-3';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        <strong>${title}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}
