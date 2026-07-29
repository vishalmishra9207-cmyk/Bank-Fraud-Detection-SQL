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

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    reference_number VARCHAR(50) UNIQUE NOT NULL,

    amount DECIMAL(15,2) NOT NULL,
    transaction_type VARCHAR(25) NOT NULL,

    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_status VARCHAR(20) NOT NULL,
    payment_mode VARCHAR(20) NOT NULL,

    transaction_location VARCHAR(100),
    receiver_account VARCHAR(20),

    merchant_id INT,
    device_id INT,

    ip_address VARCHAR(45),
    is_fraud BOOLEAN DEFAULT FALSE,

    remarks VARCHAR(255),

    CONSTRAINT fk_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
);

CREATE TABLE devices (
    device_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    device_identifier VARCHAR(100) UNIQUE NOT NULL,
    device_name VARCHAR(100),

    device_type ENUM('Android','iPhone','Web') NOT NULL,

    device_model VARCHAR(50),

    operating_system VARCHAR(30),
    os_version VARCHAR(20),

    app_version VARCHAR(20),

    device_status VARCHAR(20) DEFAULT 'Active',

    is_trusted BOOLEAN DEFAULT TRUE,

    last_ip_address VARCHAR(45),
    last_login_city VARCHAR(50),

    last_login TIMESTAMP,

    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

CONSTRAINT fk_devices_customer
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id)
);

CREATE TABLE merchants (
    merchant_id INT AUTO_INCREMENT PRIMARY KEY,

    merchant_code VARCHAR(20) UNIQUE NOT NULL,
    merchant_name VARCHAR(100) NOT NULL,

    merchant_category VARCHAR(50),
    merchant_type VARCHAR(30),

    contact_number VARCHAR(15) UNIQUE,
    merchant_email VARCHAR(100) UNIQUE,

    gst_number VARCHAR(20) UNIQUE,

    building_no VARCHAR(20),
    street VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    pincode CHAR(10),
    country VARCHAR(50),

    merchant_status VARCHAR(20) DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE merchant_devices (
    merchant_device_id INT AUTO_INCREMENT PRIMARY KEY,

    merchant_id INT NOT NULL,

    device_serial_number VARCHAR(50) UNIQUE NOT NULL,
    device_model VARCHAR(50),

    merchant_device_type ENUM('POS', 'QR', 'SoundBox', 'mPOS') NOT NULL,
    merchant_device_status VARCHAR(20) DEFAULT 'Active',

    device_issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_service_date DATE,

    CONSTRAINT fk_merchant_devices_merchant
        FOREIGN KEY (merchant_id)
        REFERENCES merchants(merchant_id)
);

CREATE TABLE cards (
    card_id INT AUTO_INCREMENT PRIMARY KEY,

    account_id INT NOT NULL,

    card_number CHAR(16) UNIQUE NOT NULL,
    card_holder_name VARCHAR(100),

    card_type VARCHAR(20),
    card_network ENUM('Visa','RuPay','Mastercard'),

    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE,

    card_status VARCHAR(20) DEFAULT 'Active',

    daily_limit DECIMAL(12,2),

    international_usage BOOLEAN DEFAULT FALSE,
    contactless_enabled BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cards_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
);

CREATE TABLE beneficiaries (
    beneficiary_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    beneficiary_name VARCHAR(100) NOT NULL,
    nickname VARCHAR(50),

    account_number VARCHAR(20) NOT NULL,
    ifsc_code CHAR(11) NOT NULL,

    bank_name VARCHAR(100),
    account_type ENUM('Savings','Current'),

    beneficiary_mobile_number VARCHAR(15),
    beneficiary_email VARCHAR(100),
    upi_id VARCHAR(100),

    beneficiary_status VARCHAR(20) DEFAULT 'Active',
    is_verified BOOLEAN DEFAULT FALSE,

    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_beneficiary_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,

    employee_code VARCHAR(20) UNIQUE NOT NULL,

    branch_id INT NOT NULL,

    employee_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    dob DATE,

    designation VARCHAR(50),
    department VARCHAR(50),

    mobile_number VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE,

    hire_date DATE,
    salary DECIMAL(10,2),

    emp_house_no VARCHAR(20),
    emp_street VARCHAR(100),
    emp_area VARCHAR(100),
    emp_city VARCHAR(50),
    emp_state VARCHAR(100),
    emp_pincode CHAR(6),
    country VARCHAR(100),

    employee_status VARCHAR(20) DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employee_branch
        FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id)
);
