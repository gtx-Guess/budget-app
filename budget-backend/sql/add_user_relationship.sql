-- Add user relationship to accounts table
-- Run this SQL to add user_id column and establish the relationship

-- Step 1: Add user_id column to accounts table
ALTER TABLE accounts 
ADD COLUMN user_id INT;

-- Step 2: Add foreign key constraint
ALTER TABLE accounts
ADD CONSTRAINT fk_accounts_user 
FOREIGN KEY (user_id) REFERENCES `budget-app-user`(id);

-- Step 3: Update existing accounts to belong to test user (assuming user ID 1)
UPDATE accounts SET user_id = 1 WHERE user_id IS NULL;

-- Step 4: Make user_id required for future accounts
ALTER TABLE accounts MODIFY user_id INT NOT NULL;

-- Verify the changes
DESCRIBE accounts;
SELECT * FROM accounts;