-- User Accounts Table
CREATE TABLE IF NOT EXISTS `budget-app-user` (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(500),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email_address VARCHAR(500),
    `password` VARCHAR(500),
    pld_public_token VARCHAR(500),
    refresh_token VARCHAR(1000),
    is_admin TINYINT(1) NOT NULL DEFAULT 0
);

-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airtable_id VARCHAR(255) UNIQUE NOT NULL,
    institution VARCHAR(255),
    usd DECIMAL(10, 2),
    last_successful_update DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    plaid_account_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INT NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES `budget-app-user`(id)
);

-- Transactions table  
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airtable_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(500),
    usd DECIMAL(10, 2),
    date DATE,
    vendor VARCHAR(255),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    account_id VARCHAR(255) NOT NULL
);

-- Sync log table
CREATE TABLE IF NOT EXISTS sync_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sync_type VARCHAR(50) NOT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    records_synced INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'running',
    error_message TEXT
);

-- Insert initial Tiko user (password: hashed version of your actual password)
INSERT INTO `budget-app-user` (id, user_name, first_name, last_name, email_address, password, is_admin) VALUES
(1, 'Tigran', 'Tiko', 'User', 'tiko2204@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj0jdXONOP3C', 1)
ON DUPLICATE KEY UPDATE
    first_name = COALESCE(first_name, 'Tiko'),
    last_name = COALESCE(last_name, 'User'),
    is_admin = 1;

-- Ensure existing accounts have user_id set
UPDATE accounts SET user_id = 1 WHERE user_id IS NULL OR user_id = 0;