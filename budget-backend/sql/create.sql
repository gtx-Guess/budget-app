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
    refresh_token VARCHAR(1000)
);

-- Add missing columns if they don't exist (for existing databases)
ALTER TABLE `budget-app-user` 
ADD COLUMN IF NOT EXISTS first_name VARCHAR(255) AFTER user_name,
ADD COLUMN IF NOT EXISTS last_name VARCHAR(255) AFTER first_name;

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

-- Add user_id column to accounts table if it doesn't exist (for existing databases)
ALTER TABLE accounts 
ADD COLUMN IF NOT EXISTS user_id INT NOT NULL DEFAULT 1 AFTER plaid_account_id;

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
INSERT INTO `budget-app-user` (id, user_name, first_name, last_name, email_address, password) VALUES 
(1, 'Tigran', 'Tiko', 'User', 'tiko2204@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj0jdXONOP3C')
ON DUPLICATE KEY UPDATE 
    first_name = COALESCE(first_name, 'Tiko'),
    last_name = COALESCE(last_name, 'User');

-- Ensure existing accounts have user_id set
UPDATE accounts SET user_id = 1 WHERE user_id IS NULL OR user_id = 0;