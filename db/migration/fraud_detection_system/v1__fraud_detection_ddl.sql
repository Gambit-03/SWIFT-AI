-- ============================================================================
-- FRAUD DETECTION SYSTEM - DDL SCHEMA (v1)
-- Version: 1.0
-- Database: MySQL 8.0+
-- Description: Simplified fraud detection dashboard for analysts and admins
-- Purpose: Monitor, analyze, and manage fraud detection operations
-- ============================================================================

-- ============================================================================
-- SECTION 1: DATABASE CREATION
-- ============================================================================

CREATE DATABASE IF NOT EXISTS fraud_detection_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE fraud_detection_db;

-- ============================================================================
-- SECTION 2: USER MANAGEMENT
-- ============================================================================

-- Create application user with limited privileges
-- Note: Run these commands as root user
CREATE USER IF NOT EXISTS 'fraud_analyst'@'%' IDENTIFIED BY 'FraudAnalyst2026#Secure!';
GRANT SELECT, INSERT, UPDATE ON fraud_detection_db.* TO 'fraud_analyst'@'%';
CREATE USER IF NOT EXISTS 'fraud_admin'@'%' IDENTIFIED BY 'FraudAdmin2026#Secure!';
GRANT ALL PRIVILEGES ON fraud_detection_db.* TO 'fraud_admin'@'%';
FLUSH PRIVILEGES;

-- ============================================================================
-- SECTION 3: TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Table: system_users
-- Description: Users of fraud detection system (analysts & admins only)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS system_users (
    id VARCHAR(50) PRIMARY KEY DEFAULT (CONCAT('user_', UUID())),
    
    -- Basic Information
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    
    -- Role & Status
    user_role ENUM('FRAUD_ANALYST', 'ADMIN') NOT NULL,
    user_status ENUM('ACTIVE', 'SUSPENDED', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    
    -- Security
    two_factor_enabled BOOLEAN DEFAULT TRUE,
    last_password_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    failed_login_attempts INT DEFAULT 0,
    last_failed_login TIMESTAMP NULL,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL,
    
    -- Soft Delete
    deleted_at TIMESTAMP NULL,
    
    INDEX idx_email (email),
    INDEX idx_user_role (user_role),
    INDEX idx_user_status (user_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: monitored_transactions
-- Description: Transactions received from banking app for fraud analysis
-- Note: This table receives data via API from banking_app_db
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS monitored_transactions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    -- Transaction Reference (from banking app)
    external_transaction_id VARCHAR(50) UNIQUE NOT NULL COMMENT 'Transaction ID from banking app',
    reference_number VARCHAR(50) COMMENT 'Banking app reference number',
    
    -- Customer Information (anonymized/masked for privacy)
    customer_id_hash VARCHAR(255) NOT NULL COMMENT 'Hashed customer ID',
    customer_email_hash VARCHAR(255) COMMENT 'Hashed email for privacy',
    customer_risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'LOW',
    
    -- Transaction Details
    amount DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    merchant_name VARCHAR(200),
    merchant_category VARCHAR(50),
    transaction_type VARCHAR(50),
    
    -- Card Information (masked)
    card_last_4 CHAR(4),
    card_type VARCHAR(20),
    card_brand VARCHAR(20),
    
    -- Device & Location Context
    device_id VARCHAR(100),
    device_type VARCHAR(50),
    device_fingerprint VARCHAR(255),
    ip_address VARCHAR(45),
    location_city VARCHAR(100),
    location_country VARCHAR(3),
    location_latitude DECIMAL(10, 8),
    location_longitude DECIMAL(11, 8),
    
    -- Velocity Metrics (calculated in real-time)
    transactions_last_1h INT DEFAULT 0,
    transactions_last_24h INT DEFAULT 0,
    amount_sum_last_1h DECIMAL(12, 2) DEFAULT 0.00,
    amount_sum_last_24h DECIMAL(12, 2) DEFAULT 0.00,
    
    -- Fraud Detection Results
    fraud_score INT CHECK (fraud_score BETWEEN 0 AND 100),
    fraud_probability DECIMAL(5, 4) COMMENT 'ML model output (0.0000 to 1.0000)',
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL,
    decision ENUM('ALLOW', 'BLOCK', 'CHALLENGE', 'REVIEW') NOT NULL,
    decision_reason TEXT,
    
    -- ML Model Information
    model_version VARCHAR(20),
    model_confidence DECIMAL(5, 4),
    rules_triggered JSON COMMENT 'Array of rule IDs that triggered',
    
    -- Processing Status
    processing_status ENUM(
        'RECEIVED',
        'ANALYZING',
        'ANALYZED',
        'FLAGGED',
        'APPROVED',
        'BLOCKED'
    ) NOT NULL DEFAULT 'RECEIVED',
    
    -- Performance Metrics
    analysis_time_ms INT COMMENT 'Time taken for fraud analysis',
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analyzed_at TIMESTAMP NULL,
    
    -- Ground Truth & Feedback
    is_fraud BOOLEAN NULL COMMENT 'Actual fraud status (ground truth)',
    feedback_source VARCHAR(50) COMMENT 'chargeback, customer_report, analyst_review',
    feedback_at TIMESTAMP NULL,
    
    -- Additional Context
    additional_data JSON COMMENT 'Extra contextual information',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_external_txn_id (external_transaction_id),
    INDEX idx_customer_hash (customer_id_hash),
    INDEX idx_fraud_score (fraud_score),
    INDEX idx_risk_level (risk_level),
    INDEX idx_decision (decision),
    INDEX idx_processing_status (processing_status),
    INDEX idx_received_at (received_at),
    INDEX idx_is_fraud (is_fraud),
    INDEX idx_ip_address (ip_address),
    INDEX idx_device_id (device_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Partition by date for performance (optional for large datasets)
-- ALTER TABLE monitored_transactions PARTITION BY RANGE (TO_DAYS(received_at)) (
--     PARTITION p_2026_01 VALUES LESS THAN (TO_DAYS('2026-02-01')),
--     PARTITION p_2026_02 VALUES LESS THAN (TO_DAYS('2026-03-01'))
-- );

-- ----------------------------------------------------------------------------
-- Table: fraud_alerts
-- Description: High-risk transactions flagged for analyst review
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fraud_alerts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    -- Related Transaction
    transaction_id BIGINT NOT NULL,
    
    -- Alert Details
    alert_type VARCHAR(50) NOT NULL COMMENT 'high_amount, velocity, location_anomaly, device_change, etc.',
    severity ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL DEFAULT 'MEDIUM',
    priority INT DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    
    -- Alert Status
    alert_status ENUM(
        'PENDING',
        'ASSIGNED',
        'IN_REVIEW',
        'RESOLVED',
        'DISMISSED',
        'ESCALATED'
    ) NOT NULL DEFAULT 'PENDING',
    
    -- Assignment
    assigned_to VARCHAR(50) NULL COMMENT 'System user ID',
    assigned_at TIMESTAMP NULL,
    
    -- Review Details
    reviewed_by VARCHAR(50) NULL COMMENT 'System user ID',
    reviewed_at TIMESTAMP NULL,
    review_decision ENUM('APPROVE', 'BLOCK', 'ESCALATE', 'NEED_MORE_INFO'),
    review_notes TEXT,
    
    -- Alert Content
    description TEXT NOT NULL,
    recommendation TEXT,
    
    -- SLA Tracking
    response_time_minutes INT COMMENT 'Time to first response',
    resolution_time_minutes INT COMMENT 'Time to resolution',
    sla_breached BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    escalated_at TIMESTAMP NULL,
    
    FOREIGN KEY (transaction_id) REFERENCES monitored_transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES system_users(id),
    FOREIGN KEY (reviewed_by) REFERENCES system_users(id),
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_alert_status (alert_status),
    INDEX idx_severity (severity),
    INDEX idx_assigned_to (assigned_to),
    INDEX idx_created_at (created_at),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: fraud_rules
-- Description: Configurable fraud detection rules
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fraud_rules (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rule_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Rule Information
    rule_name VARCHAR(100) NOT NULL,
    description TEXT,
    rule_category VARCHAR(50) COMMENT 'velocity, amount, location, device, merchant',
    
    -- Rule Logic
    rule_type VARCHAR(50) NOT NULL COMMENT 'THRESHOLD, PATTERN, ANOMALY',
    condition_json JSON NOT NULL COMMENT 'Rule conditions in JSON format',
    threshold_value DECIMAL(12, 2),
    
    -- Rule Action
    action ENUM('FLAG', 'BLOCK', 'CHALLENGE', 'NOTIFY') NOT NULL,
    priority INT DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    
    -- Rule Configuration
    is_active BOOLEAN DEFAULT TRUE,
    is_mandatory BOOLEAN DEFAULT FALSE COMMENT 'Cannot be overridden',
    applies_to_amount_above DECIMAL(12, 2) COMMENT 'Only apply for amounts above this',
    
    -- Performance Metrics
    times_triggered INT DEFAULT 0,
    true_positives INT DEFAULT 0 COMMENT 'Correctly identified fraud',
    false_positives INT DEFAULT 0 COMMENT 'Incorrectly flagged legitimate txns',
    true_negatives INT DEFAULT 0,
    false_negatives INT DEFAULT 0,
    precision_rate DECIMAL(5, 4) COMMENT 'TP / (TP + FP)',
    recall_rate DECIMAL(5, 4) COMMENT 'TP / (TP + FN)',
    f1_score DECIMAL(5, 4),
    
    -- Metadata
    created_by VARCHAR(50) NOT NULL,
    last_modified_by VARCHAR(50),
    tags JSON COMMENT 'Array of tags for categorization',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_triggered_at TIMESTAMP NULL,
    
    -- Soft Delete
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (created_by) REFERENCES system_users(id),
    FOREIGN KEY (last_modified_by) REFERENCES system_users(id),
    INDEX idx_rule_id (rule_id),
    INDEX idx_is_active (is_active),
    INDEX idx_rule_category (rule_category),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: ml_models
-- Description: Machine learning model registry and versioning
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ml_models (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    model_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Model Information
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(20) NOT NULL,
    description TEXT,
    
    -- Model Details
    model_type VARCHAR(50) NOT NULL COMMENT 'xgboost, random_forest, neural_network, ensemble',
    algorithm VARCHAR(100),
    framework VARCHAR(50) COMMENT 'scikit-learn, tensorflow, pytorch, keras',
    
    -- Model Status
    model_status ENUM(
        'TRAINING',
        'TESTING',
        'STAGING',
        'PRODUCTION',
        'ARCHIVED',
        'FAILED'
    ) NOT NULL DEFAULT 'TRAINING',
    is_active BOOLEAN DEFAULT FALSE,
    
    -- Performance Metrics
    accuracy DECIMAL(5, 4),
    precision_score DECIMAL(5, 4),
    recall_score DECIMAL(5, 4),
    f1_score DECIMAL(5, 4),
    auc_roc DECIMAL(5, 4),
    confusion_matrix JSON,
    
    -- Training Information
    training_dataset_size INT,
    validation_dataset_size INT,
    test_dataset_size INT,
    training_duration_seconds INT,
    hyperparameters JSON,
    
    -- Feature Information
    features_used JSON COMMENT 'Array of feature names',
    feature_importance JSON COMMENT 'Feature importance scores',
    num_features INT,
    
    -- Deployment Information
    model_file_path TEXT COMMENT 'S3 path or file system path',
    model_size_mb DECIMAL(10, 2),
    avg_inference_time_ms INT,
    
    -- Versioning
    parent_model_id BIGINT NULL COMMENT 'Previous version',
    
    -- Metadata
    deployed_by VARCHAR(50),
    notes TEXT,
    
    -- Timestamps
    training_started_at TIMESTAMP NULL,
    training_completed_at TIMESTAMP NULL,
    deployed_at TIMESTAMP NULL,
    deprecated_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (parent_model_id) REFERENCES ml_models(id),
    FOREIGN KEY (deployed_by) REFERENCES system_users(id),
    INDEX idx_model_id (model_id),
    INDEX idx_model_status (model_status),
    INDEX idx_is_active (is_active),
    INDEX idx_model_version (model_version),
    UNIQUE KEY unique_model_version (model_name, model_version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: model_predictions
-- Description: Log of ML model predictions for analysis and retraining
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS model_predictions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    -- Related Entities
    transaction_id BIGINT NOT NULL,
    model_id BIGINT NOT NULL,
    
    -- Prediction Results
    prediction BOOLEAN NOT NULL COMMENT 'TRUE = fraud, FALSE = legitimate',
    probability DECIMAL(5, 4) NOT NULL CHECK (probability BETWEEN 0 AND 1),
    fraud_score INT NOT NULL CHECK (fraud_score BETWEEN 0 AND 100),
    confidence_level ENUM('LOW', 'MEDIUM', 'HIGH') NOT NULL,
    
    -- Feature Values (for explainability)
    features_json JSON NOT NULL COMMENT 'Feature values used for prediction',
    
    -- Explainability (SHAP values)
    shap_values JSON COMMENT 'SHAP values for each feature',
    top_contributing_features JSON COMMENT 'Top 5 features that influenced decision',
    
    -- Performance
    inference_time_ms INT,
    
    -- Ground Truth (for model evaluation)
    actual_label BOOLEAN NULL COMMENT 'Actual fraud status',
    is_correct BOOLEAN NULL COMMENT 'Whether prediction matched actual',
    feedback_received_at TIMESTAMP NULL,
    
    -- Timestamps
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (transaction_id) REFERENCES monitored_transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES ml_models(id),
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_model_id (model_id),
    INDEX idx_prediction (prediction),
    INDEX idx_predicted_at (predicted_at),
    INDEX idx_actual_label (actual_label)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: customer_profiles
-- Description: Behavioral profiles for monitored customers
-- Note: Built from transaction history for anomaly detection
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customer_profiles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id_hash VARCHAR(255) UNIQUE NOT NULL,
    
    -- Transaction Statistics
    total_transactions INT DEFAULT 0,
    total_amount DECIMAL(15, 2) DEFAULT 0.00,
    avg_transaction_amount DECIMAL(10, 2) DEFAULT 0.00,
    median_amount DECIMAL(10, 2) DEFAULT 0.00,
    max_amount DECIMAL(10, 2) DEFAULT 0.00,
    std_dev_amount DECIMAL(10, 2) DEFAULT 0.00,
    
    -- Behavioral Patterns
    common_merchants JSON COMMENT 'Array of frequently used merchants',
    common_categories JSON COMMENT 'Array of frequent transaction categories',
    typical_amounts JSON COMMENT 'Array of common transaction amounts',
    typical_transaction_hours JSON COMMENT 'Array of hours (0-23)',
    typical_days JSON COMMENT 'Array of day names',
    
    -- Location Patterns
    home_city VARCHAR(100),
    home_country VARCHAR(3),
    home_location JSON COMMENT '{lat, lon}',
    recent_cities JSON COMMENT 'Cities visited in last 30 days',
    countries_visited JSON COMMENT 'Countries visited in last 90 days',
    
    -- Device Patterns
    known_devices JSON COMMENT 'Array of known device fingerprints',
    primary_device_id VARCHAR(100),
    device_switches_30d INT DEFAULT 0,
    
    -- Risk Indicators
    fraud_incidents INT DEFAULT 0,
    chargebacks_90d INT DEFAULT 0,
    disputes_30d INT DEFAULT 0,
    blocked_transactions_30d INT DEFAULT 0,
    
    -- Risk Scores
    behavioral_risk_score INT DEFAULT 50 CHECK (behavioral_risk_score BETWEEN 0 AND 100),
    trust_score INT DEFAULT 50 CHECK (trust_score BETWEEN 0 AND 100),
    
    -- Activity Tracking
    first_transaction_at TIMESTAMP NULL,
    last_transaction_at TIMESTAMP NULL,
    last_fraud_incident_at TIMESTAMP NULL,
    
    -- Profile Metadata
    profile_completeness INT DEFAULT 0 CHECK (profile_completeness BETWEEN 0 AND 100),
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_customer_hash (customer_id_hash),
    INDEX idx_behavioral_risk (behavioral_risk_score),
    INDEX idx_trust_score (trust_score),
    INDEX idx_last_transaction (last_transaction_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: system_audit_logs
-- Description: Audit trail for fraud detection system operations
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS system_audit_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    -- Actor Information
    user_id VARCHAR(50) NULL,
    user_email VARCHAR(100),
    user_role VARCHAR(20),
    
    -- Action Details
    action VARCHAR(100) NOT NULL COMMENT 'login, review_alert, approve_transaction, update_rule',
    action_type ENUM('CREATE', 'READ', 'UPDATE', 'DELETE', 'EXECUTE') NOT NULL,
    entity_type VARCHAR(50) COMMENT 'alert, transaction, rule, model',
    entity_id VARCHAR(50),
    
    -- Request Context
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Change Tracking
    old_values JSON,
    new_values JSON,
    
    -- Status
    status VARCHAR(20) COMMENT 'success, failed, error',
    error_message TEXT,
    
    -- Additional Metadata
    metadata JSON,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES system_users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_entity_type (entity_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: system_sessions
-- Description: Active sessions for fraud analysts and admins
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS system_sessions (
    id VARCHAR(100) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    
    -- Session Details
    session_token VARCHAR(500) UNIQUE NOT NULL,
    refresh_token VARCHAR(500),
    
    -- Session Context
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    terminated_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES system_users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_session_token (session_token),
    INDEX idx_is_active (is_active),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: dashboard_metrics
-- Description: Pre-computed metrics for dashboard performance
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dashboard_metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    metric_date DATE NOT NULL,
    metric_hour TINYINT NULL CHECK (metric_hour BETWEEN 0 AND 23),
    
    -- Transaction Metrics
    total_transactions INT DEFAULT 0,
    total_amount DECIMAL(15, 2) DEFAULT 0.00,
    flagged_transactions INT DEFAULT 0,
    blocked_transactions INT DEFAULT 0,
    approved_transactions INT DEFAULT 0,
    
    -- Fraud Metrics
    confirmed_fraud_count INT DEFAULT 0,
    fraud_amount DECIMAL(15, 2) DEFAULT 0.00,
    fraud_rate DECIMAL(5, 4) DEFAULT 0.0000,
    
    -- Alert Metrics
    alerts_created INT DEFAULT 0,
    alerts_resolved INT DEFAULT 0,
    avg_resolution_time_minutes DECIMAL(10, 2),
    
    -- Performance Metrics
    true_positives INT DEFAULT 0,
    false_positives INT DEFAULT 0,
    true_negatives INT DEFAULT 0,
    false_negatives INT DEFAULT 0,
    model_accuracy DECIMAL(5, 4),
    model_precision DECIMAL(5, 4),
    model_recall DECIMAL(5, 4),
    
    -- Risk Distribution
    low_risk_count INT DEFAULT 0,
    medium_risk_count INT DEFAULT 0,
    high_risk_count INT DEFAULT 0,
    critical_risk_count INT DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_metric_datetime (metric_date, metric_hour),
    INDEX idx_metric_date (metric_date),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 4: VIEWS FOR DASHBOARD
-- ============================================================================

-- View: Real-time fraud alerts dashboard
CREATE OR REPLACE VIEW v_active_alerts AS
SELECT 
    fa.id,
    fa.alert_type,
    fa.severity,
    fa.priority,
    fa.alert_status,
    mt.external_transaction_id,
    mt.amount,
    mt.currency,
    mt.merchant_name,
    mt.fraud_score,
    mt.location_country,
    fa.assigned_to,
    u.full_name as assigned_to_name,
    fa.created_at,
    TIMESTAMPDIFF(MINUTE, fa.created_at, NOW()) as pending_minutes
FROM fraud_alerts fa
JOIN monitored_transactions mt ON fa.transaction_id = mt.id
LEFT JOIN system_users u ON fa.assigned_to = u.id
WHERE fa.alert_status IN ('PENDING', 'ASSIGNED', 'IN_REVIEW')
ORDER BY fa.severity DESC, fa.priority DESC, fa.created_at ASC;

-- View: High-risk transactions requiring immediate attention
CREATE OR REPLACE VIEW v_high_risk_transactions AS
SELECT 
    mt.id,
    mt.external_transaction_id,
    mt.amount,
    mt.currency,
    mt.merchant_name,
    mt.merchant_category,
    mt.fraud_score,
    mt.fraud_probability,
    mt.risk_level,
    mt.decision,
    mt.location_country,
    mt.location_city,
    mt.device_type,
    mt.processing_status,
    mt.received_at,
    cp.behavioral_risk_score,
    cp.trust_score,
    cp.fraud_incidents
FROM monitored_transactions mt
LEFT JOIN customer_profiles cp ON mt.customer_id_hash = cp.customer_id_hash
WHERE mt.risk_level IN ('HIGH', 'CRITICAL')
  AND mt.received_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY mt.fraud_score DESC, mt.received_at DESC;

-- View: Analyst performance metrics
CREATE OR REPLACE VIEW v_analyst_performance AS
SELECT 
    u.id,
    u.full_name,
    u.email,
    COUNT(DISTINCT fa.id) as total_alerts_reviewed,
    SUM(CASE WHEN fa.alert_status = 'RESOLVED' THEN 1 ELSE 0 END) as resolved_alerts,
    AVG(fa.resolution_time_minutes) as avg_resolution_time,
    COUNT(DISTINCT DATE(fa.reviewed_at)) as active_days,
    u.last_login_at
FROM system_users u
LEFT JOIN fraud_alerts fa ON u.id = fa.reviewed_by 
    AND fa.reviewed_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
WHERE u.user_role = 'FRAUD_ANALYST'
  AND u.user_status = 'ACTIVE'
GROUP BY u.id;

-- View: Model performance summary
CREATE OR REPLACE VIEW v_model_performance AS
SELECT 
    m.id,
    m.model_name,
    m.model_version,
    m.model_status,
    m.is_active,
    m.accuracy,
    m.precision_score,
    m.recall_score,
    m.f1_score,
    m.auc_roc,
    COUNT(mp.id) as total_predictions,
    SUM(CASE WHEN mp.prediction = TRUE THEN 1 ELSE 0 END) as fraud_predictions,
    SUM(CASE WHEN mp.is_correct = TRUE THEN 1 ELSE 0 END) as correct_predictions,
    AVG(mp.inference_time_ms) as avg_inference_time,
    m.deployed_at
FROM ml_models m
LEFT JOIN model_predictions mp ON m.id = mp.model_id
    AND mp.predicted_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
WHERE m.model_status IN ('STAGING', 'PRODUCTION')
GROUP BY m.id
ORDER BY m.is_active DESC, m.deployed_at DESC;

-- ============================================================================
-- SECTION 5: STORED PROCEDURES
-- ============================================================================

-- Procedure: Update customer profile statistics
DELIMITER //
CREATE PROCEDURE sp_update_customer_profile(IN p_customer_hash VARCHAR(255))
BEGIN
    DECLARE v_total_txns INT;
    DECLARE v_total_amt DECIMAL(15,2);
    DECLARE v_avg_amt DECIMAL(10,2);
    
    -- Calculate statistics
    SELECT 
        COUNT(*),
        SUM(amount),
        AVG(amount)
    INTO v_total_txns, v_total_amt, v_avg_amt
    FROM monitored_transactions
    WHERE customer_id_hash = p_customer_hash;
    
    -- Update or insert profile
    INSERT INTO customer_profiles (
        customer_id_hash,
        total_transactions,
        total_amount,
        avg_transaction_amount,
        last_transaction_at
    ) VALUES (
        p_customer_hash,
        v_total_txns,
        v_total_amt,
        v_avg_amt,
        NOW()
    )
    ON DUPLICATE KEY UPDATE
        total_transactions = v_total_txns,
        total_amount = v_total_amt,
        avg_transaction_amount = v_avg_amt,
        last_transaction_at = NOW(),
        last_updated_at = NOW();
END//
DELIMITER ;

-- Procedure: Calculate daily dashboard metrics
DELIMITER //
CREATE PROCEDURE sp_calculate_daily_metrics(IN p_date DATE)
BEGIN
    INSERT INTO dashboard_metrics (
        metric_date,
        total_transactions,
        total_amount,
        flagged_transactions,
        blocked_transactions,
        confirmed_fraud_count,
        fraud_amount,
        fraud_rate,
        alerts_created,
        low_risk_count,
        medium_risk_count,
        high_risk_count,
        critical_risk_count
    )
    SELECT 
        p_date,
        COUNT(*),
        SUM(amount),
        SUM(CASE WHEN processing_status = 'FLAGGED' THEN 1 ELSE 0 END),
        SUM(CASE WHEN decision = 'BLOCK' THEN 1 ELSE 0 END),
        SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END),
        SUM(CASE WHEN is_fraud = TRUE THEN amount ELSE 0 END),
        AVG(CASE WHEN is_fraud = TRUE THEN 1.0 ELSE 0.0 END),
        (SELECT COUNT(*) FROM fraud_alerts WHERE DATE(created_at) = p_date),
        SUM(CASE WHEN risk_level = 'LOW' THEN 1 ELSE 0 END),
        SUM(CASE WHEN risk_level = 'MEDIUM' THEN 1 ELSE 0 END),
        SUM(CASE WHEN risk_level = 'HIGH' THEN 1 ELSE 0 END),
        SUM(CASE WHEN risk_level = 'CRITICAL' THEN 1 ELSE 0 END)
    FROM monitored_transactions
    WHERE DATE(received_at) = p_date
    ON DUPLICATE KEY UPDATE
        total_transactions = VALUES(total_transactions),
        total_amount = VALUES(total_amount),
        flagged_transactions = VALUES(flagged_transactions),
        blocked_transactions = VALUES(blocked_transactions),
        confirmed_fraud_count = VALUES(confirmed_fraud_count),
        fraud_amount = VALUES(fraud_amount),
        fraud_rate = VALUES(fraud_rate),
        updated_at = NOW();
END//
DELIMITER ;

-- ============================================================================
-- SECTION 6: TRIGGERS
-- ============================================================================

-- Trigger: Create alert for high-risk transactions
DELIMITER //
CREATE TRIGGER trg_create_alert_for_high_risk
AFTER INSERT ON monitored_transactions
FOR EACH ROW
BEGIN
    IF NEW.risk_level IN ('HIGH', 'CRITICAL') OR NEW.fraud_score >= 70 THEN
        INSERT INTO fraud_alerts (
            transaction_id,
            alert_type,
            severity,
            priority,
            description,
            recommendation
        ) VALUES (
            NEW.id,
            CASE 
                WHEN NEW.fraud_score >= 90 THEN 'critical_fraud_score'
                WHEN NEW.risk_level = 'CRITICAL' THEN 'critical_risk_level'
                ELSE 'high_risk_transaction'
            END,
            NEW.risk_level,
            CASE 
                WHEN NEW.fraud_score >= 90 THEN 10
                WHEN NEW.fraud_score >= 80 THEN 8
                ELSE 6
            END,
            CONCAT('High-risk transaction detected: Amount ', NEW.currency, ' ', NEW.amount, 
                   ', Fraud Score: ', NEW.fraud_score),
            'Immediate review recommended. Contact customer if necessary.'
        );
    END IF;
END//
DELIMITER ;

-- Trigger: Update fraud rule performance metrics
DELIMITER //
CREATE TRIGGER trg_update_rule_performance
AFTER UPDATE ON monitored_transactions
FOR EACH ROW
BEGIN
    IF NEW.is_fraud IS NOT NULL AND OLD.is_fraud IS NULL THEN
        -- Update rule statistics when ground truth is provided
        -- This is a simplified version; in production, you'd iterate through triggered rules
        UPDATE fraud_rules
        SET times_triggered = times_triggered + 1,
            last_triggered_at = NEW.analyzed_at
        WHERE rule_id IN (
            SELECT JSON_UNQUOTE(JSON_EXTRACT(NEW.rules_triggered, CONCAT('$[', idx, ']')))
            FROM (SELECT 0 as idx UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) nums
            WHERE JSON_EXTRACT(NEW.rules_triggered, CONCAT('$[', idx, ']')) IS NOT NULL
        );
    END IF;
END//
DELIMITER ;

-- ============================================================================
-- SCRIPT COMPLETION
-- ============================================================================

SELECT '========================================' as '';
SELECT 'FRAUD DETECTION SYSTEM DDL CREATED' as '';
SELECT '========================================' as '';
SELECT 'Database: fraud_detection_db' as '';
SELECT 'Tables Created: 13' as '';
SELECT 'Views Created: 4' as '';
SELECT 'Stored Procedures: 2' as '';
SELECT 'Triggers: 2' as '';
SELECT '' as '';
SELECT 'User Roles: FRAUD_ANALYST, ADMIN' as '';
SELECT '' as '';
SELECT 'Next Step: Run fraud_detection_v2_dml.sql' as '';
SELECT '========================================' as '';