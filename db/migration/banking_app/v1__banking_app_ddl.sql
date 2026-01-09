-- ============================================================================
-- BANKING APPLICATION - DDL SCHEMA (v1)
-- Version: 1.0
-- Database: MySQL 8.0+
-- Description: Simplified banking app schema for secure payment processing
-- Purpose: Store user, card, and transaction data for banking operations
-- ============================================================================

-- ============================================================================
-- SECTION 1: DATABASE CREATION
-- ============================================================================

CREATE DATABASE IF NOT EXISTS banking_app_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE banking_app_db;

-- ============================================================================
-- SECTION 2: USER MANAGEMENT
-- ============================================================================

-- Create application user with limited privileges
-- Note: Run these commands as root user
CREATE USER IF NOT EXISTS 'banking_app_user'@'%' IDENTIFIED BY 'BankApp2026#Secure!';
GRANT SELECT, INSERT, UPDATE ON banking_app_db.* TO 'banking_app_user'@'%';
FLUSH PRIVILEGES;

-- ============================================================================
-- SECTION 3: TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Table: customers
-- Description: Core customer accounts for banking application
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    id VARCHAR(50) PRIMARY KEY DEFAULT (CONCAT('cust_', UUID())),
    
    -- Basic Information
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    
    -- Address Information
    address_line1 VARCHAR(200),
    address_line2 VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(3) NOT NULL DEFAULT 'USA',
    postal_code VARCHAR(20),
    
    -- Account Information
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_type ENUM('SAVINGS', 'CURRENT', 'SALARY') NOT NULL DEFAULT 'SAVINGS',
    account_status ENUM('ACTIVE', 'SUSPENDED', 'CLOSED') NOT NULL DEFAULT 'ACTIVE',
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00 CHECK (balance >= 0),
    
    -- Security
    pin_hash VARCHAR(255),
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    security_question VARCHAR(200),
    security_answer_hash VARCHAR(255),
    
    -- KYC Information
    kyc_verified BOOLEAN DEFAULT FALSE,
    kyc_verified_at TIMESTAMP NULL,
    id_proof_type VARCHAR(50),
    id_proof_number VARCHAR(50),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL,
    
    -- Soft Delete
    deleted_at TIMESTAMP NULL,
    
    INDEX idx_email (email),
    INDEX idx_account_number (account_number),
    INDEX idx_account_status (account_status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: cards
-- Description: Payment cards linked to customer accounts
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cards (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    
    -- Card Information (PCI-DSS Compliant)
    card_number_hash VARCHAR(255) UNIQUE NOT NULL COMMENT 'SHA-256 hash of card number',
    card_token VARCHAR(100) UNIQUE NOT NULL COMMENT 'Tokenized card for processing',
    last_4_digits CHAR(4) NOT NULL,
    card_type ENUM('DEBIT', 'CREDIT', 'PREPAID') NOT NULL,
    card_brand VARCHAR(20) NOT NULL COMMENT 'VISA, MASTERCARD, AMEX, RUPAY',
    
    -- Card Details
    expiry_month TINYINT NOT NULL CHECK (expiry_month BETWEEN 1 AND 12),
    expiry_year SMALLINT NOT NULL,
    cardholder_name VARCHAR(100) NOT NULL,
    
    -- Issuer Information
    issuer_bank VARCHAR(100),
    issuer_country VARCHAR(3) DEFAULT 'USA',
    bin_number VARCHAR(6) COMMENT 'First 6 digits - Bank Identification Number',
    
    -- Card Status
    card_status ENUM('ACTIVE', 'BLOCKED', 'EXPIRED', 'LOST', 'STOLEN') NOT NULL DEFAULT 'ACTIVE',
    
    -- Limits
    daily_limit DECIMAL(12, 2) DEFAULT 50000.00,
    transaction_limit DECIMAL(12, 2) DEFAULT 10000.00,
    
    -- Security
    cvv_hash VARCHAR(255) COMMENT 'Hashed CVV (if stored)',
    is_verified BOOLEAN DEFAULT FALSE,
    verification_method VARCHAR(50) COMMENT '3DS, OTP, AVS',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP NULL,
    blocked_at TIMESTAMP NULL,
    
    -- Soft Delete
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_customer_id (customer_id),
    INDEX idx_card_status (card_status),
    INDEX idx_card_token (card_token),
    INDEX idx_last_4 (last_4_digits)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: merchants
-- Description: Registered merchants for payment processing
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS merchants (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    merchant_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Merchant Information
    business_name VARCHAR(200) NOT NULL,
    legal_name VARCHAR(200),
    contact_email VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(20),
    
    -- Business Details
    category VARCHAR(100) COMMENT 'Electronics, Fashion, Travel, Food, etc.',
    mcc_code VARCHAR(4) COMMENT 'Merchant Category Code',
    business_type VARCHAR(50),
    
    -- Location
    country VARCHAR(3) NOT NULL,
    city VARCHAR(100),
    address TEXT,
    
    -- Status
    merchant_status ENUM('ACTIVE', 'SUSPENDED', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    is_verified BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_business_name (business_name),
    INDEX idx_category (category),
    INDEX idx_merchant_status (merchant_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: transactions
-- Description: All payment transactions processed through banking app
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    id VARCHAR(50) PRIMARY KEY DEFAULT (CONCAT('txn_', DATE_FORMAT(NOW(), '%Y%m%d'), '_', LPAD(UUID_SHORT() % 1000000, 6, '0'))),
    
    -- Transaction Parties
    customer_id VARCHAR(50) NOT NULL,
    card_id BIGINT NULL COMMENT 'NULL for account-to-account transfers',
    merchant_id BIGINT NULL COMMENT 'NULL for P2P transfers',
    
    -- Beneficiary Information (for P2P or account transfers)
    beneficiary_account_number VARCHAR(20),
    beneficiary_name VARCHAR(100),
    beneficiary_ifsc VARCHAR(11) COMMENT 'For Indian banks',
    
    -- Transaction Details
    transaction_type ENUM('CARD_PAYMENT', 'ACCOUNT_TRANSFER', 'UPI', 'WALLET') NOT NULL,
    amount DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    
    -- Merchant Information (if applicable)
    merchant_name VARCHAR(200),
    merchant_category VARCHAR(50),
    
    -- Transaction Status
    transaction_status ENUM(
        'INITIATED',
        'PENDING',
        'PROCESSING',
        'SUCCESS',
        'FAILED',
        'DECLINED',
        'CANCELLED'
    ) NOT NULL DEFAULT 'INITIATED',
    
    -- Transaction Context
    description TEXT,
    reference_number VARCHAR(50) UNIQUE,
    
    -- Timestamps
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (card_id) REFERENCES cards(id),
    FOREIGN KEY (merchant_id) REFERENCES merchants(id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_card_id (card_id),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_transaction_status (transaction_status),
    INDEX idx_initiated_at (initiated_at),
    INDEX idx_reference_number (reference_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: transaction_metadata
-- Description: Additional context for transaction processing
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transaction_metadata (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL UNIQUE,
    
    -- Device Information
    device_id VARCHAR(100),
    device_type VARCHAR(50) COMMENT 'mobile, desktop, tablet, pos',
    device_os VARCHAR(50),
    device_browser VARCHAR(50),
    user_agent TEXT,
    
    -- Location Information
    ip_address VARCHAR(45) NOT NULL,
    location_city VARCHAR(100),
    location_state VARCHAR(100),
    location_country VARCHAR(3),
    location_latitude DECIMAL(10, 8),
    location_longitude DECIMAL(11, 8),
    
    -- Network Information
    connection_type VARCHAR(50) COMMENT 'wifi, 4g, 5g, ethernet',
    vpn_detected BOOLEAN DEFAULT FALSE,
    proxy_detected BOOLEAN DEFAULT FALSE,
    
    -- Session Information
    session_id VARCHAR(100),
    session_duration_seconds INT,
    
    -- Additional Data (JSON format for flexibility)
    additional_info JSON COMMENT 'Store any extra contextual data',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_ip_address (ip_address),
    INDEX idx_device_id (device_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: audit_logs
-- Description: Audit trail for compliance and security
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    -- Actor Information
    customer_id VARCHAR(50),
    customer_email VARCHAR(100),
    
    -- Action Details
    action VARCHAR(100) NOT NULL COMMENT 'login, payment, card_block, profile_update',
    action_type ENUM('CREATE', 'READ', 'UPDATE', 'DELETE') NOT NULL,
    entity_type VARCHAR(50) COMMENT 'customer, card, transaction',
    entity_id VARCHAR(50),
    
    -- Request Information
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Status
    status VARCHAR(20) COMMENT 'success, failed, error',
    error_message TEXT,
    
    -- Additional Data
    metadata JSON,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_customer_id (customer_id),
    INDEX idx_action (action),
    INDEX idx_entity_type (entity_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table: sessions
-- Description: Active customer sessions
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(100) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    
    -- Session Details
    session_token VARCHAR(500) UNIQUE NOT NULL,
    refresh_token VARCHAR(500),
    
    -- Session Context
    ip_address VARCHAR(45),
    user_agent TEXT,
    device_id VARCHAR(100),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    terminated_at TIMESTAMP NULL,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_customer_id (customer_id),
    INDEX idx_session_token (session_token),
    INDEX idx_is_active (is_active),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 4: VIEWS
-- ============================================================================

-- View: Customer account summary
CREATE OR REPLACE VIEW v_customer_accounts AS
SELECT 
    c.id,
    c.full_name,
    c.email,
    c.phone,
    c.account_number,
    c.account_type,
    c.account_status,
    c.balance,
    c.kyc_verified,
    COUNT(DISTINCT cd.id) as total_cards,
    SUM(CASE WHEN cd.card_status = 'ACTIVE' THEN 1 ELSE 0 END) as active_cards,
    c.created_at,
    c.last_login_at
FROM customers c
LEFT JOIN cards cd ON c.id = cd.customer_id AND cd.deleted_at IS NULL
WHERE c.deleted_at IS NULL
GROUP BY c.id;

-- View: Recent transactions
CREATE OR REPLACE VIEW v_recent_transactions AS
SELECT 
    t.id,
    t.customer_id,
    c.full_name as customer_name,
    c.email as customer_email,
    t.transaction_type,
    t.amount,
    t.currency,
    t.merchant_name,
    t.merchant_category,
    t.transaction_status,
    t.reference_number,
    t.initiated_at,
    t.completed_at,
    tm.ip_address,
    tm.location_city,
    tm.location_country
FROM transactions t
JOIN customers c ON t.customer_id = c.id
LEFT JOIN transaction_metadata tm ON t.id = tm.transaction_id
WHERE t.initiated_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY t.initiated_at DESC;

-- ============================================================================
-- SECTION 5: TRIGGERS
-- ============================================================================

-- Trigger: Update account balance after successful transaction
DELIMITER //
CREATE TRIGGER trg_update_balance_after_transaction
AFTER UPDATE ON transactions
FOR EACH ROW
BEGIN
    IF NEW.transaction_status = 'SUCCESS' AND OLD.transaction_status != 'SUCCESS' THEN
        -- Deduct amount from customer's account
        UPDATE customers 
        SET balance = balance - NEW.amount,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.customer_id;
    END IF;
END//
DELIMITER ;

-- Trigger: Log audit trail on customer updates
DELIMITER //
CREATE TRIGGER trg_audit_customer_updates
AFTER UPDATE ON customers
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (
        customer_id,
        customer_email,
        action,
        action_type,
        entity_type,
        entity_id,
        status,
        metadata
    ) VALUES (
        NEW.id,
        NEW.email,
        'customer_update',
        'UPDATE',
        'customer',
        NEW.id,
        'success',
        JSON_OBJECT(
            'old_status', OLD.account_status,
            'new_status', NEW.account_status
        )
    );
END//
DELIMITER ;

-- ============================================================================
-- SCRIPT COMPLETION
-- ============================================================================

SELECT '========================================' as '';
SELECT 'BANKING APP DDL SCHEMA CREATED' as '';
SELECT '========================================' as '';
SELECT 'Database: banking_app_db' as '';
SELECT 'Tables Created: 8' as '';
SELECT 'Views Created: 2' as '';
SELECT 'Triggers Created: 2' as '';
SELECT '' as '';
SELECT 'Next Step: Run banking_app_v2_dml.sql' as '';
SELECT '========================================' as '';