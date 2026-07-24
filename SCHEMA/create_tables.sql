CREATE DATABASE IF NOT EXISTS bank_fraud_db;

USE bank_fraud_db;

create table customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY , 
    customer_name VARCHAR(100) NOT NULL , 
    mobile_number VARCHAR(10) NOT NULL UNIQUE , 
    email varchar (100) UNIQUE, 
    dob date  , 
    gender varchar (10) , 
    occupation varchar (100) , 
    house_no varchar(20) , 
    street varchar(100) , 
    area varchar (100) , 
    city varchar (50) , 
    state varchar (100) , 
    pincode varchar(6) , 
    country varchar (100) ,
    pan_number char (10) UNIQUE, 
    kyc_status varchar (10) , 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

) ;


CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_type VARCHAR(20) NOT NULL,
    branch_code CHAR(20) NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0.00,
    account_status VARCHAR(25) DEFAULT 'Active',
    open_date DATE NOT NULL,
    closed_date DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);
