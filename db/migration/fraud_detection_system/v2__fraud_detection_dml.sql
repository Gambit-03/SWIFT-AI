-- ============================================================================
-- FRAUD DETECTION SYSTEM - DML SEED DATA (v2)
-- Version: 1.0
-- Database: MySQL 8.0+
-- Description: Sample data for testing fraud detection dashboard
-- ============================================================================

USE fraud_detection_db;

-- ============================================================================
-- SECTION 1: SYSTEM USERS (Fraud Analysts & Admins)
-- ============================================================================

INSERT INTO system_users (
    id, full_name, email, password_hash, phone,
    user_role, user_status, two_factor_enabled
) VALUES
-- Admin User
(
    'user_admin_001',
    'Admin User',
    'admin@frauddetection.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm', -- password: AdminPass123!
    '+1-555-9001',
    'ADMIN',
    'ACTIVE',
    TRUE
),

-- Fraud Analysts
(
    'user_analyst_001',
    'Alice Johnson',
    'alice.johnson@frauddetection.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm', -- password: AnalystPass123!
    '+1-555-9002',
    'FRAUD_ANALYST',
    'ACTIVE',
    TRUE
),
(
    'user_analyst_002',
    'Bob Martinez',
    'bob.martinez@frauddetection.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm',
    '+1-555-9003',
    'FRAUD_ANALYST',
    'ACTIVE',
    TRUE
),
(
    'user_analyst_003',
    'Carol White',
    'carol.white@frauddetection.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm',
    '+1-555-9004',
    'FRAUD_ANALYST',
    'ACTIVE',
    TRUE
),
(
    'user_analyst_004',
    'David Chen',
    'david.chen@frauddetection.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm',
    '+1-555-9005',
    'FRAUD_ANALYST',
    'ACTIVE',
    FALSE
);

-- ============================================================================
-- SECTION 2: ML MODELS
-- ============================================================================

INSERT INTO ml_models (
    model_id, model_name, model_version, description,
    model_type, algorithm, framework,
    model_status, is_active,
    accuracy, precision_score, recall_score, f1_score, auc_roc,
    training_dataset_size, validation_dataset_size, test_dataset_size,
    training_duration_seconds,
    features_used, num_features,
    model_file_path, model_size_mb, avg_inference_time_ms,
    deployed_by, deployed_at
) VALUES
-- Production Model
(
    'model_xgb_prod_001',
    'XGBoost Fraud Detector',
    'v2.1.0',
    'Production fraud detection model using XGBoost with SMOTE for handling imbalanced data',
    'xgboost',
    'Gradient Boosting',
    'xgboost',
    'PRODUCTION',
    TRUE,
    0.9650,
    0.9200,
    0.8800,
    0.8995,
    0.9750,
    500000,
    100000,
    50000,
    3600,
    JSON_ARRAY(
        'amount', 'merchant_category', 'hour_of_day', 'day_of_week',
        'location_distance', 'device_age_days', 'velocity_1h', 'velocity_24h',
        'avg_amount_7d', 'merchant_fraud_rate', 'customer_risk_score',
        'amount_deviation', 'international_transaction', 'card_present',
        'customer_age_days', 'previous_fraud_count'
    ),
    16,
    '/models/xgboost_v2.1.0.pkl',
    45.50,
    12,
    'user_admin_001',
    '2025-12-01 10:00:00'
),

-- Staging Model (being tested)
(
    'model_rf_staging_001',
    'Random Forest Fraud Detector',
    'v1.5.0',
    'Random Forest model in staging for A/B testing',
    'random_forest',
    'Random Forest Classifier',
    'scikit-learn',
    'STAGING',
    FALSE,
    0.9580,
    0.9100,
    0.8600,
    0.8844,
    0.9680,
    500000,
    100000,
    50000,
    2400,
    JSON_ARRAY(
        'amount', 'merchant_category', 'hour_of_day', 'day_of_week',
        'location_distance', 'device_age_days', 'velocity_1h', 'velocity_24h',
        'avg_amount_7d', 'merchant_fraud_rate', 'customer_risk_score',
        'amount_deviation', 'international_transaction', 'card_present'
    ),
    14,
    '/models/random_forest_v1.5.0.pkl',
    120.00,
    8,
    'user_admin_001',
    NULL
),

-- Archived Model
(
    'model_xgb_arch_001',
    'XGBoost Fraud Detector',
    'v1.0.0',
    'Previous production model - archived after v2.1.0 deployment',
    'xgboost',
    'Gradient Boosting',
    'xgboost',
    'ARCHIVED',
    FALSE,
    0.9450,
    0.8900,
    0.8400,
    0.8644,
    0.9600,
    300000,
    75000,
    25000,
    2700,
    JSON_ARRAY(
        'amount', 'merchant_category', 'hour_of_day',
        'velocity_24h', 'customer_risk_score', 'amount_deviation'
    ),
    6,
    '/models/xgboost_v1.0.0.pkl',
    32.00,
    15,
    'user_admin_001',
    '2025-06-01 10:00:00'
);

-- ============================================================================
-- SECTION 3: FRAUD RULES
-- ============================================================================

INSERT INTO fraud_rules (
    rule_id, rule_name, description, rule_category,
    rule_type, condition_json, threshold_value,
    action, priority, is_active, is_mandatory,
    created_by
) VALUES
-- Rule 1: High Amount Transaction
(
    'RULE_HIGH_AMOUNT_001',
    'High Amount Transaction Alert',
    'Flag transactions above $5000 for review',
    'amount',
    'THRESHOLD',
    JSON_OBJECT(
        'field', 'amount',
        'operator', 'greater_than',
        'value', 5000
    ),
    5000.00,
    'FLAG',
    8,
    TRUE,
    FALSE,
    'user_admin_001'
),

-- Rule 2: Velocity Check - Transactions per hour
(
    'RULE_VELOCITY_1H_001',
    'Multiple Transactions in 1 Hour',
    'Block if more than 5 transactions in 1 hour',
    'velocity',
    'THRESHOLD',
    JSON_OBJECT(
        'field', 'transactions_last_1h',
        'operator', 'greater_than',
        'value', 5
    ),
    5.00,
    'BLOCK',
    9,
    TRUE,
    TRUE,
    'user_admin_001'
),

-- Rule 3: International Transaction
(
    'RULE_INTL_TXN_001',
    'International Transaction Review',
    'Challenge international transactions above $1000',
    'location',
    'PATTERN',
    JSON_OBJECT(
        'conditions', JSON_ARRAY(
            JSON_OBJECT('field', 'location_country', 'operator', 'not_equals', 'value', 'USA'),
            JSON_OBJECT('field', 'amount', 'operator', 'greater_than', 'value', 1000)
        ),
        'logic', 'AND'
    ),
    1000.00,
    'CHALLENGE',
    7,
    TRUE,
    FALSE,
    'user_admin_001'
),

-- Rule 4: Device Change
(
    'RULE_DEVICE_CHANGE_001',
    'New Device Detection',
    'Flag transactions from unknown devices',
    'device',
    'PATTERN',
    JSON_OBJECT(
        'field', 'device_fingerprint',
        'operator', 'not_in',
        'value', 'known_devices'
    ),
    NULL,
    'FLAG',
    6,
    TRUE,
    FALSE,
    'user_admin_001'
),

-- Rule 5: Unusual Hour
(
    'RULE_UNUSUAL_HOUR_001',
    'Transaction at Unusual Hour',
    'Flag transactions between 2 AM - 5 AM',
    'velocity',
    'PATTERN',
    JSON_OBJECT(
        'field', 'hour_of_day',
        'operator', 'between',
        'value', JSON_ARRAY(2, 5)
    ),
    NULL,
    'FLAG',
    4,
    TRUE,
    FALSE,
    'user_admin_001'
),

-- Rule 6: High Velocity Amount
(
    'RULE_VELOCITY_AMOUNT_001',
    'High Amount in 24 Hours',
    'Block if total amount exceeds $10000 in 24 hours',
    'velocity',
    'THRESHOLD',
    JSON_OBJECT(
        'field', 'amount_sum_last_24h',
        'operator', 'greater_than',
        'value', 10000
    ),
    10000.00,
    'BLOCK',
    10,
    TRUE,
    TRUE,
    'user_admin_001'
),

-- Rule 7: Merchant Risk
(
    'RULE_HIGH_RISK_MERCHANT_001',
    'High-Risk Merchant Alert',
    'Challenge transactions with high-risk merchants',
    'merchant',
    'PATTERN',
    JSON_OBJECT(
        'field', 'merchant_category',
        'operator', 'in',
        'value', JSON_ARRAY('GAMBLING', 'CRYPTO', 'ADULT_CONTENT')
    ),
    NULL,
    'CHALLENGE',
    7,
    TRUE,
    FALSE,
    'user_admin_001'
),

-- Rule 8: Rapid Location Change
(
    'RULE_LOCATION_VELOCITY_001',
    'Impossible Travel Detection',
    'Block if location changes more than 500km in 1 hour',
    'location',
    'ANOMALY',
    JSON_OBJECT(
        'field', 'location_distance_last_txn_km',
        'operator', 'greater_than',
        'value', 500,
        'timeframe', '1_hour'
    ),
    500.00,
    'BLOCK',
    10,
    TRUE,
    TRUE,
    'user_admin_001'
);

-- ============================================================================
-- SECTION 4: MONITORED TRANSACTIONS (Samples)
-- ============================================================================

-- First, let's create some customer profile hashes
SET @cust_hash_1 = SHA2('cust_001', 256);
SET @cust_hash_2 = SHA2('cust_002', 256);
SET @cust_hash_3 = SHA2('cust_003', 256);
SET @cust_hash_4 = SHA2('cust_004', 256);
SET @cust_hash_5 = SHA2('cust_005', 256);

-- Sample Transactions
INSERT INTO monitored_transactions (
    external_transaction_id, reference_number,
    customer_id_hash, customer_email_hash, customer_risk_level,
    amount, currency, merchant_name, merchant_category, transaction_type,
    card_last_4, card_type, card_brand,
    device_id, device_type, device_fingerprint,
    ip_address, location_city, location_country,
    location_latitude, location_longitude,
    transactions_last_1h, transactions_last_24h,
    amount_sum_last_1h, amount_sum_last_24h,
    fraud_score, fraud_probability, risk_level, decision, decision_reason,
    model_version, model_confidence, rules_triggered,
    processing_status, analysis_time_ms,
    received_at, analyzed_at
) VALUES
-- Transaction 1: Legitimate - Low Risk
(
    'txn_20260109_000001',
    'REF_20260109_001',
    @cust_hash_1,
    SHA2('john.doe@example.com', 256),
    'LOW',
    129.99,
    'USD',
    'Amazon.com',
    'E-COMMERCE',
    'CARD_PAYMENT',
    '9012',
    'DEBIT',
    'VISA',
    'DEV_JOHN_IPHONE_001',
    'mobile',
    'fp_abc123def456',
    '192.168.1.101',
    'New York',
    'USA',
    40.7128,
    -74.0060,
    1,
    3,
    129.99,
    389.97,
    15,
    0.0850,
    'LOW',
    'ALLOW',
    'Normal transaction pattern, low fraud score',
    'v2.1.0',
    0.9150,
    JSON_ARRAY(),
    'ANALYZED',
    11,
    DATE_SUB(NOW(), INTERVAL 2 HOUR),
    DATE_SUB(NOW(), INTERVAL 2 HOUR)
),

-- Transaction 2: Legitimate but Flagged - Medium Risk
(
    'txn_20260109_000002',
    'REF_20260109_002',
    @cust_hash_2,
    SHA2('jane.smith@example.com', 256),
    'MEDIUM',
    3500.00,
    'USD',
    'Apple Store',
    'ELECTRONICS',
    'CARD_PAYMENT',
    '1234',
    'CREDIT',
    'MASTERCARD',
    'DEV_JANE_LAPTOP_001',
    'desktop',
    'fp_xyz789ghi012',
    '192.168.1.201',
    'Los Angeles',
    'USA',
    34.0522,
    -118.2437,
    1,
    2,
    3500.00,
    3950.00,
    45,
    0.3200,
    'MEDIUM',
    'CHALLENGE',
    'High amount transaction, requires additional verification',
    'v2.1.0',
    0.6800,
    JSON_ARRAY('RULE_HIGH_AMOUNT_001'),
    'FLAGGED',
    13,
    DATE_SUB(NOW(), INTERVAL 5 HOUR),
    DATE_SUB(NOW(), INTERVAL 5 HOUR)
),

-- Transaction 3: Suspicious - High Risk
(
    'txn_20260109_000003',
    'REF_20260109_003',
    @cust_hash_3,
    SHA2('mike.j@example.com', 256),
    'HIGH',
    8500.00,
    'USD',
    'Luxury Jewelers International',
    'JEWELRY',
    'CARD_PAYMENT',
    '0005',
    'CREDIT',
    'AMEX',
    'DEV_UNKNOWN_001',
    'desktop',
    'fp_suspicious_001',
    '45.123.45.67',
    'Miami',
    'USA',
    25.7617,
    -80.1918,
    3,
    6,
    15000.00,
    18500.00,
    78,
    0.7850,
    'HIGH',
    'BLOCK',
    'Multiple red flags: high amount, new device, unusual merchant category, high velocity',
    'v2.1.0',
    0.2150,
    JSON_ARRAY('RULE_HIGH_AMOUNT_001', 'RULE_VELOCITY_1H_001', 'RULE_DEVICE_CHANGE_001'),
    'BLOCKED',
    15,
    DATE_SUB(NOW(), INTERVAL 1 HOUR),
    DATE_SUB(NOW(), INTERVAL 1 HOUR)
),

-- Transaction 4: Likely Fraud - Critical Risk
(
    'txn_20260109_000004',
    'REF_20260109_004',
    @cust_hash_3,
    SHA2('mike.j@example.com', 256),
    'CRITICAL',
    9999.99,
    'USD',
    'Electronics Wholesale USA',
    'ELECTRONICS',
    'CARD_PAYMENT',
    '0005',
    'CREDIT',
    'AMEX',
    'DEV_UNKNOWN_002',
    'mobile',
    'fp_suspicious_002',
    '45.123.45.68',
    'Miami',
    'USA',
    25.7617,
    -80.1918,
    4,
    7,
    24999.99,
    28499.98,
    92,
    0.9250,
    'CRITICAL',
    'BLOCK',
    'Critical fraud indicators: Very high amount, rapid succession, different device, velocity limits exceeded',
    'v2.1.0',
    0.0750,
    JSON_ARRAY('RULE_HIGH_AMOUNT_001', 'RULE_VELOCITY_1H_001', 'RULE_VELOCITY_AMOUNT_001', 'RULE_DEVICE_CHANGE_001'),
    'BLOCKED',
    18,
    DATE_SUB(NOW(), INTERVAL 45 MINUTE),
    DATE_SUB(NOW(), INTERVAL 45 MINUTE)
),

-- Transaction 5: International - Medium Risk
(
    'txn_20260109_000005',
    'REF_20260109_005',
    @cust_hash_2,
    SHA2('jane.smith@example.com', 256),
    'MEDIUM',
    1250.00,
    'USD',
    'Boutique Hotel Paris',
    'TRAVEL',
    'CARD_PAYMENT',
    '1098',
    'DEBIT',
    'VISA',
    'DEV_JANE_MOBILE_002',
    'mobile',
    'fp_xyz789ghi012',
    '195.154.0.1',
    'Paris',
    'FRA',
    48.8566,
    2.3522,
    1,
    1,
    1250.00,
    1250.00,
    52,
    0.4100,
    'MEDIUM',
    'CHALLENGE',
    'International transaction from France, requires 3DS verification',
    'v2.1.0',
    0.5900,
    JSON_ARRAY('RULE_INTL_TXN_001'),
    'ANALYZED',
    14,
    DATE_SUB(NOW(), INTERVAL 3 HOUR),
    DATE_SUB(NOW(), INTERVAL 3 HOUR)
),

-- Transaction 6: Late Night Transaction - Low-Medium Risk
(
    'txn_20260109_000006',
    'REF_20260109_006',
    @cust_hash_5,
    SHA2('robert.b@example.com', 256),
    'LOW',
    85.50,
    'USD',
    'Shell Gas Station',
    'FUEL',
    'CARD_PAYMENT',
    '1117',
    'CREDIT',
    'DISCOVER',
    'DEV_ROB_TABLET_001',
    'tablet',
    'fp_rob_device_001',
    '192.168.1.501',
    'Phoenix',
    'AZ',
    33.4484,
    -112.0740,
    1,
    4,
    85.50,
    285.50,
    28,
    0.1850,
    'LOW',
    'ALLOW',
    'Legitimate pattern, known device, typical merchant',
    'v2.1.0',
    0.8150,
    JSON_ARRAY(),
    'APPROVED',
    10,
    DATE_SUB(NOW(), INTERVAL 30 MINUTE),
    DATE_SUB(NOW(), INTERVAL 30 MINUTE)
),

-- Transaction 7: High Velocity - Under Review
(
    'txn_20260109_000007',
    'REF_20260109_007',
    @cust_hash_4,
    SHA2('sarah.w@example.com', 256),
    'HIGH',
    2500.00,
    'USD',
    'Designer Fashion Outlet',
    'RETAIL',
    'CARD_PAYMENT',
    '5678',
    'CREDIT',
    'VISA',
    'DEV_SARAH_001',
    'mobile',
    'fp_sarah_device_001',
    '192.168.1.401',
    'Houston',
    'TX',
    29.7604,
    -95.3698,
    2,
    5,
    4500.00,
    7000.00,
    65,
    0.6200,
    'HIGH',
    'REVIEW',
    'Customer has 5 transactions in 24h, needs manual review',
    'v2.1.0',
    0.3800,
    JSON_ARRAY('RULE_HIGH_AMOUNT_001'),
    'FLAGGED',
    12,
    DATE_SUB(NOW(), INTERVAL 15 MINUTE),
    DATE_SUB(NOW(), INTERVAL 15 MINUTE)
),

-- Transaction 8: Confirmed Fraud (with ground truth)
(
    'txn_20260108_000099',
    'REF_20260108_099',
    @cust_hash_1,
    SHA2('john.doe@example.com', 256),
    'CRITICAL',
    5000.00,
    'USD',
    'Unknown Merchant',
    'MISC',
    'CARD_PAYMENT',
    '9012',
    'DEBIT',
    'VISA',
    'DEV_UNKNOWN_099',
    'desktop',
    'fp_fraud_device',
    '103.45.67.89',
    'Lagos',
    'NGA',
    6.5244,
    3.3792,
    1,
    1,
    5000.00,
    5000.00,
    95,
    0.9650,
    'CRITICAL',
    'BLOCK',
    'International transaction from Nigeria, unknown merchant, new device',
    'v2.1.0',
    0.0350,
    JSON_ARRAY('RULE_HIGH_AMOUNT_001', 'RULE_INTL_TXN_001', 'RULE_DEVICE_CHANGE_001', 'RULE_LOCATION_VELOCITY_001'),
    'BLOCKED',
    20,
    DATE_SUB(NOW(), INTERVAL 1 DAY),
    DATE_SUB(NOW(), INTERVAL 1 DAY)
);

-- Update the last transaction with ground truth
UPDATE monitored_transactions 
SET is_fraud = TRUE, 
    feedback_source = 'customer_report',
    feedback_at = DATE_SUB(NOW(), INTERVAL 12 HOUR)
WHERE external_transaction_id = 'txn_20260108_000099';

-- ============================================================================
-- SECTION 5: MODEL PREDICTIONS
-- ============================================================================

-- Get model IDs
SET @model_prod_id = (SELECT id FROM ml_models WHERE model_id = 'model_xgb_prod_001');

-- Get transaction IDs
SET @txn_id_1 = (SELECT id FROM monitored_transactions WHERE external_transaction_id = 'txn_20260109_000001');
SET @txn_id_2 = (SELECT id FROM monitored_transactions WHERE external_transaction_id = 'txn_20260109_000002');
SET @txn_id_3 = (SELECT id FROM monitored_transactions WHERE external_transaction_id = 'txn_20260109_000003');
SET @txn_id_4 = (SELECT id FROM monitored_transactions WHERE external_transaction_id = 'txn_20260109_000004');
SET @txn_id_8 = (SELECT id FROM monitored_transactions WHERE external_transaction_id = 'txn_20260108_000099');

INSERT INTO model_predictions (
    transaction_id, model_id,
    prediction, probability, fraud_score, confidence_level,
    features_json, shap_values, top_contributing_features,
    inference_time_ms, actual_label, is_correct
) VALUES
-- Prediction for Transaction 1 (Correct - True Negative)
(
    @txn_id_1, @model_prod_id,
    FALSE, 0.0850, 15, 'HIGH',
    JSON_OBJECT(
        'amount', 129.99, 'merchant_category', 'E-COMMERCE',
        'hour_of_day', 14, 'velocity_1h', 1, 'velocity_24h', 3,
        'customer_risk_score', 25, 'device_known', TRUE
    ),
    JSON_OBJECT(
        'amount', -0.05, 'merchant_category', -0.02, 'velocity_1h', -0.03
    ),
    JSON_ARRAY(
        JSON_OBJECT('feature', 'customer_risk_score', 'impact', -0.15),
        JSON_OBJECT('feature', 'device_known', 'impact', -0.12),
        JSON_OBJECT('feature', 'merchant_category', 'impact', -0.08)
    ),
    11, FALSE, TRUE
),

-- Prediction for Transaction 3 (Correct - True Positive)
(
    @txn_id_3, @model_prod_id,
    TRUE, 0.7850, 78, 'MEDIUM',
    JSON_OBJECT(
        'amount', 8500.00, 'merchant_category', 'JEWELRY',
        'hour_of_day', 16, 'velocity_1h', 3, 'velocity_24h', 6,
        'customer_risk_score', 65, 'device_known', FALSE
    ),
    JSON_OBJECT(
        'amount', 0.35, 'device_known', 0.28, 'velocity_1h', 0.25
    ),
    JSON_ARRAY(
        JSON_OBJECT('feature', 'amount', 'impact', 0.35),
        JSON_OBJECT('feature', 'device_known', 'impact', 0.28),
        JSON_OBJECT('feature', 'velocity_1h', 'impact', 0.25),
        JSON_OBJECT('feature', 'merchant_category', 'impact', 0.18),
        JSON_OBJECT('feature', 'customer_risk_score', 'impact', 0.15)
    ),
    15, NULL, NULL
),

-- Prediction for Transaction 8 (Correct - True Positive with ground truth)
(
    @txn_id_8, @model_prod_id,
    TRUE, 0.9650, 95, 'HIGH',
    JSON_OBJECT(
        'amount', 5000.00, 'merchant_category', 'MISC',
        'hour_of_day', 22, 'velocity_1h', 1, 'velocity_24h', 1,
        'customer_risk_score', 85, 'device_known', FALSE,
        'international', TRUE, 'location_distance_km', 8500
    ),
    JSON_OBJECT(
        'location_distance_km', 0.45, 'device_known', 0.32,
        'international', 0.28, 'amount', 0.25
    ),
    JSON_ARRAY(
        JSON_OBJECT('feature', 'location_distance_km', 'impact', 0.45),
        JSON_OBJECT('feature', 'device_known', 'impact', 0.32),
        JSON_OBJECT('feature', 'international', 'impact', 0.28),
        JSON_OBJECT('feature', 'amount', 'impact', 0.25),
        JSON_OBJECT('feature', 'customer_risk_score', 'impact', 0.20)
    ),
    20, TRUE, TRUE
);

-- ============================================================================
-- SECTION 6: CUSTOMER PROFILES
-- ============================================================================

INSERT INTO customer_profiles (
    customer_id_hash, total_transactions, total_amount,
    avg_transaction_amount, median_amount, max_amount, std_dev_amount,
    common_merchants, common_categories, typical_amounts,
    typical_transaction_hours, typical_days,
    home_city, home_country, home_location,
    known_devices, primary_device_id,
    behavioral_risk_score, trust_score,
    first_transaction_at, last_transaction_at
) VALUES
-- Profile for Customer 1 (John Doe)
(
    @cust_hash_1,
    45,
    12500.00,
    277.78,
    195.00,
    1250.00,
    285.50,
    JSON_ARRAY('Amazon.com', 'Walmart', 'Starbucks', 'Shell'),
    JSON_ARRAY('E-COMMERCE', 'RETAIL', 'FOOD_BEVERAGE', 'FUEL'),
    JSON_ARRAY(15.50, 45.00, 129.99, 250.00),
    JSON_ARRAY(9, 12, 14, 18, 20),
    JSON_ARRAY('Mon', 'Wed', 'Fri', 'Sat'),
    'New York',
    'USA',
    JSON_OBJECT('lat', 40.7128, 'lon', -74.0060),
    JSON_ARRAY(
        JSON_OBJECT('device_id', 'DEV_JOHN_IPHONE_001', 'fingerprint', 'fp_abc123def456', 'first_seen', '2025-01-01')
    ),
    'DEV_JOHN_IPHONE_001',
    25,
    85,
    '2025-01-01 10:00:00',
    DATE_SUB(NOW(), INTERVAL 2 HOUR)
),

-- Profile for Customer 2 (Jane Smith)
(
    @cust_hash_2,
    78,
    45000.00,
    576.92,
    350.00,
    3500.00,
    620.00,
    JSON_ARRAY('Delta Airlines', 'Apple Store', 'Whole Foods', 'Target'),
    JSON_ARRAY('TRAVEL', 'ELECTRONICS', 'RETAIL', 'FOOD'),
    JSON_ARRAY(25.00, 150.00, 450.00, 1200.00),
    JSON_ARRAY(8, 11, 13, 16, 19),
    JSON_ARRAY('Tue', 'Thu', 'Sat', 'Sun'),
    'Los Angeles',
    'USA',
    JSON_OBJECT('lat', 34.0522, 'lon', -118.2437),
    JSON_ARRAY(
        JSON_OBJECT('device_id', 'DEV_JANE_LAPTOP_001', 'fingerprint', 'fp_xyz789ghi012', 'first_seen', '2025-01-05'),
        JSON_OBJECT('device_id', 'DEV_JANE_MOBILE_002', 'fingerprint', 'fp_xyz789ghi012', 'first_seen', '2025-01-10')
    ),
    'DEV_JANE_LAPTOP_001',
    35,
    75,
    '2025-01-05 14:00:00',
    DATE_SUB(NOW(), INTERVAL 3 HOUR)
);

-- ============================================================================
-- SECTION 7: INITIAL DASHBOARD METRICS
-- ============================================================================

-- Calculate metrics for today
CALL sp_calculate_daily_metrics(CURDATE());

-- Calculate metrics for yesterday
CALL sp_calculate_daily_metrics(DATE_SUB(CURDATE(), INTERVAL 1 DAY));

-- ============================================================================
-- SCRIPT COMPLETION
-- ============================================================================

SELECT '========================================' as '';
SELECT 'FRAUD DETECTION SYSTEM DML DATA LOADED' as '';
SELECT '========================================' as '';
SELECT CONCAT('System Users: ', COUNT(*), ' records') as '' FROM system_users;
SELECT CONCAT('ML Models: ', COUNT(*), ' records') as '' FROM ml_models;
SELECT CONCAT('Fraud Rules: ', COUNT(*), ' records') as '' FROM fraud_rules;
SELECT CONCAT('Monitored Transactions: ', COUNT(*), ' records') as '' FROM monitored_transactions;
SELECT CONCAT('Model Predictions: ', COUNT(*), ' records') as '' FROM model_predictions;
SELECT CONCAT('Customer Profiles: ', COUNT(*), ' records') as '' FROM customer_profiles;
SELECT CONCAT('Fraud Alerts: ', COUNT(*), ' records') as '' FROM fraud_alerts;
SELECT CONCAT('Dashboard Metrics: ', COUNT(*), ' records') as '' FROM dashboard_metrics;
SELECT '' as '';
SELECT 'Sample Data Loaded Successfully!' as '';
SELECT 'System is ready for testing.' as '';
SELECT '========================================' as '';