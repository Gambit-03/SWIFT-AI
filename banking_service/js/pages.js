// Additional Page Templates (Customer Profile, Risk Scoring, Analytics, etc.)

const additionalPages = {
    'customer-profile': `
        <div class="customer-profile-page fade-in">
            <div class="page-header">
                <h2>Customer Behavioral Profile</h2>
                <div class="header-controls">
                    <input type="text" placeholder="Search User ID..." class="search-input" style="width: 300px;">
                    <button class="btn btn-primary">
                        <i class="fas fa-search"></i> Search
                    </button>
                </div>
            </div>

            <div class="profile-overview card" style="margin-top: var(--spacing-md);">
                <div class="profile-header">
                    <div class="profile-avatar">
                        <img src="https://ui-avatars.com/api/?name=John+Doe&background=FF6B6B&color=fff&size=120" alt="User">
                        <div class="profile-status online">
                            <i class="fas fa-circle"></i> Active
                        </div>
                    </div>
                    <div class="profile-info">
                        <h2>John Doe</h2>
                        <p class="profile-id"><code>USR-45821</code></p>
                        <div class="profile-meta">
                            <span><i class="fas fa-calendar"></i> Member since Jan 2022</span>
                            <span><i class="fas fa-location-dot"></i> New York, USA</span>
                            <span><i class="fas fa-envelope"></i> john.doe@email.com</span>
                        </div>
                    </div>
                    <div class="profile-risk-summary">
                        <div class="risk-gauge-mini">
                            <div class="gauge-value" style="color: var(--accent-success);">28</div>
                            <div class="gauge-label">Current Risk Score</div>
                        </div>
                        <span class="badge-status badge-success">Low Risk</span>
                    </div>
                </div>
            </div>

            <div class="grid grid-3" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Behavioral Baseline</h2>
                    </div>
                    <div class="card-body">
                        <div class="baseline-metrics">
                            <div class="baseline-item">
                                <div class="baseline-icon" style="color: var(--accent-secondary);">
                                    <i class="fas fa-dollar-sign"></i>
                                </div>
                                <div class="baseline-content">
                                    <p class="baseline-label">Avg Transaction</p>
                                    <h4 class="baseline-value">$3,245</h4>
                                    <span class="baseline-range">Range: $500 - $8,000</span>
                                </div>
                            </div>
                            <div class="baseline-item">
                                <div class="baseline-icon" style="color: var(--accent-tertiary);">
                                    <i class="fas fa-clock"></i>
                                </div>
                                <div class="baseline-content">
                                    <p class="baseline-label">Typical Time</p>
                                    <h4 class="baseline-value">9 AM - 6 PM</h4>
                                    <span class="baseline-range">Weekdays</span>
                                </div>
                            </div>
                            <div class="baseline-item">
                                <div class="baseline-icon" style="color: var(--accent-primary);">
                                    <i class="fas fa-chart-line"></i>
                                </div>
                                <div class="baseline-content">
                                    <p class="baseline-label">Frequency</p>
                                    <h4 class="baseline-value">12-15/month</h4>
                                    <span class="baseline-range">Consistent pattern</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Location History</h2>
                    </div>
                    <div class="card-body">
                        <div class="location-list">
                            <div class="location-item">
                                <div class="location-icon primary">
                                    <i class="fas fa-home"></i>
                                </div>
                                <div class="location-content">
                                    <h4>New York, USA</h4>
                                    <p>Primary location - 87% of transactions</p>
                                </div>
                            </div>
                            <div class="location-item">
                                <div class="location-icon secondary">
                                    <i class="fas fa-location-dot"></i>
                                </div>
                                <div class="location-content">
                                    <h4>Los Angeles, USA</h4>
                                    <p>Secondary - 8% of transactions</p>
                                </div>
                            </div>
                            <div class="location-item">
                                <div class="location-icon tertiary">
                                    <i class="fas fa-plane"></i>
                                </div>
                                <div class="location-content">
                                    <h4>London, UK</h4>
                                    <p>Travel - 5% of transactions</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Device Fingerprints</h2>
                    </div>
                    <div class="card-body">
                        <div class="device-list">
                            <div class="device-item trusted">
                                <div class="device-icon">
                                    <i class="fas fa-laptop"></i>
                                </div>
                                <div class="device-content">
                                    <h4>MacBook Pro</h4>
                                    <p>macOS 14.2 • Chrome</p>
                                    <span class="device-badge trusted">Trusted</span>
                                </div>
                            </div>
                            <div class="device-item trusted">
                                <div class="device-icon">
                                    <i class="fas fa-mobile"></i>
                                </div>
                                <div class="device-content">
                                    <h4>iPhone 14 Pro</h4>
                                    <p>iOS 17.2 • Safari</p>
                                    <span class="device-badge trusted">Trusted</span>
                                </div>
                            </div>
                            <div class="device-item">
                                <div class="device-icon">
                                    <i class="fas fa-tablet"></i>
                                </div>
                                <div class="device-content">
                                    <h4>iPad Air</h4>
                                    <p>iPadOS 17.1 • Safari</p>
                                    <span class="device-badge">Recognized</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Transaction Behavior Timeline</h2>
                    </div>
                    <div class="card-body">
                        <canvas id="behaviorTimelineChart" style="max-height: 300px;"></canvas>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Spending Heatmap</h2>
                    </div>
                    <div class="card-body">
                        <div class="heatmap-container">
                            <div class="heatmap-grid">
                                <!-- Time-based heatmap visualization -->
                                <div class="heatmap-placeholder" style="background: var(--bg-tertiary); height: 300px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
                                    <div style="text-align: center; color: var(--text-muted);">
                                        <i class="fas fa-fire" style="font-size: 3rem; margin-bottom: 1rem; color: var(--accent-primary);"></i>
                                        <p>Transaction heatmap by time & day</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Fraud History</h2>
                </div>
                <div class="card-body">
                    <div class="fraud-history-empty" style="text-align: center; padding: var(--spacing-xl); color: var(--text-muted);">
                        <i class="fas fa-shield-check" style="font-size: 4rem; color: var(--accent-success); margin-bottom: var(--spacing-md);"></i>
                        <h3 style="color: var(--accent-success); margin-bottom: var(--spacing-sm);">Clean Record</h3>
                        <p>No confirmed fraud incidents for this user</p>
                    </div>
                </div>
            </div>
        </div>
    `,

    'risk-scoring': `
        <div class="risk-scoring-page fade-in">
            <div class="page-header">
                <h2>Risk Scoring & Anomaly Insights</h2>
                <div class="header-controls">
                    <button class="btn btn-secondary">
                        <i class="fas fa-sliders"></i> Configure Thresholds
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-download"></i> Export Report
                    </button>
                </div>
            </div>

            <div class="risk-overview grid grid-4" style="margin-top: var(--spacing-md);">
                <div class="risk-stat-card card">
                    <div class="risk-stat-header">
                        <h3>Critical Risk</h3>
                        <div class="risk-indicator critical"></div>
                    </div>
                    <div class="risk-stat-value">247</div>
                    <div class="risk-stat-label">Score > 80</div>
                </div>
                <div class="risk-stat-card card">
                    <div class="risk-stat-header">
                        <h3>High Risk</h3>
                        <div class="risk-indicator high"></div>
                    </div>
                    <div class="risk-stat-value">1,842</div>
                    <div class="risk-stat-label">Score 60-80</div>
                </div>
                <div class="risk-stat-card card">
                    <div class="risk-stat-header">
                        <h3>Medium Risk</h3>
                        <div class="risk-indicator medium"></div>
                    </div>
                    <div class="risk-stat-value">3,456</div>
                    <div class="risk-stat-label">Score 40-60</div>
                </div>
                <div class="risk-stat-card card">
                    <div class="risk-stat-header">
                        <h3>Low Risk</h3>
                        <div class="risk-indicator low"></div>
                    </div>
                    <div class="risk-stat-value">42,187</div>
                    <div class="risk-stat-label">Score < 40</div>
                </div>
            </div>

            <div class="grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Risk Score Distribution</h2>
                    </div>
                    <div class="card-body">
                        <canvas id="riskDistChart" style="max-height: 350px;"></canvas>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Anomaly Detection Insights</h2>
                    </div>
                    <div class="card-body">
                        <div class="anomaly-insights">
                            <div class="insight-item">
                                <div class="insight-header">
                                    <div class="insight-icon" style="background: rgba(255, 107, 107, 0.2); color: var(--accent-danger);">
                                        <i class="fas fa-location-crosshairs"></i>
                                    </div>
                                    <h4>Geo-Velocity Anomalies</h4>
                                </div>
                                <div class="insight-stats">
                                    <div class="insight-stat">
                                        <span class="stat-number">89</span>
                                        <span class="stat-label">Detected Today</span>
                                    </div>
                                    <div class="insight-stat">
                                        <span class="stat-number">+23%</span>
                                        <span class="stat-label">vs Yesterday</span>
                                    </div>
                                </div>
                                <p class="insight-description">Impossible travel patterns detected between transaction locations</p>
                            </div>

                            <div class="insight-item">
                                <div class="insight-header">
                                    <div class="insight-icon" style="background: rgba(255, 169, 77, 0.2); color: var(--accent-warning);">
                                        <i class="fas fa-gauge-high"></i>
                                    </div>
                                    <h4>Velocity Spikes</h4>
                                </div>
                                <div class="insight-stats">
                                    <div class="insight-stat">
                                        <span class="stat-number">156</span>
                                        <span class="stat-label">Detected Today</span>
                                    </div>
                                    <div class="insight-stat">
                                        <span class="stat-number">+12%</span>
                                        <span class="stat-label">vs Yesterday</span>
                                    </div>
                                </div>
                                <p class="insight-description">Unusual transaction frequency patterns identified</p>
                            </div>

                            <div class="insight-item">
                                <div class="insight-header">
                                    <div class="insight-icon" style="background: rgba(78, 205, 196, 0.2); color: var(--accent-secondary);">
                                        <i class="fas fa-chart-line"></i>
                                    </div>
                                    <h4>Amount Deviations</h4>
                                </div>
                                <div class="insight-stats">
                                    <div class="insight-stat">
                                        <span class="stat-number">234</span>
                                        <span class="stat-label">Detected Today</span>
                                    </div>
                                    <div class="insight-stat">
                                        <span class="stat-number">-8%</span>
                                        <span class="stat-label">vs Yesterday</span>
                                    </div>
                                </div>
                                <p class="insight-description">Transactions significantly outside normal spending patterns</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Risk Factor Breakdown</h2>
                </div>
                <div class="card-body">
                    <div class="risk-factors-grid grid grid-3">
                        <div class="risk-factor-card">
                            <h4>Behavioral Risk</h4>
                            <div class="factor-gauge">
                                <div class="gauge-bar">
                                    <div class="gauge-fill" style="width: 34%; background: var(--accent-success);"></div>
                                </div>
                                <span class="gauge-percentage">34%</span>
                            </div>
                            <p class="factor-description">Deviation from learned user behavior patterns</p>
                        </div>
                        <div class="risk-factor-card">
                            <h4>Anomaly Score</h4>
                            <div class="factor-gauge">
                                <div class="gauge-bar">
                                    <div class="gauge-fill" style="width: 67%; background: var(--accent-warning);"></div>
                                </div>
                                <span class="gauge-percentage">67%</span>
                            </div>
                            <p class="factor-description">Statistical anomaly detection score</p>
                        </div>
                        <div class="risk-factor-card">
                            <h4>Rule-Based Score</h4>
                            <div class="factor-gauge">
                                <div class="gauge-bar">
                                    <div class="gauge-fill" style="width: 89%; background: var(--accent-danger);"></div>
                                </div>
                                <span class="gauge-percentage">89%</span>
                            </div>
                            <p class="factor-description">Traditional rule-based fraud indicators</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,

    'analytics': `
        <div class="analytics-page fade-in">
            <div class="page-header">
                <h2>Analytics & Reports</h2>
                <div class="header-controls">
                    <select class="filter-select">
                        <option>Last 24 Hours</option>
                        <option>Last 7 Days</option>
                        <option>Last 30 Days</option>
                        <option>Custom Range</option>
                    </select>
                    <button class="btn btn-secondary">
                        <i class="fas fa-calendar"></i> Custom Date
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-file-export"></i> Export Report
                    </button>
                </div>
            </div>

            <div class="analytics-summary grid grid-4" style="margin-top: var(--spacing-md);">
                <div class="analytics-card card">
                    <div class="analytics-icon" style="color: var(--accent-danger);">
                        <i class="fas fa-shield-halved"></i>
                    </div>
                    <h3>Total Fraud Detected</h3>
                    <div class="analytics-value">1,247</div>
                    <div class="analytics-change danger">
                        <i class="fas fa-arrow-up"></i> 15% from last period
                    </div>
                </div>
                <div class="analytics-card card">
                    <div class="analytics-icon" style="color: var(--accent-success);">
                        <i class="fas fa-dollar-sign"></i>
                    </div>
                    <h3>Loss Prevented</h3>
                    <div class="analytics-value">$2.4M</div>
                    <div class="analytics-change success">
                        <i class="fas fa-arrow-up"></i> 28% from last period
                    </div>
                </div>
                <div class="analytics-card card">
                    <div class="analytics-icon" style="color: var(--accent-warning);">
                        <i class="fas fa-percentage"></i>
                    </div>
                    <h3>False Positive Rate</h3>
                    <div class="analytics-value">1.2%</div>
                    <div class="analytics-change success">
                        <i class="fas fa-arrow-down"></i> 0.3% from last period
                    </div>
                </div>
                <div class="analytics-card card">
                    <div class="analytics-icon" style="color: var(--accent-secondary);">
                        <i class="fas fa-bullseye"></i>
                    </div>
                    <h3>Detection Accuracy</h3>
                    <div class="analytics-value">98.7%</div>
                    <div class="analytics-change success">
                        <i class="fas fa-arrow-up"></i> 0.5% from last period
                    </div>
                </div>
            </div>

            <div class="grid grid-2" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Fraud Trends Over Time</h2>
                        <div class="chart-legend">
                            <span class="legend-item"><span class="legend-dot" style="background: var(--accent-danger);"></span> Fraud Detected</span>
                            <span class="legend-item"><span class="legend-dot" style="background: var(--accent-success);"></span> Legitimate</span>
                        </div>
                    </div>
                    <div class="card-body">
                        <canvas id="fraudTrendsChart" style="max-height: 350px;"></canvas>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Fraud by Category</h2>
                    </div>
                    <div class="card-body">
                        <canvas id="fraudCategoryChart" style="max-height: 350px;"></canvas>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top: var(--spacing-lg);">
                <div class="card-header">
                    <h2 class="card-title">Model Performance Comparison</h2>
                </div>
                <div class="card-body">
                    <div class="performance-table-wrapper">
                        <table class="performance-table">
                            <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Current Model</th>
                                    <th>Previous Model</th>
                                    <th>Change</th>
                                    <th>Industry Benchmark</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Accuracy</strong></td>
                                    <td><span class="metric-badge success">98.7%</span></td>
                                    <td>97.2%</td>
                                    <td><span class="change-badge positive">+1.5%</span></td>
                                    <td>95.0%</td>
                                </tr>
                                <tr>
                                    <td><strong>Precision</strong></td>
                                    <td><span class="metric-badge success">96.3%</span></td>
                                    <td>94.8%</td>
                                    <td><span class="change-badge positive">+1.5%</span></td>
                                    <td>92.0%</td>
                                </tr>
                                <tr>
                                    <td><strong>Recall</strong></td>
                                    <td><span class="metric-badge success">97.1%</span></td>
                                    <td>95.5%</td>
                                    <td><span class="change-badge positive">+1.6%</span></td>
                                    <td>90.0%</td>
                                </tr>
                                <tr>
                                    <td><strong>F1 Score</strong></td>
                                    <td><span class="metric-badge success">96.7%</span></td>
                                    <td>95.1%</td>
                                    <td><span class="change-badge positive">+1.6%</span></td>
                                    <td>91.0%</td>
                                </tr>
                                <tr>
                                    <td><strong>False Positive Rate</strong></td>
                                    <td><span class="metric-badge success">1.2%</span></td>
                                    <td>1.5%</td>
                                    <td><span class="change-badge positive">-0.3%</span></td>
                                    <td>3.0%</td>
                                </tr>
                                <tr>
                                    <td><strong>Avg Detection Time</strong></td>
                                    <td><span class="metric-badge success">47ms</span></td>
                                    <td>62ms</td>
                                    <td><span class="change-badge positive">-15ms</span></td>
                                    <td>100ms</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="grid grid-3" style="margin-top: var(--spacing-lg);">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Top Fraud Patterns</h2>
                    </div>
                    <div class="card-body">
                        <div class="pattern-list">
                            <div class="pattern-item">
                                <div class="pattern-rank">1</div>
                                <div class="pattern-content">
                                    <h4>Geo-Velocity Anomaly</h4>
                                    <div class="pattern-bar">
                                        <div class="pattern-fill" style="width: 89%; background: var(--accent-danger);"></div>
                                    </div>
                                    <span class="pattern-count">234 cases</span>
                                </div>
                            </div>
                            <div class="pattern-item">
                                <div class="pattern-rank">2</div>
                                <div class="pattern-content">
                                    <h4>Large Amount Deviation</h4>
                                    <div class="pattern-bar">
                                        <div class="pattern-fill" style="width: 76%; background: var(--accent-warning);"></div>
                                    </div>
                                    <span class="pattern-count">198 cases</span>
                                </div>
                            </div>
                            <div class="pattern-item">
                                <div class="pattern-rank">3</div>
                                <div class="pattern-content">
                                    <h4>Unusual Time Pattern</h4>
                                    <div class="pattern-bar">
                                        <div class="pattern-fill" style="width: 65%; background: var(--accent-warning);"></div>
                                    </div>
                                    <span class="pattern-count">167 cases</span>
                                </div>
                            </div>
                            <div class="pattern-item">
                                <div class="pattern-rank">4</div>
                                <div class="pattern-content">
                                    <h4>New Device</h4>
                                    <div class="pattern-bar">
                                        <div class="pattern-fill" style="width: 54%; background: var(--accent-secondary);"></div>
                                    </div>
                                    <span class="pattern-count">142 cases</span>
                                </div>
                            </div>
                            <div class="pattern-item">
                                <div class="pattern-rank">5</div>
                                <div class="pattern-content">
                                    <h4>Velocity Spike</h4>
                                    <div class="pattern-bar">
                                        <div class="pattern-fill" style="width: 48%; background: var(--accent-secondary);"></div>
                                    </div>
                                    <span class="pattern-count">126 cases</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Geographic Distribution</h2>
                    </div>
                    <div class="card-body">
                        <div class="geo-list">
                            <div class="geo-item">
                                <div class="geo-flag">🇳🇬</div>
                                <div class="geo-content">
                                    <h4>Nigeria</h4>
                                    <div class="geo-bar">
                                        <div class="geo-fill" style="width: 34%; background: var(--accent-danger);"></div>
                                    </div>
                                    <span class="geo-percentage">34%</span>
                                </div>
                            </div>
                            <div class="geo-item">
                                <div class="geo-flag">🇷🇺</div>
                                <div class="geo-content">
                                    <h4>Russia</h4>
                                    <div class="geo-bar">
                                        <div class="geo-fill" style="width: 23%; background: var(--accent-danger);"></div>
                                    </div>
                                    <span class="geo-percentage">23%</span>
                                </div>
                            </div>
                            <div class="geo-item">
                                <div class="geo-flag">🇨🇳</div>
                                <div class="geo-content">
                                    <h4>China</h4>
                                    <div class="geo-bar">
                                        <div class="geo-fill" style="width: 18%; background: var(--accent-warning);"></div>
                                    </div>
                                    <span class="geo-percentage">18%</span>
                                </div>
                            </div>
                            <div class="geo-item">
                                <div class="geo-flag">🇧🇷</div>
                                <div class="geo-content">
                                    <h4>Brazil</h4>
                                    <div class="geo-bar">
                                        <div class="geo-fill" style="width: 15%; background: var(--accent-warning);"></div>
                                    </div>
                                    <span class="geo-percentage">15%</span>
                                </div>
                            </div>
                            <div class="geo-item">
                                <div class="geo-flag">🇮🇳</div>
                                <div class="geo-content">
                                    <h4>India</h4>
                                    <div class="geo-bar">
                                        <div class="geo-fill" style="width: 10%; background: var(--accent-secondary);"></div>
                                    </div>
                                    <span class="geo-percentage">10%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Scheduled Reports</h2>
                    </div>
                    <div class="card-body">
                        <div class="reports-list">
                            <div class="report-item">
                                <div class="report-icon">
                                    <i class="fas fa-file-pdf"></i>
                                </div>
                                <div class="report-content">
                                    <h4>Daily Fraud Summary</h4>
                                    <p>PDF • Every day at 9:00 AM</p>
                                </div>
                                <button class="btn-icon"><i class="fas fa-download"></i></button>
                            </div>
                            <div class="report-item">
                                <div class="report-icon">
                                    <i class="fas fa-file-excel"></i>
                                </div>
                                <div class="report-content">
                                    <h4>Weekly Analytics</h4>
                                    <p>Excel • Every Monday at 8:00 AM</p>
                                </div>
                                <button class="btn-icon"><i class="fas fa-download"></i></button>
                            </div>
                            <div class="report-item">
                                <div class="report-icon">
                                    <i class="fas fa-file-csv"></i>
                                </div>
                                <div class="report-content">
                                    <h4>Monthly Performance</h4>
                                    <p>CSV • 1st of every month</p>
                                </div>
                                <button class="btn-icon"><i class="fas fa-download"></i></button>
                            </div>
                        </div>
                        <button class="btn btn-secondary" style="width: 100%; margin-top: var(--spacing-md);">
                            <i class="fas fa-plus"></i> Create New Report
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `
};

// Merge additional pages with main pages object
Object.assign(pages, additionalPages);
