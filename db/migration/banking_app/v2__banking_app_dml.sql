-- ============================================================================
-- BANKING APPLICATION - DML SEED DATA (v2)
-- Version: 1.0
-- Database: MySQL 8.0+
-- Description: Sample data for testing and development
-- ============================================================================

USE banking_app_db;

-- ============================================================================
-- SECTION 1: CUSTOMERS
-- ============================================================================

INSERT INTO customers (
    id, full_name, email, password_hash, phone, date_of_birth,
    address_line1, city, state, country, postal_code,
    account_number, account_type, account_status, balance,
    pin_hash, two_factor_enabled, kyc_verified, kyc_verified_at,
    id_proof_type, id_proof_number
) VALUES
-- Customer 1: John Doe (Active, Verified)
(
    'cust_001',
    'John Doe',
    'john.doe@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm', -- password: SecurePass123!
    '+1-555-0101',
    '1990-05-15',
    '123 Main Street',
    'New York',
    'NY',
    'USA',
    '10001',
    'ACC1000000001',
    'SAVINGS',
    'ACTIVE',
    25000.00,
    '$2b$12$abc123...',
    TRUE,
    TRUE,
    '2025-01-01 10:00:00',
    'PASSPORT',
    'P12345678'
),

-- Customer 2: Jane Smith (Active, Verified)
(
    'cust_002',
    'Jane Smith',
    'jane.smith@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm',
    '+1-555-0102',
    '1988-08-20',
    '456 Oak Avenue',
    'Los Angeles',
    'CA',
    'USA',
    '90001',
    'ACC1000000002',
    'CURRENT',
    'ACTIVE',
    50000.00,
    '$2b$12$def456...',
    TRUE,
    TRUE,
    '2025-01-05 14:30:00',
    'DRIVERS_LICENSE',
    'DL987654321'
),

-- Customer 3: Mike Johnson (Active, Not Verified)
(
    'cust_003',
    'Mike Johnson',
    'mike.j@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm',
    '+1-555-0103',
    '1995-03-10',
    '789 Pine Street',
    'Chicago',
    'IL',
    'USA',
    '60601',
    'ACC1000000003',
    'SAVINGS',
    'ACTIVE',
    10000.00,
    '$2b$12$ghi789...',
    FALSE,
    FALSE,
    NULL,
    NULL,
    NULL
),

-- Customer 4: Sarah Williams (Suspended)
(
    'cust_004',
    'Sarah Williams',
    'sarah.w@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm',
    '+1-555-0104',
    '1992-11-25',
    '321 Elm Road',
    'Houston',
    'TX',
    'USA',
    '77001',
    'ACC1000000004',
    'SAVINGS',
    'SUSPENDED',
    5000.00,
    '$2b$12$jkl012...',
    TRUE,
    TRUE,
    '2025-01-03 09:00:00',
    'PASSPORT',
    'P98765432'
),

-- Customer 5: Robert Brown (Active, Verified)
(
    'cust_005',
    'Robert Brown',
    'robert.b@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7BlXFy.Rtm',
    '+1-555-0105',
    '1985-07-14',
    '654 Maple Drive',
    'Phoenix',
    'AZ',
    'USA',
    '85001',
    'ACC1000000005',
    'SALARY',
    'ACTIVE',
    75000.00,
    '$2b$12$mno345...',
    TRUE,
    TRUE,
    '2024-12-15 11:20:00',
    'DRIVERS_LICENSE',
    'DL123456789'
);

-- ============================================================================
-- SECTION 2: CARDS
-- ============================================================================

INSERT INTO cards (
    customer_id, card_number_hash, card_token, last_4_digits,
    card_type, card_brand, expiry_month, expiry_year, cardholder_name,
    issuer_bank, issuer_country, bin_number,
    card_status, daily_limit, transaction_limit,
    cvv_hash, is_verified, verification_method
) VALUES
-- Cards for Customer 1 (John Doe)
(
    'cust_001',
    SHA2('4532123456789012', 256),
    'tok_visa_001_' || UUID(),
    '9012',
    'DEBIT',
    'VISA',
    12,
    2027,
    'JOHN DOE',
    'Chase Bank',
    'USA',
    '453212',
    'ACTIVE',
    50000.00,
    10000.00,
    SHA2('123', 256),
    TRUE,
    '3DS'
),

-- Cards for Customer 2 (Jane Smith)
(
    'cust_002',
    SHA2('5412345678901234', 256),
    'tok_mc_002_' || UUID(),
    '1234',
    'CREDIT',
    'MASTERCARD',
    6,
    2028,
    'JANE SMITH',
    'Bank of America',
    'USA',
    '541234',
    'ACTIVE',
    100000.00,
    25000.00,
    SHA2('456', 256),
    TRUE,
    '3DS'
),
(
    'cust_002',
    SHA2('4532987654321098', 256),
    'tok_visa_002b_' || UUID(),
    '1098',
    'DEBIT',
    'VISA',
    3,
    2027,
    'JANE SMITH',
    'Citibank',
    'USA',
    '453298',
    'ACTIVE',
    50000.00,
    15000.00,
    SHA2('789', 256),
    TRUE,
    'OTP'
),

-- Cards for Customer 3 (Mike Johnson)
(
    'cust_003',
    SHA2('378282246310005', 256),
    'tok_amex_003_' || UUID(),
    '0005',
    'CREDIT',
    'AMEX',
    9,
    2026,
    'MIKE JOHNSON',
    'American Express',
    'USA',
    '378282',
    'ACTIVE',
    75000.00,
    20000.00,
    SHA2('1234', 256),
    FALSE,
    NULL
),

-- Cards for Customer 5 (Robert Brown)
(
    'cust_005',
    SHA2('6011111111111117', 256),
    'tok_disc_005_' || UUID(),
    '1117',
    'CREDIT',
    'DISCOVER',
    11,
    2028,
    'ROBERT BROWN',
    'Wells Fargo',
    'USA',
    '601111',
    'ACTIVE',
    80000.00,
    20000.00,
    SHA2('567', 256),
    TRUE,
    '3DS'
);

-- ============================================================================
-- SECTION 3: MERCHANTS
-- ============================================================================

INSERT INTO merchants (
    merchant_id, business_name, legal_name, contact_email, contact_phone,
    category, mcc_code, business_type,
    country, city, address, merchant_status, is_verified
) VALUES
-- Merchant 1: Amazon
(
    'MERCH_AMZ_001',
    'Amazon.com',
    'Amazon.com Inc.',
    'merchant@amazon.com',
    '+1-800-280-4331',
    'E-COMMERCE',
    '5999',
    'ONLINE_RETAIL',
    'USA',
    'Seattle',
    '410 Terry Avenue North, Seattle, WA 98109',
    'ACTIVE',
    TRUE
),

-- Merchant 2: Walmart
(
    'MERCH_WMT_002',
    'Walmart',
    'Walmart Inc.',
    'merchant@walmart.com',
    '+1-800-925-6278',
    'RETAIL',
    '5411',
    'SUPERMARKET',
    'USA',
    'Bentonville',
    '702 SW 8th Street, Bentonville, AR 72716',
    'ACTIVE',
    TRUE
),

-- Merchant 3: Starbucks
(
    'MERCH_SBX_003',
    'Starbucks',
    'Starbucks Corporation',
    'merchant@starbucks.com',
    '+1-800-782-7282',
    'FOOD_BEVERAGE',
    '5814',
    'RESTAURANT',
    'USA',
    'Seattle',
    '2401 Utah Avenue South, Seattle, WA 98134',
    'ACTIVE',
    TRUE
),

-- Merchant 4: Delta Airlines
(
    'MERCH_DAL_004',
    'Delta Air Lines',
    'Delta Air Lines Inc.',
    'merchant@delta.com',
    '+1-800-221-1212',
    'TRAVEL',
    '4511',
    'AIRLINE',
    'USA',
    'Atlanta',
    'Hartsfield-Jackson International Airport, Atlanta, GA 30320',
    'ACTIVE',
    TRUE
),

-- Merchant 5: Apple Store
(
    'MERCH_APL_005',
    'Apple Store',
    'Apple Inc.',
    'merchant@apple.com',
    '+1-800-692-7753',
    'ELECTRONICS',
    '5732',
    'ELECTRONICS_STORE',
    'USA',
    'Cupertino',
    'One Apple Park Way, Cupertino, CA 95014',
    'ACTIVE',
    TRUE
),

-- Merchant 6: Shell Gas Station
(
    'MERCH_SHL_006',
    'Shell',
    'Shell Oil Company',
    'merchant@shell.com',
    '+1-800-331-3703',
    'FUEL',
    '5541',
    'SERVICE_STATION',
    'USA',
    'Houston',
    '910 Louisiana Street, Houston, TX 77002',
    'ACTIVE',
    TRUE
),

-- Merchant 7: Netflix
(
    'MERCH_NFX_007',
    'Netflix',
    'Netflix Inc.',
    'merchant@netflix.com',
    '+1-866-579-7172',
    'ENTERTAINMENT',
    '5968',
    'SUBSCRIPTION_SERVICE',
    'USA',
    'Los Gatos',
    '100 Winchester Circle, Los Gatos, CA 95032',
    'ACTIVE',
    TRUE
),

-- Merchant 8: Target
(
    'MERCH_TGT_008',
    'Target',
    'Target Corporation',
    'merchant@target.com',
    '+1-800-440-0680',
    'RETAIL',
    '5310',
    'DEPARTMENT_STORE',
    'USA',
    'Minneapolis',
    '1000 Nicollet Mall, Minneapolis, MN 55403',
    'ACTIVE',
    TRUE
);

-- ============================================================================
-- SECTION 4: TRANSACTIONS (Sample)
-- ============================================================================

-- Note: Transaction IDs will be auto-generated
-- These are sample transactions for testing

INSERT INTO transactions (
    customer_id, card_id, merchant_id,
    transaction_type, amount, currency,
    merchant_name, merchant_category,
    transaction_status, reference_number,
    initiated_at, processed_at, completed_at
) VALUES
-- Transaction 1: John Doe - Amazon purchase (Success)
(
    'cust_001',
    1,
    1,
    'CARD_PAYMENT',
    129.99,
    'USD',
    'Amazon.com',
    'E-COMMERCE',
    'SUCCESS',
    CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_001'),
    DATE_SUB(NOW(), INTERVAL 2 HOUR),
    DATE_SUB(NOW(), INTERVAL 2 HOUR),
    DATE_SUB(NOW(), INTERVAL 2 HOUR)
),

-- Transaction 2: Jane Smith - Starbucks (Success)
(
    'cust_002',
    2,
    3,
    'CARD_PAYMENT',
    15.50,
    'USD',
    'Starbucks',
    'FOOD_BEVERAGE',
    'SUCCESS',
    CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_002'),
    DATE_SUB(NOW(), INTERVAL 5 HOUR),
    DATE_SUB(NOW(), INTERVAL 5 HOUR),
    DATE_SUB(NOW(), INTERVAL 5 HOUR)
),

-- Transaction 3: Mike Johnson - Apple Store (Pending)
(
    'cust_003',
    4,
    5,
    'CARD_PAYMENT',
    999.00,
    'USD',
    'Apple Store',
    'ELECTRONICS',
    'PENDING',
    CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_003'),
    DATE_SUB(NOW(), INTERVAL 30 MINUTE),
    NULL,
    NULL
),

-- Transaction 4: Jane Smith - Delta Airlines (Success)
(
    'cust_002',
    3,
    4,
    'CARD_PAYMENT',
    450.00,
    'USD',
    'Delta Air Lines',
    'TRAVEL',
    'SUCCESS',
    CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_004'),
    DATE_SUB(NOW(), INTERVAL 1 DAY),
    DATE_SUB(NOW(), INTERVAL 1 DAY),
    DATE_SUB(NOW(), INTERVAL 1 DAY)
),

-- Transaction 5: Robert Brown - Shell Gas Station (Success)
(
    'cust_005',
    5,
    6,
    'CARD_PAYMENT',
    65.00,
    'USD',
    'Shell',
    'FUEL',
    'SUCCESS',
    CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_005'),
    DATE_SUB(NOW(), INTERVAL 3 HOUR),
    DATE_SUB(NOW(), INTERVAL 3 HOUR),
    DATE_SUB(NOW(), INTERVAL 3 HOUR)
);

-- ============================================================================
-- SECTION 5: TRANSACTION METADATA
-- ============================================================================

-- Get the transaction IDs we just created
SET @txn1 = (SELECT id FROM transactions WHERE reference_number = CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_001') LIMIT 1);
SET @txn2 = (SELECT id FROM transactions WHERE reference_number = CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_002') LIMIT 1);
SET @txn3 = (SELECT id FROM transactions WHERE reference_number = CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_003') LIMIT 1);
SET @txn4 = (SELECT id FROM transactions WHERE reference_number = CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_004') LIMIT 1);
SET @txn5 = (SELECT id FROM transactions WHERE reference_number = CONCAT('REF_', DATE_FORMAT(NOW(), '%Y%m%d'), '_005') LIMIT 1);

INSERT INTO transaction_metadata (
    transaction_id, device_id, device_type, device_os, device_browser,
    user_agent, ip_address, location_city, location_state, location_country,
    location_latitude, location_longitude,
    connection_type, vpn_detected, proxy_detected, session_id
) VALUES
-- Metadata for Transaction 1
(
    @txn1,
    'DEV_JOHN_IPHONE_001',
    'mobile',
    'iOS 17',
    'Safari',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)',
    '192.168.1.101',
    'New York',
    'NY',
    'USA',
    40.7128,
    -74.0060,
    '4g',
    FALSE,
    FALSE,
    'sess_john_001'
),

-- Metadata for Transaction 2
(
    @txn2,
    'DEV_JANE_LAPTOP_001',
    'desktop',
    'Windows 11',
    'Chrome',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
    '192.168.1.201',
    'Los Angeles',
    'CA',
    'USA',
    34.0522,
    -118.2437,
    'wifi',
    FALSE,
    FALSE,
    'sess_jane_001'
),

-- Metadata for Transaction 3
(
    @txn3,
    'DEV_MIKE_ANDROID_001',
    'mobile',
    'Android 14',
    'Chrome',
    'Mozilla/5.0 (Linux; Android 14) Chrome/120.0.0.0',
    '192.168.1.301',
    'Chicago',
    'IL',
    'USA',
    41.8781,
    -87.6298,
    '5g',
    FALSE,
    FALSE,
    'sess_mike_001'
),

-- Metadata for Transaction 4
(
    @txn4,
    'DEV_JANE_MOBILE_002',
    'mobile',
    'iOS 17',
    'Safari',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)',
    '192.168.1.202',
    'Los Angeles',
    'CA',
    'USA',
    34.0522,
    -118.2437,
    'wifi',
    FALSE,
    FALSE,
    'sess_jane_002'
),

-- Metadata for Transaction 5
(
    @txn5,
    'DEV_ROB_TABLET_001',
    'tablet',
    'Android 14',
    'Chrome',
    'Mozilla/5.0 (Linux; Android 14) Chrome/120.0.0.0',
    '192.168.1.501',
    'Phoenix',
    'AZ',
    'USA',
    33.4484,
    -112.0740,
    'wifi',
    FALSE,
    FALSE,
    'sess_rob_001'
);

-- ============================================================================
-- SCRIPT COMPLETION
-- ============================================================================

SELECT '========================================' as '';
SELECT 'BANKING APP DML DATA LOADED' as '';
SELECT '========================================' as '';
SELECT CONCAT('Customers: ', COUNT(*), ' records') as '' FROM customers;
SELECT CONCAT('Cards: ', COUNT(*), ' records') as '' FROM cards;
SELECT CONCAT('Merchants: ', COUNT(*), ' records') as '' FROM merchants;
SELECT CONCAT('Transactions: ', COUNT(*), ' records') as '' FROM transactions;
SELECT CONCAT('Transaction Metadata: ', COUNT(*), ' records') as '' FROM transaction_metadata;
SELECT '' as '';
SELECT 'Sample Data Loaded Successfully!' as '';
SELECT '========================================' as '';