// Final Page Templates (Model Management, Integrations, Feedback, User Management, Audit Logs, Settings)

const finalPages = {
    'model-management': `
        <div class="model-management-page fade-in">
            <div class="page-header">
                <h2>Model & Detection Rules</h2>
                <div class="header-controls">
                    <button class="btn btn-secondary">
                        <i class="fas fa-upload"></i> Upload Model
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-plus"></i> Create Rule
                    </button>
                </div>
            </div>

            <div class="model-tabs" style="margin-top: var(--spacing-md);">
                <button class="model-tab active" data-tab="active-models">
                    <i class="fas fa-brain"></i> Active Models
                </button>
                <button class="model-tab" data-tab="rules">
                    <i class="fas fa-list-check"></i> Detection Rules
                </button>
                <button class="model-tab" data-tab="thresholds">
                    <i class="fas fa-sliders"></i> Thresholds
                </button>
                <button class="model-tab" data-tab="versions">
                    <i class="fas fa-code-branch"></i> Version History
                </button>
            </div>

            <div class="models-grid grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="model-card card">
                    <div class="model-card-header">
                        <div class="model-status active">
                            <i class="fas fa-circle pulse"></i> Active
                        </div>
                        <span class="model-version">v2.4.1</span>
                    </div>
                    <div class="model-card-body">
                        <h3>Behavioral Analytics Model</h3>
                        <p class="model-description">Deep learning model trained on user behavior patterns</p>
                        <div class="model-metrics grid grid-2">
                            <div class="model-metric">
                                <span class="metric-label">Accuracy</span>
                                <span class="metric-value" style="color: var(--accent-success);">98.7%</span>
                            </div>
                            <div class="model-metric">
                                <span class="metric-label">Latency</span>
                                <span class="metric-value" style="color: var(--accent-secondary);">32ms</span>
                            </div>
                            <div class="model-metric">
                                <span class="metric-label">Deployed</span>
                                <span class="metric-value">15 days ago</span>
                            </div>
                            <div class="model-metric">
                                <span class="metric-label">Predictions</span>
                                <span class="metric-value">2.4M</span>
                            </div>
                        </div>
                        <div class="model-features">
                            <h4>Key Features</h4>
                            <div class="feature-tags">
                                <span class="feature-tag">Transaction Amount</span>
                                <span class="feature-tag">Time Patterns</span>
                                <span class="feature-tag">Location History</span>
                                <span class="feature-tag">Device Fingerprint</span>
                            </div>
                        </div>
                    </div>
                    <div class="model-card-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-chart-line"></i> View Performance
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-cog"></i> Configure
                        </button>
                        <button class="btn btn-danger btn-sm">
                            <i class="fas fa-power-off"></i> Deactivate
                        </button>
                    </div>
                </div>

                <div class="model-card card">
                    <div class="model-card-header">
                        <div class="model-status active">
                            <i class="fas fa-circle pulse"></i> Active
                        </div>
                        <span class="model-version">v1.8.3</span>
                    </div>
                    <div class="model-card-body">
                        <h3>Anomaly Detection Model</h3>
                        <p class="model-description">Isolation Forest algorithm for detecting statistical anomalies</p>
                        <div class="model-metrics grid grid-2">
                            <div class="model-metric">
                                <span class="metric-label">Accuracy</span>
                                <span class="metric-value" style="color: var(--accent-success);">96.2%</span>
                            </div>
                            <div class="model-metric">
                                <span class="metric-label">Latency</span>
                                <span class="metric-value" style="color: var(--accent-success);">18ms</span>
                            </div>
                            <div class="model-metric">
                                <span class="metric-label">Deployed</span>
                                <span class="metric-value">42 days ago</span>
                            </div>
                            <div class="model-metric">
                                <span class="metric-label">Predictions</span>
                                <span class="metric-value">5.1M</span>
                            </div>
                        </div>
                        <div class="model-features">
                            <h4>Key Features</h4>
                            <div class="feature-tags">
                                <span class="feature-tag">Velocity Patterns</span>
                                <span class="feature-tag">Amount Deviation</span>
                                <span class="feature-tag">Geo-Velocity</span>
                                <span class="feature-tag">Frequency Analysis</span>
                            </div>
                        </div>
                    </div>
                    <div class="model-card-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-chart-line"></i> View Performance
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-cog"></i> Configure
                        </button>
                        <button class="btn btn-danger btn-sm">
                            <i class="fas fa-power-off"></i> Deactivate
                        </button>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Detection Rules Configuration</h2>
                    <button class="btn btn-primary btn-sm">
                        <i class="fas fa-plus"></i> Add Rule
                    </button>
                </div>
                <div class="card-body">
                    <div class="rules-table-wrapper">
                        <table class="rules-table">
                            <thead>
                                <tr>
                                    <th>Rule Name</th>
                                    <th>Condition</th>
                                    <th>Risk Score Impact</th>
                                    <th>Priority</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Large Transaction</strong></td>
                                    <td><code>amount > $10,000</code></td>
                                    <td><span class="impact-badge high">+35</span></td>
                                    <td><span class="badge-status badge-danger">Critical</span></td>
                                    <td><span class="status-toggle active"><i class="fas fa-toggle-on"></i> Active</span></td>
                                    <td>
                                        <button class="btn-icon"><i class="fas fa-edit"></i></button>
                                        <button class="btn-icon"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>High-Risk Country</strong></td>
                                    <td><code>location in risk_countries</code></td>
                                    <td><span class="impact-badge high">+28</span></td>
                                    <td><span class="badge-status badge-danger">Critical</span></td>
                                    <td><span class="status-toggle active"><i class="fas fa-toggle-on"></i> Active</span></td>
                                    <td>
                                        <button class="btn-icon"><i class="fas fa-edit"></i></button>
                                        <button class="btn-icon"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Unusual Time</strong></td>
                                    <td><code>hour < 6 OR hour > 23</code></td>
                                    <td><span class="impact-badge medium">+18</span></td>
                                    <td><span class="badge-status badge-warning">High</span></td>
                                    <td><span class="status-toggle active"><i class="fas fa-toggle-on"></i> Active</span></td>
                                    <td>
                                        <button class="btn-icon"><i class="fas fa-edit"></i></button>
                                        <button class="btn-icon"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>New Device</strong></td>
                                    <td><code>device_fingerprint not in history</code></td>
                                    <td><span class="impact-badge medium">+15</span></td>
                                    <td><span class="badge-status badge-warning">High</span></td>
                                    <td><span class="status-toggle active"><i class="fas fa-toggle-on"></i> Active</span></td>
                                    <td>
                                        <button class="btn-icon"><i class="fas fa-edit"></i></button>
                                        <button class="btn-icon"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `,

    'integrations': `
        <div class="integrations-page fade-in">
            <div class="page-header">
                <h2>System Integrations</h2>
                <div class="header-controls">
                    <button class="btn btn-primary">
                        <i class="fas fa-plus"></i> Add Integration
                    </button>
                </div>
            </div>

            <div class="integrations-grid grid grid-3" style="margin-top: var(--spacing-md);">
                <div class="integration-card card">
                    <div class="integration-header">
                        <div class="integration-icon" style="background: linear-gradient(135deg, #FF6B6B, #FF8E53);">
                            <i class="fas fa-building-columns"></i>
                        </div>
                        <div class="integration-status connected">
                            <i class="fas fa-circle pulse"></i> Connected
                        </div>
                    </div>
                    <div class="integration-body">
                        <h3>Core Banking System</h3>
                        <p class="integration-description">Primary banking infrastructure integration</p>
                        <div class="integration-details">
                            <div class="detail-row">
                                <span class="detail-label">Endpoint</span>
                                <span class="detail-value"><code>api.bank.internal</code></span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Last Sync</span>
                                <span class="detail-value">2 minutes ago</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Uptime</span>
                                <span class="detail-value" style="color: var(--accent-success);">99.98%</span>
                            </div>
                        </div>
                    </div>
                    <div class="integration-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-vial"></i> Test Connection
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-cog"></i> Configure
                        </button>
                    </div>
                </div>

                <div class="integration-card card">
                    <div class="integration-header">
                        <div class="integration-icon" style="background: linear-gradient(135deg, #4ECDC4, #44A08D);">
                            <i class="fas fa-credit-card"></i>
                        </div>
                        <div class="integration-status connected">
                            <i class="fas fa-circle pulse"></i> Connected
                        </div>
                    </div>
                    <div class="integration-body">
                        <h3>Payment Gateway</h3>
                        <p class="integration-description">Real-time payment processing integration</p>
                        <div class="integration-details">
                            <div class="detail-row">
                                <span class="detail-label">Endpoint</span>
                                <span class="detail-value"><code>gateway.payments.com</code></span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Last Sync</span>
                                <span class="detail-value">5 seconds ago</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Uptime</span>
                                <span class="detail-value" style="color: var(--accent-success);">99.95%</span>
                            </div>
                        </div>
                    </div>
                    <div class="integration-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-vial"></i> Test Connection
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-cog"></i> Configure
                        </button>
                    </div>
                </div>

                <div class="integration-card card">
                    <div class="integration-header">
                        <div class="integration-icon" style="background: linear-gradient(135deg, #FFE66D, #FFA94D);">
                            <i class="fas fa-user-check"></i>
                        </div>
                        <div class="integration-status connected">
                            <i class="fas fa-circle pulse"></i> Connected
                        </div>
                    </div>
                    <div class="integration-body">
                        <h3>KYC System</h3>
                        <p class="integration-description">Know Your Customer verification service</p>
                        <div class="integration-details">
                            <div class="detail-row">
                                <span class="detail-label">Endpoint</span>
                                <span class="detail-value"><code>kyc.verify.com</code></span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Last Sync</span>
                                <span class="detail-value">1 minute ago</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Uptime</span>
                                <span class="detail-value" style="color: var(--accent-success);">99.92%</span>
                            </div>
                        </div>
                    </div>
                    <div class="integration-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-vial"></i> Test Connection
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-cog"></i> Configure
                        </button>
                    </div>
                </div>

                <div class="integration-card card">
                    <div class="integration-header">
                        <div class="integration-icon" style="background: linear-gradient(135deg, #A8E6CF, #51CF66);">
                            <i class="fas fa-users"></i>
                        </div>
                        <div class="integration-status connected">
                            <i class="fas fa-circle pulse"></i> Connected
                        </div>
                    </div>
                    <div class="integration-body">
                        <h3>CRM System</h3>
                        <p class="integration-description">Customer relationship management platform</p>
                        <div class="integration-details">
                            <div class="detail-row">
                                <span class="detail-label">Endpoint</span>
                                <span class="detail-value"><code>crm.internal.com</code></span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Last Sync</span>
                                <span class="detail-value">8 minutes ago</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Uptime</span>
                                <span class="detail-value" style="color: var(--accent-success);">99.87%</span>
                            </div>
                        </div>
                    </div>
                    <div class="integration-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-vial"></i> Test Connection
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-cog"></i> Configure
                        </button>
                    </div>
                </div>

                <div class="integration-card card">
                    <div class="integration-header">
                        <div class="integration-icon" style="background: linear-gradient(135deg, #FF6B9D, #C06C84);">
                            <i class="fas fa-bell"></i>
                        </div>
                        <div class="integration-status connected">
                            <i class="fas fa-circle pulse"></i> Connected
                        </div>
                    </div>
                    <div class="integration-body">
                        <h3>Notification Service</h3>
                        <p class="integration-description">SMS, Email, and Push notification delivery</p>
                        <div class="integration-details">
                            <div class="detail-row">
                                <span class="detail-label">Endpoint</span>
                                <span class="detail-value"><code>notify.service.com</code></span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Last Sync</span>
                                <span class="detail-value">30 seconds ago</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Uptime</span>
                                <span class="detail-value" style="color: var(--accent-success);">99.99%</span>
                            </div>
                        </div>
                    </div>
                    <div class="integration-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-vial"></i> Test Connection
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-cog"></i> Configure
                        </button>
                    </div>
                </div>

                <div class="integration-card card disabled">
                    <div class="integration-header">
                        <div class="integration-icon" style="background: var(--bg-tertiary); color: var(--text-muted);">
                            <i class="fas fa-database"></i>
                        </div>
                        <div class="integration-status disconnected">
                            <i class="fas fa-circle"></i> Not Connected
                        </div>
                    </div>
                    <div class="integration-body">
                        <h3>Data Warehouse</h3>
                        <p class="integration-description">Historical data analytics platform</p>
                        <div class="integration-details">
                            <div class="detail-row">
                                <span class="detail-label">Status</span>
                                <span class="detail-value" style="color: var(--text-muted);">Not configured</span>
                            </div>
                        </div>
                    </div>
                    <div class="integration-footer">
                        <button class="btn btn-primary btn-sm">
                            <i class="fas fa-plug"></i> Connect
                        </button>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Integration Logs</h2>
                    <button class="btn btn-secondary btn-sm">
                        <i class="fas fa-sync"></i> Refresh
                    </button>
                </div>
                <div class="card-body">
                    <div class="logs-list">
                        <div class="log-item success">
                            <div class="log-icon"><i class="fas fa-check-circle"></i></div>
                            <div class="log-content">
                                <h4>Payment Gateway - Connection Successful</h4>
                                <p>Successfully synced 1,247 transactions</p>
                                <span class="log-time">2 minutes ago</span>
                            </div>
                        </div>
                        <div class="log-item success">
                            <div class="log-icon"><i class="fas fa-check-circle"></i></div>
                            <div class="log-content">
                                <h4>Core Banking System - Health Check Passed</h4>
                                <p>All systems operational</p>
                                <span class="log-time">5 minutes ago</span>
                            </div>
                        </div>
                        <div class="log-item warning">
                            <div class="log-icon"><i class="fas fa-exclamation-triangle"></i></div>
                            <div class="log-content">
                                <h4>CRM System - Slow Response</h4>
                                <p>Response time: 2.3s (threshold: 1s)</p>
                                <span class="log-time">8 minutes ago</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,

    'feedback': `
        <div class="feedback-page fade-in">
            <div class="page-header">
                <h2>Feedback & Adaptive Learning</h2>
                <div class="header-controls">
                    <button class="btn btn-secondary">
                        <i class="fas fa-chart-line"></i> View Impact
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-sync"></i> Retrain Models
                    </button>
                </div>
            </div>

            <div class="feedback-stats grid grid-4" style="margin-top: var(--spacing-md);">
                <div class="feedback-stat card">
                    <div class="stat-icon" style="color: var(--accent-success);">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <h3>Confirmed Fraud</h3>
                    <div class="stat-value">1,247</div>
                    <p class="stat-label">Analyst confirmations this month</p>
                </div>
                <div class="feedback-stat card">
                    <div class="stat-icon" style="color: var(--accent-warning);">
                        <i class="fas fa-times-circle"></i>
                    </div>
                    <h3>False Positives</h3>
                    <div class="stat-value">89</div>
                    <p class="stat-label">Incorrectly flagged transactions</p>
                </div>
                <div class="feedback-stat card">
                    <div class="stat-icon" style="color: var(--accent-secondary);">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3>Model Updates</h3>
                    <div class="stat-value">12</div>
                    <p class="stat-label">Adaptive learning cycles completed</p>
                </div>
                <div class="feedback-stat card">
                    <div class="stat-icon" style="color: var(--accent-tertiary);">
                        <i class="fas fa-arrow-trend-up"></i>
                    </div>
                    <h3>Accuracy Improvement</h3>
                    <div class="stat-value">+2.3%</div>
                    <p class="stat-label">Since last training cycle</p>
                </div>
            </div>

            <div class="grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Pending Feedback</h2>
                    </div>
                    <div class="card-body">
                        <div class="feedback-queue">
                            <div class="feedback-item">
                                <div class="feedback-header">
                                    <span class="feedback-id"><code>TXN-847291</code></span>
                                    <span class="badge-status badge-warning">Needs Review</span>
                                </div>
                                <p class="feedback-description">High-risk transaction flagged - awaiting analyst confirmation</p>
                                <div class="feedback-actions">
                                    <button class="btn btn-success btn-sm">
                                        <i class="fas fa-check"></i> Confirm Fraud
                                    </button>
                                    <button class="btn btn-danger btn-sm">
                                        <i class="fas fa-times"></i> Mark False Positive
                                    </button>
                                </div>
                            </div>
                            <div class="feedback-item">
                                <div class="feedback-header">
                                    <span class="feedback-id"><code>TXN-847245</code></span>
                                    <span class="badge-status badge-warning">Needs Review</span>
                                </div>
                                <p class="feedback-description">Velocity anomaly detected - customer dispute filed</p>
                                <div class="feedback-actions">
                                    <button class="btn btn-success btn-sm">
                                        <i class="fas fa-check"></i> Confirm Fraud
                                    </button>
                                    <button class="btn btn-danger btn-sm">
                                        <i class="fas fa-times"></i> Mark False Positive
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Learning Impact</h2>
                    </div>
                    <div class="card-body">
                        <canvas id="learningImpactChart" style="max-height: 300px;"></canvas>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Recent Feedback Activity</h2>
                </div>
                <div class="card-body">
                    <div class="activity-timeline">
                        <div class="activity-item">
                            <div class="activity-dot success"></div>
                            <div class="activity-content">
                                <h4>Fraud Confirmed - TXN-847289</h4>
                                <p>Analyst marked transaction as confirmed fraud. Model updated with new pattern.</p>
                                <span class="activity-time">15 minutes ago</span>
                            </div>
                        </div>
                        <div class="activity-item">
                            <div class="activity-dot warning"></div>
                            <div class="activity-content">
                                <h4>False Positive - TXN-847234</h4>
                                <p>Legitimate transaction incorrectly flagged. Behavioral baseline adjusted.</p>
                                <span class="activity-time">1 hour ago</span>
                            </div>
                        </div>
                        <div class="activity-item">
                            <div class="activity-dot info"></div>
                            <div class="activity-content">
                                <h4>Model Retrained</h4>
                                <p>Adaptive learning cycle completed with 247 new feedback samples.</p>
                                <span class="activity-time">3 hours ago</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,

    'user-management': `
        <div class="user-management-page fade-in">
            <div class="page-header">
                <h2>User & Role Management</h2>
                <div class="header-controls">
                    <button class="btn btn-secondary">
                        <i class="fas fa-user-shield"></i> Manage Roles
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-user-plus"></i> Add User
                    </button>
                </div>
            </div>

            <div class="users-grid grid grid-3" style="margin-top: var(--spacing-md);">
                <div class="user-card card">
                    <div class="user-card-header">
                        <img src="https://ui-avatars.com/api/?name=Sarah+Johnson&background=FF6B6B&color=fff" alt="User" class="user-avatar">
                        <span class="user-status online"><i class="fas fa-circle"></i></span>
                    </div>
                    <div class="user-card-body">
                        <h3>Sarah Johnson</h3>
                        <p class="user-email">sarah.johnson@swiftai.com</p>
                        <span class="user-role admin">
                            <i class="fas fa-crown"></i> Administrator
                        </span>
                        <div class="user-stats">
                            <div class="user-stat">
                                <span class="stat-label">Cases Reviewed</span>
                                <span class="stat-value">1,247</span>
                            </div>
                            <div class="user-stat">
                                <span class="stat-label">Last Active</span>
                                <span class="stat-value">5 min ago</span>
                            </div>
                        </div>
                    </div>
                    <div class="user-card-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-key"></i> Reset Password
                        </button>
                    </div>
                </div>

                <div class="user-card card">
                    <div class="user-card-header">
                        <img src="https://ui-avatars.com/api/?name=Michael+Chen&background=4ECDC4&color=fff" alt="User" class="user-avatar">
                        <span class="user-status online"><i class="fas fa-circle"></i></span>
                    </div>
                    <div class="user-card-body">
                        <h3>Michael Chen</h3>
                        <p class="user-email">michael.chen@swiftai.com</p>
                        <span class="user-role analyst">
                            <i class="fas fa-user-tie"></i> Fraud Analyst
                        </span>
                        <div class="user-stats">
                            <div class="user-stat">
                                <span class="stat-label">Cases Reviewed</span>
                                <span class="stat-value">892</span>
                            </div>
                            <div class="user-stat">
                                <span class="stat-label">Last Active</span>
                                <span class="stat-value">2 min ago</span>
                            </div>
                        </div>
                    </div>
                    <div class="user-card-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-key"></i> Reset Password
                        </button>
                    </div>
                </div>

                <div class="user-card card">
                    <div class="user-card-header">
                        <img src="https://ui-avatars.com/api/?name=Emily+Rodriguez&background=FFE66D&color=333" alt="User" class="user-avatar">
                        <span class="user-status away"><i class="fas fa-circle"></i></span>
                    </div>
                    <div class="user-card-body">
                        <h3>Emily Rodriguez</h3>
                        <p class="user-email">emily.rodriguez@swiftai.com</p>
                        <span class="user-role manager">
                            <i class="fas fa-user-shield"></i> Risk Manager
                        </span>
                        <div class="user-stats">
                            <div class="user-stat">
                                <span class="stat-label">Cases Reviewed</span>
                                <span class="stat-value">654</span>
                            </div>
                            <div class="user-stat">
                                <span class="stat-label">Last Active</span>
                                <span class="stat-value">1 hour ago</span>
                            </div>
                        </div>
                    </div>
                    <div class="user-card-footer">
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-secondary btn-sm">
                            <i class="fas fa-key"></i> Reset Password
                        </button>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Role Permissions</h2>
                </div>
                <div class="card-body">
                    <div class="permissions-table-wrapper">
                        <table class="permissions-table">
                            <thead>
                                <tr>
                                    <th>Permission</th>
                                    <th>Administrator</th>
                                    <th>Risk Manager</th>
                                    <th>Fraud Analyst</th>
                                    <th>Compliance Officer</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>View Dashboard</strong></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                </tr>
                                <tr>
                                    <td><strong>Review Alerts</strong></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                </tr>
                                <tr>
                                    <td><strong>Block Transactions</strong></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                </tr>
                                <tr>
                                    <td><strong>Manage Models</strong></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                </tr>
                                <tr>
                                    <td><strong>User Management</strong></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                </tr>
                                <tr>
                                    <td><strong>System Configuration</strong></td>
                                    <td><i class="fas fa-check-circle" style="color: var(--accent-success);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                    <td><i class="fas fa-times-circle" style="color: var(--text-muted);"></i></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `,

    'audit-logs': `
        <div class="audit-logs-page fade-in">
            <div class="page-header">
                <h2>Audit Logs & Compliance</h2>
                <div class="header-controls">
                    <input type="text" placeholder="Search logs..." class="search-input">
                    <select class="filter-select">
                        <option>All Actions</option>
                        <option>User Actions</option>
                        <option>Model Decisions</option>
                        <option>Configuration Changes</option>
                    </select>
                    <button class="btn btn-primary">
                        <i class="fas fa-download"></i> Export Logs
                    </button>
                </div>
            </div>

            <div class="logs-table-wrapper card" style="margin-top: var(--spacing-md);">
                <table class="audit-table">
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>User</th>
                            <th>Action</th>
                            <th>Resource</th>
                            <th>Details</th>
                            <th>IP Address</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>2026-01-08 22:45:12</td>
                            <td>
                                <div class="user-info">
                                    <img src="https://ui-avatars.com/api/?name=Sarah+Johnson&background=FF6B6B&color=fff&size=32" alt="User">
                                    <span>Sarah Johnson</span>
                                </div>
                            </td>
                            <td><span class="action-badge critical">Block Transaction</span></td>
                            <td><code>TXN-847291</code></td>
                            <td>Blocked high-risk transaction from Nigeria</td>
                            <td><code>192.168.1.100</code></td>
                            <td><span class="badge-status badge-success">Success</span></td>
                        </tr>
                        <tr>
                            <td>2026-01-08 22:42:35</td>
                            <td>
                                <div class="user-info">
                                    <img src="https://ui-avatars.com/api/?name=Michael+Chen&background=4ECDC4&color=fff&size=32" alt="User">
                                    <span>Michael Chen</span>
                                </div>
                            </td>
                            <td><span class="action-badge normal">Review Alert</span></td>
                            <td><code>ALT-8472</code></td>
                            <td>Reviewed and approved alert</td>
                            <td><code>192.168.1.105</code></td>
                            <td><span class="badge-status badge-success">Success</span></td>
                        </tr>
                        <tr>
                            <td>2026-01-08 22:38:21</td>
                            <td>
                                <div class="user-info">
                                    <img src="https://ui-avatars.com/api/?name=System&background=888&color=fff&size=32" alt="System">
                                    <span>System</span>
                                </div>
                            </td>
                            <td><span class="action-badge info">Model Decision</span></td>
                            <td><code>TXN-847290</code></td>
                            <td>Anomaly detection model flagged transaction (score: 94)</td>
                            <td><code>-</code></td>
                            <td><span class="badge-status badge-success">Success</span></td>
                        </tr>
                        <tr>
                            <td>2026-01-08 22:30:15</td>
                            <td>
                                <div class="user-info">
                                    <img src="https://ui-avatars.com/api/?name=Sarah+Johnson&background=FF6B6B&color=fff&size=32" alt="User">
                                    <span>Sarah Johnson</span>
                                </div>
                            </td>
                            <td><span class="action-badge warning">Config Change</span></td>
                            <td><code>Detection Rules</code></td>
                            <td>Updated "Large Transaction" threshold to $10,000</td>
                            <td><code>192.168.1.100</code></td>
                            <td><span class="badge-status badge-success">Success</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `,

    'settings': `
        <div class="settings-page fade-in">
            <div class="page-header">
                <h2>Settings & Configuration</h2>
                <div class="header-controls">
                    <button class="btn btn-primary">
                        <i class="fas fa-save"></i> Save Changes
                    </button>
                </div>
            </div>

            <div class="settings-tabs" style="margin-top: var(--spacing-md);">
                <button class="settings-tab active" data-tab="general">
                    <i class="fas fa-cog"></i> General
                </button>
                <button class="settings-tab" data-tab="alerts">
                    <i class="fas fa-bell"></i> Alerts
                </button>
                <button class="settings-tab" data-tab="notifications">
                    <i class="fas fa-envelope"></i> Notifications
                </button>
                <button class="settings-tab" data-tab="security">
                    <i class="fas fa-shield"></i> Security
                </button>
            </div>

            <div class="settings-content grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Alert Thresholds</h2>
                    </div>
                    <div class="card-body">
                        <div class="settings-group">
                            <label class="setting-label">
                                <span>Critical Risk Threshold</span>
                                <input type="number" class="setting-input" value="80" min="0" max="100">
                            </label>
                            <p class="setting-description">Transactions with risk score above this value will be automatically blocked</p>
                        </div>
                        <div class="settings-group">
                            <label class="setting-label">
                                <span>High Risk Threshold</span>
                                <input type="number" class="setting-input" value="60" min="0" max="100">
                            </label>
                            <p class="setting-description">Transactions will be flagged for manual review</p>
                        </div>
                        <div class="settings-group">
                            <label class="setting-label">
                                <span>Medium Risk Threshold</span>
                                <input type="number" class="setting-input" value="40" min="0" max="100">
                            </label>
                            <p class="setting-description">Transactions will be monitored but not blocked</p>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">SLA Configuration</h2>
                    </div>
                    <div class="card-body">
                        <div class="settings-group">
                            <label class="setting-label">
                                <span>Critical Alert Response Time</span>
                                <input type="number" class="setting-input" value="15" min="1">
                                <span class="input-suffix">minutes</span>
                            </label>
                            <p class="setting-description">Maximum time to respond to critical alerts</p>
                        </div>
                        <div class="settings-group">
                            <label class="setting-label">
                                <span>High Alert Response Time</span>
                                <input type="number" class="setting-input" value="60" min="1">
                                <span class="input-suffix">minutes</span>
                            </label>
                            <p class="setting-description">Maximum time to respond to high-priority alerts</p>
                        </div>
                        <div class="settings-group">
                            <label class="setting-label">
                                <span>Detection Latency Target</span>
                                <input type="number" class="setting-input" value="50" min="1">
                                <span class="input-suffix">ms</span>
                            </label>
                            <p class="setting-description">Target maximum time for fraud detection</p>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Notification Preferences</h2>
                    </div>
                    <div class="card-body">
                        <div class="settings-group">
                            <label class="setting-toggle">
                                <input type="checkbox" checked>
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">Email Notifications</span>
                            </label>
                            <p class="setting-description">Receive email alerts for critical events</p>
                        </div>
                        <div class="settings-group">
                            <label class="setting-toggle">
                                <input type="checkbox" checked>
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">SMS Notifications</span>
                            </label>
                            <p class="setting-description">Receive SMS for urgent fraud alerts</p>
                        </div>
                        <div class="settings-group">
                            <label class="setting-toggle">
                                <input type="checkbox">
                                <span class="toggle-slider"></span>
                                <span class="toggle-label">Push Notifications</span>
                            </label>
                            <p class="setting-description">Browser push notifications for real-time updates</p>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Data Retention</h2>
                    </div>
                    <div class="card-body">
                        <div class="settings-group">
                            <label class="setting-label">
                                <span>Transaction Data Retention</span>
                                <select class="setting-select">
                                    <option>30 days</option>
                                    <option>90 days</option>
                                    <option selected>180 days</option>
                                    <option>1 year</option>
                                    <option>2 years</option>
                                </select>
                            </label>
                            <p class="setting-description">How long to retain transaction records</p>
                        </div>
                        <div class="settings-group">
                            <label class="setting-label">
                                <span>Audit Log Retention</span>
                                <select class="setting-select">
                                    <option>90 days</option>
                                    <option>180 days</option>
                                    <option selected>1 year</option>
                                    <option>2 years</option>
                                    <option>5 years</option>
                                </select>
                            </label>
                            <p class="setting-description">How long to retain audit logs for compliance</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
};

// Merge final pages with main pages object
Object.assign(pages, finalPages);
