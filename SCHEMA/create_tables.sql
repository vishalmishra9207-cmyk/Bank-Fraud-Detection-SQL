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

CREATE TABLE branches (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_code CHAR(20) UNIQUE NOT NULL,
    branch_manager_id INT NOT NULL UNIQUE,

    building_no VARCHAR(20),
    street VARCHAR(50),
    area VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    pincode CHAR(10) NOT NULL,

    ifsc_code CHAR(11) UNIQUE NOT NULL,
    contact_number VARCHAR(15),
    branch_email VARCHAR(100),

    branch_status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE branches
ADD COLUMN ifsc_code_branch CHAR(11) UNIQUE NOT NULL;

ALTER TABLE branches
ADD COLUMN contact_number_branch VARCHAR(15);

ALTER TABLE branches
ADD COLUMN branch_email VARCHAR(100) UNIQUE;

ALTER TABLE branches
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

select * from branches ;

alter table branches drop column contact_number_branch ;
alter table branches drop column ifsc_code_branch ;


ALTER TABLE accounts
DROP COLUMN branch_code;

ALTER TABLE accounts
ADD COLUMN branch_id INT NOT NULL;

ALTER TABLE accounts
ADD CONSTRAINT fk_branch
FOREIGN KEY (branch_id)
REFERENCES branches(branch_id);

