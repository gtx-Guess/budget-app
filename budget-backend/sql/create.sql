CREATE DATABASE `local_dev_stuff`

USE `local_dev_stuff`

CREATE TABLE `budget-app-user` (
	id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(500),
    email_address VARCHAR(500),
    `password` VARCHAR(500),
    pld_public_token VARCHAR(500),
    refresh_token VARCHAR(1000)
);