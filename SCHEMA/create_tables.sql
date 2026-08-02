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

CREATE TABLE fraud_alerts (

    fraud_alert_id INT AUTO_INCREMENT PRIMARY KEY,

    transaction_id INT NOT NULL,
    account_id INT NOT NULL,
    customer_id INT NOT NULL,

    alert_type ENUM(
        'High Amount',
        'New Device',
        'Different Location',
        'Multiple Failed Login',
        'Suspicious Merchant',
        'Multiple Transactions'
    ) NOT NULL,

    risk_score TINYINT UNSIGNED NOT NULL,

    alert_status ENUM(
        'Pending',
        'Under Review',
        'Resolved',
        'False Positive'
    ) DEFAULT 'Pending',

    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detected_location VARCHAR(255),

    resolved_at TIMESTAMP NULL DEFAULT NULL,

    reviewed_by INT DEFAULT NULL,

    action_taken VARCHAR(100),

    remarks VARCHAR(255),

    CONSTRAINT fk_fraud_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id),

    CONSTRAINT fk_fraud_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id),

    CONSTRAINT fk_fraud_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_fraud_employee
        FOREIGN KEY (reviewed_by)
        REFERENCES employees(employee_id)
);

create table audit_logs(
audit_id INT  primary KEY AUTO_INCREMENT , 
employee_id int NOT NULL, 
table_name varchar(50),
record_id int NOT NULL,
action_type varchar(20) ,
old_value varchar(50),
new_value varchar(50), 
action_time varchar(50),
ip_address varchar(45),
remarks varchar(200)
CONSTRAINT fk_employee_id FOREIGN key (employee_id) REFERENCES employees(employee_id),
);

CREATE TABLE login_history (

    login_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,
    device_id INT,

    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP NULL DEFAULT NULL,

    login_status ENUM(
        'Success',
        'Failed',
        'Blocked'
    ),

    login_method ENUM(
        'Password',
        'OTP',
        'Fingerprint',
        'Face ID'
    ),

    ip_address VARCHAR(45),
    location VARCHAR(100),

    failed_attempts TINYINT DEFAULT 0,

    session_id VARCHAR(100),

    CONSTRAINT fk_login_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_login_device
        FOREIGN KEY (device_id)
        REFERENCES devices(device_id)
);

CREATE TABLE kyc_documents (

    kyc_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    document_type ENUM(
        'Aadhaar',
        'PAN',
        'Passport',
        'Driving License',
        'Voter ID'
    ),

    document_number VARCHAR(50) UNIQUE NOT NULL,

    issue_date DATE,
    expiry_date DATE,

    verification_status ENUM(
        'Verified',
        'Pending',
        'Rejected',
        'Failed'
    ) DEFAULT 'Pending',

    verified_by INT DEFAULT NULL,

    verification_date TIMESTAMP NULL DEFAULT NULL,

    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    document_expired BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_kyc_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_kyc_employee
        FOREIGN KEY (verified_by)
        REFERENCES employees(employee_id)
);

CREATE TABLE notifications (

    notification_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    notification_type ENUM(
        'Debit',
        'Credit',
        'OTP',
        'Fraud Alert',
        'KYC',
        'Promotional',
        'Loan Update'
    ),

    title VARCHAR(100),

    message VARCHAR(300),

    channel ENUM(
        'SMS',
        'IVRS',
        'WhatsApp',
        'App Notification',
        'E-mail'
    ),

    sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    delivery_status ENUM(
        'Pending',
        'Delivered',
        'Failed'
    ) DEFAULT 'Pending',

    read_status ENUM(
        'Read',
        'Unread'
    ) DEFAULT 'Unread',

    priority ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    ) DEFAULT 'Medium',

    reference_id INT,

    CONSTRAINT fk_notification_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,
    account_id INT NOT NULL,

    loan_type ENUM(
        'Home Loan',
        'Personal Loan',
        'Car Loan',
        'Education Loan',
        'Business Loan',
        'Gold Loan'
    ),

    loan_amount DECIMAL(15,2) NOT NULL,
    interest_rate DECIMAL(5,2) NOT NULL,

    tenure_months INT NOT NULL,
    emi_amount DECIMAL(15,2),

    loan_status ENUM(
        'Pending',
        'Approved',
        'Rejected',
        'Closed'
    ) DEFAULT 'Pending',

    approved_by INT DEFAULT NULL,
    approved_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_loan_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_loan_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id),

    CONSTRAINT fk_loan_employee
        FOREIGN KEY (approved_by)
        REFERENCES employees(employee_id)
);

ALTER TABLE customers
ADD COLUMN customer_status ENUM(
'Active',
'Inactive',
'Blocked'
) DEFAULT 'Active';

ALTER TABLE customers
MODIFY COLUMN kyc_status ENUM(
'Pending',
'Verified',
'Rejected'
) DEFAULT 'Pending';

ALTER TABLE customers
MODIFY COLUMN gender ENUM(
'Male',
'Female',
'Other'
);

ALTER TABLE customers
MODIFY COLUMN country VARCHAR(100) DEFAULT 'India';

ALTER TABLE accounts
MODIFY COLUMN account_type ENUM(
'Savings',
'Current',
'Salary',
'Fixed Deposit'
) NOT NULL;

ALTER TABLE accounts
MODIFY COLUMN account_status ENUM(
'Active',
'Inactive',
'Frozen',
'Closed'
) DEFAULT 'Active';

ALTER TABLE accounts
ADD CONSTRAINT fk_accounts_branch
FOREIGN KEY (branch_id)
REFERENCES branches(branch_id);

ALTER TABLE branches
ADD CONSTRAINT fk_branches_manager
FOREIGN KEY (branch_manager_id)
REFERENCES employees(employee_id);

ALTER TABLE branches
ADD CONSTRAINT uq_branch_contact
UNIQUE (contact_number);

ALTER TABLE branches
ADD CONSTRAINT uq_branch_email
UNIQUE (branch_email);

ALTER TABLE transactions
MODIFY COLUMN transaction_type ENUM(
'Credit',
'Debit',
'Transfer',
'Withdrawal',
'Deposit',
'Refund'
) NOT NULL;

ALTER TABLE transactions
MODIFY COLUMN transaction_status ENUM(
'Pending',
'Success',
'Failed',
'Reversed'
) DEFAULT 'Pending';

ALTER TABLE transactions
MODIFY COLUMN payment_mode ENUM(
'UPI',
'NEFT',
'RTGS',
'IMPS',
'Card',
'Cash',
'Cheque',
'Net Banking'
) NOT NULL;

ALTER TABLE transactions
CHANGE COLUMN receiver_account receiver_account_id INT;

ALTER TABLE transactions
ADD CONSTRAINT fk_transactions_receiver
FOREIGN KEY (receiver_account_id)
REFERENCES accounts(account_id);

ALTER TABLE transactions
ADD CONSTRAINT fk_transactions_merchant
FOREIGN KEY (merchant_id)
REFERENCES merchants(merchant_id);

ALTER TABLE transactions
ADD CONSTRAINT fk_transactions_device
FOREIGN KEY (device_id)
REFERENCES devices(device_id);

ALTER TABLE transactions
ADD COLUMN risk_score INT DEFAULT 0;

ALTER TABLE devices
MODIFY COLUMN device_status ENUM(
'Active',
'Blocked',
'Inactive'
) DEFAULT 'Active';

ALTER TABLE devices
ADD COLUMN registered_from ENUM(
'Mobile App',
'Internet Banking',
'Branch'
) DEFAULT 'Mobile App';

ALTER TABLE devices
ADD COLUMN failed_login_attempts INT DEFAULT 0;

ALTER TABLE devices
ADD COLUMN blocked_at TIMESTAMP NULL DEFAULT NULL;

ALTER TABLE merchants
MODIFY COLUMN merchant_category ENUM(
'Retail',
'Grocery',
'Restaurant',
'Fuel',
'Healthcare',
'E-commerce',
'Travel',
'Entertainment',
'Education',
'Utilities'
);

ALTER TABLE merchants
MODIFY COLUMN merchant_type ENUM(
'Individual',
'Business',
'Corporate'
);

ALTER TABLE merchants
MODIFY COLUMN merchant_status ENUM(
'Active',
'Inactive',
'Suspended',
'Blocked'
) DEFAULT 'Active';

ALTER TABLE merchant_devices
MODIFY COLUMN merchant_device_status ENUM(
'Active',
'Inactive',
'Blocked',
'Lost',
'Damaged',
'Under Maintenance'
) DEFAULT 'Active';

ALTER TABLE merchant_devices
ADD COLUMN branch_id INT;

ALTER TABLE merchant_devices
ADD CONSTRAINT fk_merchant_devices_branch
FOREIGN KEY (branch_id)
REFERENCES branches(branch_id);

ALTER TABLE merchant_devices
ADD COLUMN warranty_expiry DATE;

ALTER TABLE merchant_devices
ADD COLUMN last_used_at TIMESTAMP NULL DEFAULT NULL;

ALTER TABLE merchant_devices
ADD COLUMN firmware_version VARCHAR(20);

ALTER TABLE cards
MODIFY COLUMN card_type ENUM(
'Debit',
'Credit',
'Prepaid',
'Virtual'
);

ALTER TABLE cards
MODIFY COLUMN card_status ENUM(
'Active',
'Inactive',
'Blocked',
'Expired',
'Hotlisted'
) DEFAULT 'Active';

ALTER TABLE cards
ADD COLUMN block_reason VARCHAR(100);

ALTER TABLE beneficiaries
MODIFY COLUMN beneficiary_status ENUM(
'Active',
'Inactive',
'Blocked'
) DEFAULT 'Active';

ALTER TABLE beneficiaries
ADD CONSTRAINT uq_customer_beneficiary
UNIQUE (
customer_id,
account_number,
ifsc_code
);

ALTER TABLE beneficiaries
ADD COLUMN verified_at TIMESTAMP NULL DEFAULT NULL;

ALTER TABLE beneficiaries
ADD COLUMN added_via ENUM(
'Mobile App',
'Internet Banking',
'Branch'
) DEFAULT 'Mobile App';

ALTER TABLE employees
MODIFY COLUMN gender ENUM(
'Male',
'Female',
'Other'
);

ALTER TABLE employees
MODIFY COLUMN employee_status ENUM(
'Active',
'Inactive',
'Suspended',
'Resigned'
) DEFAULT 'Active';

ALTER TABLE employees
MODIFY COLUMN country VARCHAR(100)
DEFAULT 'India';

ALTER TABLE employees
ADD COLUMN manager_id INT;

ALTER TABLE employees
ADD CONSTRAINT fk_employee_manager
FOREIGN KEY (manager_id)
REFERENCES employees(employee_id);

ALTER TABLE employees
ADD COLUMN exit_date DATE;

ALTER TABLE fraud_alerts
ADD COLUMN priority ENUM(
'Low',
'Medium',
'High',
'Critical'
) DEFAULT 'Medium';

ALTER TABLE fraud_alerts
ADD COLUMN fraud_confirmed BOOLEAN DEFAULT FALSE;

ALTER TABLE fraud_alerts
ADD COLUMN resolution_reason VARCHAR(255);

ALTER TABLE fraud_alerts
ADD CONSTRAINT chk_risk_score
CHECK (risk_score BETWEEN 0 AND 100);

CREATE TABLE audit_logs (

    audit_id INT AUTO_INCREMENT PRIMARY KEY,

    employee_id INT NOT NULL,

    table_name VARCHAR(50) NOT NULL,

    record_id INT NOT NULL,

    action_type ENUM(
        'INSERT',
        'UPDATE',
        'DELETE'
    ) NOT NULL,

    old_value TEXT,
    new_value TEXT,

    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    action_source ENUM(
        'Branch',
        'Mobile App',
        'Internet Banking',
        'Admin Portal',
        'API'
    ) DEFAULT 'Branch',

    device_id INT DEFAULT NULL,

    session_id VARCHAR(100),

    ip_address VARCHAR(45),

    remarks VARCHAR(255),

    CONSTRAINT fk_audit_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    CONSTRAINT fk_audit_device
        FOREIGN KEY (device_id)
        REFERENCES devices(device_id)

);

ALTER TABLE login_history
ADD COLUMN login_city VARCHAR(50),
ADD COLUMN login_state VARCHAR(50),
ADD COLUMN login_country VARCHAR(50);

ALTER TABLE login_history
ADD COLUMN logout_reason ENUM(
'User Logout',
'Session Timeout',
'Forced Logout'
);

ALTER TABLE login_history
ADD COLUMN is_suspicious BOOLEAN DEFAULT FALSE;

ALTER TABLE kyc_documents
ADD CONSTRAINT uq_customer_document
UNIQUE (
customer_id,
document_type
);

ALTER TABLE kyc_documents
ADD COLUMN uploaded_via ENUM(
'Branch',
'Mobile App',
'Internet Banking'
) DEFAULT 'Mobile App';

ALTER TABLE kyc_documents
ADD COLUMN rejection_reason VARCHAR(255);

ALTER TABLE kyc_documents
ADD COLUMN document_path VARCHAR(255);

ALTER TABLE notifications
ADD COLUMN reference_type ENUM(
'Transaction',
'Loan',
'Fraud Alert',
'KYC',
'Card',
'Account'
);

ALTER TABLE notifications
ADD COLUMN read_at TIMESTAMP NULL DEFAULT NULL;

ALTER TABLE notifications
ADD COLUMN retry_count TINYINT DEFAULT 0;

ALTER TABLE notifications
ADD COLUMN expires_at TIMESTAMP NULL DEFAULT NULL;

ALTER TABLE loans
ADD COLUMN loan_start_date DATE AFTER emi_amount,
ADD COLUMN loan_end_date DATE AFTER loan_start_date;

ALTER TABLE loans
ADD COLUMN outstanding_balance DECIMAL(15,2);

ALTER TABLE loans
ADD COLUMN paid_emi_count INT DEFAULT 0;

ALTER TABLE loans
ADD COLUMN next_emi_date DATE;

ALTER TABLE loans
ADD COLUMN rejection_reason VARCHAR(255);

ALTER TABLE loans
MODIFY COLUMN loan_status ENUM(
'Pending',
'Approved',
'Rejected',
'Active',
'Closed',
'Defaulted'
) DEFAULT 'Pending';

CREATE INDEX idx_transactions_account
ON transactions(account_id);

CREATE INDEX idx_transactions_time
ON transactions(transaction_time);

CREATE INDEX idx_transactions_status
ON transactions(transaction_status);

CREATE INDEX idx_fraud_status
ON fraud_alerts(alert_status);

CREATE INDEX idx_fraud_score
ON fraud_alerts(risk_score);

CREATE INDEX idx_customer_city
ON customers(city);

CREATE INDEX idx_customer_mobile
ON customers(mobile_number);

CREATE INDEX idx_login_customer
ON login_history(customer_id);

CREATE INDEX idx_login_time
ON login_history(login_time);

SHOW INDEX FROM customers;

SHOW INDEX FROM accounts;

SHOW INDEX FROM transactions;

SHOW INDEX FROM fraud_alerts;