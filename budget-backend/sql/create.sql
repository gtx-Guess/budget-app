-- User Accounts Table
CREATE TABLE `budget-app-user` (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(500),
    email_address VARCHAR(500),
    `password` VARCHAR(500),
    pld_public_token VARCHAR(500),
    refresh_token VARCHAR(1000)
);
-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airtable_id VARCHAR(255) UNIQUE NOT NULL,
    institution VARCHAR(255),
    usd DECIMAL(10, 2),
    last_successful_update DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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