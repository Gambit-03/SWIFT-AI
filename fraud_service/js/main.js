// Page Templates
const pages = {
    dashboard: `
        <div class="dashboard-page fade-in">
            <div class="stats-grid grid grid-4">
                <div class="stat-card card">
                    <div class="stat-icon" style="background: linear-gradient(135deg, rgba(255, 107, 107, 0.2), rgba(255, 107, 107, 0.05)); color: var(--accent-danger);">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div class="stat-content">
                        <h3 class="stat-value">247</h3>
                        <p class="stat-label">Live Fraud Alerts</p>
                        <span class="stat-change danger"><i class="fas fa-arrow-up"></i> 12% vs yesterday</span>
                    </div>
                </div>

                <div class="stat-card card">
                    <div class="stat-icon" style="background: linear-gradient(135deg, rgba(255, 169, 77, 0.2), rgba(255, 169, 77, 0.05)); color: var(--accent-warning);">
                        <i class="fas fa-shield-halved"></i>
                    </div>
                    <div class="stat-content">
                        <h3 class="stat-value">1,842</h3>
                        <p class="stat-label">High-Risk Transactions</p>
                        <span class="stat-change warning"><i class="fas fa-arrow-up"></i> 8% vs yesterday</span>
                    </div>
                </div>

                <div class="stat-card card">
                    <div class="stat-icon" style="background: linear-gradient(135deg, rgba(81, 207, 102, 0.2), rgba(81, 207, 102, 0.05)); color: var(--accent-success);">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <div class="stat-content">
                        <h3 class="stat-value">45,231</h3>
                        <p class="stat-label">Approved Transactions</p>
                        <span class="stat-change success"><i class="fas fa-arrow-down"></i> 3% vs yesterday</span>
                    </div>
                </div>

                <div class="stat-card card">
                    <div class="stat-icon" style="background: linear-gradient(135deg, rgba(78, 205, 196, 0.2), rgba(78, 205, 196, 0.05)); color: var(--accent-secondary);">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <div class="stat-content">
                        <h3 class="stat-value">1,247/s</h3>
                        <p class="stat-label">Transactions Per Second</p>
                        <span class="stat-change info"><i class="fas fa-minus"></i> Stable</span>
                    </div>
                </div>
            </div>

            <div class="dashboard-grid grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Fraud Detection Overview</h2>
                        <div class="card-actions">
                            <button class="btn btn-secondary btn-sm">
                                <i class="fas fa-filter"></i> Filter
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <canvas id="fraudTrendChart" style="max-height: 300px;"></canvas>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Risk Distribution</h2>
                        <div class="card-actions">
                            <button class="btn btn-secondary btn-sm">
                                <i class="fas fa-download"></i> Export
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <canvas id="riskDistributionChart" style="max-height: 300px;"></canvas>
                    </div>
                </div>
            </div>

            <div class="dashboard-grid grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Fraud by Location</h2>
                    </div>
                    <div class="card-body">
                        <div id="fraudMap" style="height: 350px; background: var(--bg-tertiary); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
                            <div style="text-align: center; color: var(--text-muted);">
                                <i class="fas fa-map-marked-alt" style="font-size: 3rem; margin-bottom: 1rem; color: var(--accent-secondary);"></i>
                                <p>Interactive fraud heatmap</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Recent Critical Alerts</h2>
                        <a href="#" class="view-all-link">View All <i class="fas fa-arrow-right"></i></a>
                    </div>
                    <div class="card-body">
                        <div class="alerts-list">
                            <div class="alert-item">
                                <div class="alert-icon danger">
                                    <i class="fas fa-exclamation-circle"></i>
                                </div>
                                <div class="alert-content">
                                    <h4>Suspicious Transaction Detected</h4>
                                    <p>User #45821 - $15,420 from Nigeria</p>
                                    <span class="alert-time">2 minutes ago</span>
                                </div>
                                <span class="badge-status badge-danger">Critical</span>
                            </div>
                            <div class="alert-item">
                                <div class="alert-icon warning">
                                    <i class="fas fa-shield-alt"></i>
                                </div>
                                <div class="alert-content">
                                    <h4>Unusual Velocity Pattern</h4>
                                    <p>User #32109 - 15 transactions in 3 minutes</p>
                                    <span class="alert-time">8 minutes ago</span>
                                </div>
                                <span class="badge-status badge-warning">High</span>
                            </div>
                            <div class="alert-item">
                                <div class="alert-icon warning">
                                    <i class="fas fa-location-dot"></i>
                                </div>
                                <div class="alert-content">
                                    <h4>Geo-Velocity Anomaly</h4>
                                    <p>User #78234 - Location jump: NY → Tokyo (2 hrs)</p>
                                    <span class="alert-time">15 minutes ago</span>
                                </div>
                                <span class="badge-status badge-warning">High</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Model Performance Metrics</h2>
                    <div class="metric-tabs">
                        <button class="metric-tab active">Today</button>
                        <button class="metric-tab">Week</button>
                        <button class="metric-tab">Month</button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="metrics-grid grid grid-4">
                        <div class="metric-box">
                            <div class="metric-label">Detection Accuracy</div>
                            <div class="metric-value" style="color: var(--accent-success);">98.7%</div>
                            <div class="metric-bar">
                                <div class="metric-fill" style="width: 98.7%; background: var(--accent-success);"></div>
                            </div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">False Positive Rate</div>
                            <div class="metric-value" style="color: var(--accent-success);">1.2%</div>
                            <div class="metric-bar">
                                <div class="metric-fill" style="width: 1.2%; background: var(--accent-success);"></div>
                            </div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">Avg Detection Latency</div>
                            <div class="metric-value" style="color: var(--accent-secondary);">47ms</div>
                            <div class="metric-bar">
                                <div class="metric-fill" style="width: 85%; background: var(--accent-secondary);"></div>
                            </div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">Model Confidence</div>
                            <div class="metric-value" style="color: var(--accent-success);">96.3%</div>
                            <div class="metric-bar">
                                <div class="metric-fill" style="width: 96.3%; background: var(--accent-success);"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,

    'live-monitoring': `
        <div class="live-monitoring-page fade-in">
            <div class="page-header">
                <h2>Live Transaction Monitoring</h2>
                <div class="header-controls">
                    <button class="btn btn-secondary">
                        <i class="fas fa-pause"></i> Pause Stream
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filters
                    </button>
                </div>
            </div>

            <div class="monitoring-stats grid grid-4" style="margin-top: var(--spacing-md);">
                <div class="mini-stat card">
                    <div class="mini-stat-icon" style="color: var(--accent-secondary);">
                        <i class="fas fa-stream"></i>
                    </div>
                    <div class="mini-stat-content">
                        <h4>1,247</h4>
                        <p>Transactions/sec</p>
                    </div>
                    <div class="pulse-indicator" style="background: var(--accent-success);"></div>
                </div>
                <div class="mini-stat card">
                    <div class="mini-stat-icon" style="color: var(--accent-danger);">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div class="mini-stat-content">
                        <h4>23</h4>
                        <p>Flagged (Last min)</p>
                    </div>
                </div>
                <div class="mini-stat card">
                    <div class="mini-stat-icon" style="color: var(--accent-success);">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <div class="mini-stat-content">
                        <h4>1,224</h4>
                        <p>Approved (Last min)</p>
                    </div>
                </div>
                <div class="mini-stat card">
                    <div class="mini-stat-icon" style="color: var(--accent-tertiary);">
                        <i class="fas fa-clock"></i>
                    </div>
                    <div class="mini-stat-content">
                        <h4>42ms</h4>
                        <p>Avg Latency</p>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Live Transaction Stream</h2>
                    <div class="stream-controls">
                        <input type="text" placeholder="Search Transaction ID..." class="search-input">
                        <select class="filter-select">
                            <option>All Transactions</option>
                            <option>High Risk Only</option>
                            <option>Flagged Only</option>
                            <option>Approved Only</option>
                        </select>
                    </div>
                </div>
                <div class="card-body">
                    <div class="transaction-table-wrapper">
                        <table class="transaction-table">
                            <thead>
                                <tr>
                                    <th>Transaction ID</th>
                                    <th>User ID</th>
                                    <th>Amount</th>
                                    <th>Location</th>
                                    <th>Device</th>
                                    <th>Time</th>
                                    <th>Risk Score</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="transactionTableBody">
                                <tr class="transaction-row">
                                    <td><code>TXN-847291</code></td>
                                    <td><code>USR-45821</code></td>
                                    <td class="amount">$15,420.00</td>
                                    <td><i class="fas fa-location-dot"></i> Lagos, Nigeria</td>
                                    <td><i class="fas fa-mobile"></i> iPhone 14</td>
                                    <td>2 min ago</td>
                                    <td><span class="risk-score high">94</span></td>
                                    <td><span class="badge-status badge-danger">Blocked</span></td>
                                    <td>
                                        <button class="btn-icon" title="View Details"><i class="fas fa-eye"></i></button>
                                    </td>
                                </tr>
                                <tr class="transaction-row">
                                    <td><code>TXN-847290</code></td>
                                    <td><code>USR-32109</code></td>
                                    <td class="amount">$245.50</td>
                                    <td><i class="fas fa-location-dot"></i> New York, USA</td>
                                    <td><i class="fas fa-laptop"></i> MacBook Pro</td>
                                    <td>2 min ago</td>
                                    <td><span class="risk-score medium">67</span></td>
                                    <td><span class="badge-status badge-warning">Review</span></td>
                                    <td>
                                        <button class="btn-icon" title="View Details"><i class="fas fa-eye"></i></button>
                                    </td>
                                </tr>
                                <tr class="transaction-row">
                                    <td><code>TXN-847289</code></td>
                                    <td><code>USR-78234</code></td>
                                    <td class="amount">$89.99</td>
                                    <td><i class="fas fa-location-dot"></i> London, UK</td>
                                    <td><i class="fas fa-mobile"></i> Samsung S23</td>
                                    <td>3 min ago</td>
                                    <td><span class="risk-score low">12</span></td>
                                    <td><span class="badge-status badge-success">Approved</span></td>
                                    <td>
                                        <button class="btn-icon" title="View Details"><i class="fas fa-eye"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `,

    'fraud-alerts': `
        <div class="fraud-alerts-page fade-in">
            <div class="page-header">
                <h2>Fraud Alerts & Case Management</h2>
                <div class="header-controls">
                    <button class="btn btn-secondary">
                        <i class="fas fa-download"></i> Export
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-plus"></i> Create Alert
                    </button>
                </div>
            </div>

            <div class="alert-tabs" style="margin-top: var(--spacing-md);">
                <button class="alert-tab active" data-tab="open">
                    <i class="fas fa-folder-open"></i> Open Alerts <span class="tab-count">247</span>
                </button>
                <button class="alert-tab" data-tab="review">
                    <i class="fas fa-search"></i> In Review <span class="tab-count">89</span>
                </button>
                <button class="alert-tab" data-tab="confirmed">
                    <i class="fas fa-check-circle"></i> Confirmed Fraud <span class="tab-count">156</span>
                </button>
                <button class="alert-tab" data-tab="false-positive">
                    <i class="fas fa-times-circle"></i> False Positives <span class="tab-count">34</span>
                </button>
            </div>

            <div class="alerts-grid grid grid-3" style="margin-top: var(--spacing-lg);">
                <div class="alert-card card">
                    <div class="alert-card-header">
                        <div class="alert-priority critical">
                            <i class="fas fa-exclamation-triangle"></i> Critical
                        </div>
                        <span class="alert-id">#ALT-8472</span>
                    </div>
                    <div class="alert-card-body">
                        <h3 class="alert-title">Large Transaction from High-Risk Country</h3>
                        <div class="alert-details">
                            <div class="detail-row">
                                <span class="detail-label">User:</span>
                                <span class="detail-value">USR-45821</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Amount:</span>
                                <span class="detail-value" style="color: var(--accent-danger);">$15,420.00</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Location:</span>
                                <span class="detail-value">Lagos, Nigeria</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Risk Score:</span>
                                <span class="risk-score high">94</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Detected:</span>
                                <span class="detail-value">2 minutes ago</span>
                            </div>
                        </div>
                        <div class="alert-reasons">
                            <span class="reason-tag"><i class="fas fa-location-dot"></i> Unusual Location</span>
                            <span class="reason-tag"><i class="fas fa-dollar-sign"></i> Large Amount</span>
                            <span class="reason-tag"><i class="fas fa-clock"></i> Unusual Time</span>
                        </div>
                    </div>
                    <div class="alert-card-footer">
                        <button class="btn btn-success btn-sm">
                            <i class="fas fa-check"></i> Approve
                        </button>
                        <button class="btn btn-danger btn-sm">
                            <i class="fas fa-ban"></i> Block
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-arrow-up"></i> Escalate
                        </button>
                    </div>
                </div>

                <div class="alert-card card">
                    <div class="alert-card-header">
                        <div class="alert-priority high">
                            <i class="fas fa-shield-alt"></i> High
                        </div>
                        <span class="alert-id">#ALT-8471</span>
                    </div>
                    <div class="alert-card-body">
                        <h3 class="alert-title">Velocity Anomaly Detected</h3>
                        <div class="alert-details">
                            <div class="detail-row">
                                <span class="detail-label">User:</span>
                                <span class="detail-value">USR-32109</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Transactions:</span>
                                <span class="detail-value" style="color: var(--accent-warning);">15 in 3 minutes</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Total Amount:</span>
                                <span class="detail-value">$3,682.50</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Risk Score:</span>
                                <span class="risk-score medium">78</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Detected:</span>
                                <span class="detail-value">8 minutes ago</span>
                            </div>
                        </div>
                        <div class="alert-reasons">
                            <span class="reason-tag"><i class="fas fa-gauge-high"></i> High Velocity</span>
                            <span class="reason-tag"><i class="fas fa-repeat"></i> Unusual Pattern</span>
                        </div>
                    </div>
                    <div class="alert-card-footer">
                        <button class="btn btn-success btn-sm">
                            <i class="fas fa-check"></i> Approve
                        </button>
                        <button class="btn btn-danger btn-sm">
                            <i class="fas fa-ban"></i> Block
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-arrow-up"></i> Escalate
                        </button>
                    </div>
                </div>

                <div class="alert-card card">
                    <div class="alert-card-header">
                        <div class="alert-priority high">
                            <i class="fas fa-location-crosshairs"></i> High
                        </div>
                        <span class="alert-id">#ALT-8470</span>
                    </div>
                    <div class="alert-card-body">
                        <h3 class="alert-title">Impossible Geo-Velocity</h3>
                        <div class="alert-details">
                            <div class="detail-row">
                                <span class="detail-label">User:</span>
                                <span class="detail-value">USR-78234</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Route:</span>
                                <span class="detail-value">NY → Tokyo (2 hrs)</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Amount:</span>
                                <span class="detail-value">$1,250.00</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Risk Score:</span>
                                <span class="risk-score high">89</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Detected:</span>
                                <span class="detail-value">15 minutes ago</span>
                            </div>
                        </div>
                        <div class="alert-reasons">
                            <span class="reason-tag"><i class="fas fa-plane"></i> Geo-Velocity</span>
                            <span class="reason-tag"><i class="fas fa-mobile"></i> New Device</span>
                        </div>
                    </div>
                    <div class="alert-card-footer">
                        <button class="btn btn-success btn-sm">
                            <i class="fas fa-check"></i> Approve
                        </button>
                        <button class="btn btn-danger btn-sm">
                            <i class="fas fa-ban"></i> Block
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-arrow-up"></i> Escalate
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `,

    'transaction-details': `
        <div class="transaction-details-page fade-in">
            <div class="page-header">
                <h2>Transaction Details</h2>
                <div class="header-controls">
                    <button class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> Back
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-download"></i> Export Report
                    </button>
                </div>
            </div>

            <div class="transaction-overview card" style="margin-top: var(--spacing-md);">
                <div class="transaction-header">
                    <div class="transaction-id-section">
                        <h3>Transaction <code>TXN-847291</code></h3>
                        <span class="badge-status badge-danger">Blocked - High Risk</span>
                    </div>
                    <div class="transaction-risk-gauge">
                        <div class="risk-gauge-circle">
                            <svg width="120" height="120">
                                <circle cx="60" cy="60" r="50" fill="none" stroke="var(--bg-tertiary)" stroke-width="10"/>
                                <circle cx="60" cy="60" r="50" fill="none" stroke="var(--accent-danger)" stroke-width="10" 
                                        stroke-dasharray="314" stroke-dashoffset="31.4" transform="rotate(-90 60 60)"/>
                            </svg>
                            <div class="risk-gauge-value">94</div>
                        </div>
                        <p>Risk Score</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Transaction Summary</h2>
                    </div>
                    <div class="card-body">
                        <div class="detail-list">
                            <div class="detail-item">
                                <span class="detail-label"><i class="fas fa-user"></i> User ID</span>
                                <span class="detail-value"><code>USR-45821</code></span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label"><i class="fas fa-dollar-sign"></i> Amount</span>
                                <span class="detail-value" style="color: var(--accent-danger); font-weight: 700; font-size: 1.2rem;">$15,420.00</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label"><i class="fas fa-location-dot"></i> Location</span>
                                <span class="detail-value">Lagos, Nigeria</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label"><i class="fas fa-mobile"></i> Device</span>
                                <span class="detail-value">iPhone 14 Pro (iOS 17.2)</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label"><i class="fas fa-clock"></i> Timestamp</span>
                                <span class="detail-value">2026-01-08 22:45:12 IST</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label"><i class="fas fa-network-wired"></i> IP Address</span>
                                <span class="detail-value"><code>197.210.85.142</code></span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label"><i class="fas fa-building"></i> Merchant</span>
                                <span class="detail-value">International Wire Transfer</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label"><i class="fas fa-credit-card"></i> Payment Method</span>
                                <span class="detail-value">Visa **** 4521</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Fraud Indicators</h2>
                    </div>
                    <div class="card-body">
                        <div class="fraud-indicators">
                            <div class="indicator-item high">
                                <div class="indicator-icon">
                                    <i class="fas fa-location-dot"></i>
                                </div>
                                <div class="indicator-content">
                                    <h4>Unusual Location</h4>
                                    <p>First transaction from Nigeria</p>
                                    <div class="indicator-score">Impact: <strong>+35</strong></div>
                                </div>
                            </div>
                            <div class="indicator-item high">
                                <div class="indicator-icon">
                                    <i class="fas fa-dollar-sign"></i>
                                </div>
                                <div class="indicator-content">
                                    <h4>Large Amount</h4>
                                    <p>450% above user average ($3,200)</p>
                                    <div class="indicator-score">Impact: <strong>+28</strong></div>
                                </div>
                            </div>
                            <div class="indicator-item medium">
                                <div class="indicator-icon">
                                    <i class="fas fa-clock"></i>
                                </div>
                                <div class="indicator-content">
                                    <h4>Unusual Time</h4>
                                    <p>Transaction at 2:45 AM (user typically transacts 9 AM - 6 PM)</p>
                                    <div class="indicator-score">Impact: <strong>+18</strong></div>
                                </div>
                            </div>
                            <div class="indicator-item medium">
                                <div class="indicator-icon">
                                    <i class="fas fa-mobile"></i>
                                </div>
                                <div class="indicator-content">
                                    <h4>New Device</h4>
                                    <p>Device fingerprint not recognized</p>
                                    <div class="indicator-score">Impact: <strong>+13</strong></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Historical Transaction Pattern</h2>
                </div>
                <div class="card-body">
                    <canvas id="transactionHistoryChart" style="max-height: 250px;"></canvas>
                </div>
            </div>

            <div class="grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Model Explainability</h2>
                    </div>
                    <div class="card-body">
                        <div class="explainability-chart">
                            <div class="explain-item">
                                <span class="explain-label">Location Anomaly</span>
                                <div class="explain-bar">
                                    <div class="explain-fill" style="width: 85%; background: var(--accent-danger);"></div>
                                </div>
                                <span class="explain-value">85%</span>
                            </div>
                            <div class="explain-item">
                                <span class="explain-label">Amount Deviation</span>
                                <div class="explain-bar">
                                    <div class="explain-fill" style="width: 72%; background: var(--accent-warning);"></div>
                                </div>
                                <span class="explain-value">72%</span>
                            </div>
                            <div class="explain-item">
                                <span class="explain-label">Time Pattern</span>
                                <div class="explain-bar">
                                    <div class="explain-fill" style="width: 58%; background: var(--accent-warning);"></div>
                                </div>
                                <span class="explain-value">58%</span>
                            </div>
                            <div class="explain-item">
                                <span class="explain-label">Device Trust</span>
                                <div class="explain-bar">
                                    <div class="explain-fill" style="width: 45%; background: var(--accent-tertiary);"></div>
                                </div>
                                <span class="explain-value">45%</span>
                            </div>
                            <div class="explain-item">
                                <span class="explain-label">Velocity Check</span>
                                <div class="explain-bar">
                                    <div class="explain-fill" style="width: 32%; background: var(--accent-secondary);"></div>
                                </div>
                                <span class="explain-value">32%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Actions & Timeline</h2>
                    </div>
                    <div class="card-body">
                        <div class="timeline">
                            <div class="timeline-item">
                                <div class="timeline-dot" style="background: var(--accent-danger);"></div>
                                <div class="timeline-content">
                                    <h4>Transaction Blocked</h4>
                                    <p>Automatically blocked due to high risk score</p>
                                    <span class="timeline-time">2 minutes ago</span>
                                </div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-dot" style="background: var(--accent-warning);"></div>
                                <div class="timeline-content">
                                    <h4>Alert Generated</h4>
                                    <p>Critical alert sent to fraud team</p>
                                    <span class="timeline-time">2 minutes ago</span>
                                </div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-dot" style="background: var(--accent-secondary);"></div>
                                <div class="timeline-content">
                                    <h4>ML Analysis Complete</h4>
                                    <p>Risk score calculated: 94/100</p>
                                    <span class="timeline-time">2 minutes ago</span>
                                </div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-dot" style="background: var(--accent-success);"></div>
                                <div class="timeline-content">
                                    <h4>Transaction Initiated</h4>
                                    <p>User initiated wire transfer</p>
                                    <span class="timeline-time">2 minutes ago</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
};

// Navigation handling
document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    const contentContainer = document.getElementById('contentContainer');
    const pageTitle = document.getElementById('pageTitle');
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');

    // Load dashboard by default
    loadPage('dashboard');

    // Navigation click handlers
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.dataset.page;
            
            // Update active state
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
            
            // Load page
            loadPage(page);
        });
    });

    // Menu toggle for mobile
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });

    // Load page function
    function loadPage(pageName) {
        const pageContent = pages[pageName];
        if (pageContent) {
            contentContainer.innerHTML = pageContent;
            updatePageTitle(pageName);
            initializePageScripts(pageName);
        }
    }

    // Update page title
    function updatePageTitle(pageName) {
        const titles = {
            'dashboard': 'Dashboard',
            'live-monitoring': 'Live Transaction Monitoring',
            'fraud-alerts': 'Fraud Alerts & Case Management',
            'transaction-details': 'Transaction Details',
            'customer-profile': 'Customer Behavioral Profiles',
            'risk-scoring': 'Risk Scoring & Anomaly Insights',
            'analytics': 'Analytics & Reports',
            'model-management': 'Model & Detection Rules',
            'integrations': 'System Integrations',
            'feedback': 'Feedback & Adaptive Learning',
            'user-management': 'User & Role Management',
            'audit-logs': 'Audit Logs & Compliance',
            'settings': 'Settings & Configuration'
        };
        pageTitle.textContent = titles[pageName] || 'Dashboard';
    }

    // Initialize page-specific scripts
    function initializePageScripts(pageName) {
        if (pageName === 'dashboard') {
            initializeDashboardCharts();
        } else if (pageName === 'transaction-details') {
            initializeTransactionCharts();
        }
    }

    // Dashboard charts initialization
    function initializeDashboardCharts() {
        // This would integrate with Chart.js or similar library
        console.log('Dashboard charts initialized');
    }

    // Transaction detail charts
    function initializeTransactionCharts() {
        console.log('Transaction charts initialized');
    }
});
