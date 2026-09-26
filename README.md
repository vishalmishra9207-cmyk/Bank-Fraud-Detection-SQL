🏦 Bank Fraud Detection & Risk Analysis — SQL + Power BI

An end-to-end bank fraud detection and transaction risk analysis project built using MySQL and Power BI.

The project simulates a small-bank environment and focuses on identifying suspicious transactions, analyzing customer fraud exposure, understanding transaction behavior, and presenting fraud insights through an interactive 3-page Power BI dashboard.

📌 Project Overview

Financial institutions process thousands of transactions every day. The goal of this project is to use SQL-based analysis to identify potentially suspicious activity and convert the results into business-friendly Power BI insights.

Key objectives

Analyze customer and account-level transaction behavior

Identify fraudulent and suspicious transactions

Measure fraud amount and fraud transaction volume

Detect unusually high-value transactions

Compare suspicious transaction amounts with normal successful transactions

Analyze fraud by payment mode and branch

Identify customers/accounts with higher fraud exposure

Build an interactive executive fraud dashboard

🛠️ Tech Stack

Tool

Purpose

MySQL

Database design, data analysis and SQL queries

Power BI

Interactive dashboard and data visualization

DAX

Measures and KPI calculations

Excel

Supporting data/reporting work

Git & GitHub

Version control and project documentation

VS Code

SQL/project development

🗄️ Database

Database:

bank_fraud_db

The project is designed around a small-bank-style relational database containing entities such as:

Customers

Accounts

Branches

Transactions

Cards

Devices

Merchants

Merchant Devices

Beneficiaries

Fraud Alerts

Audit Logs

Login History

KYC Documents

Notifications

Employees

Relationships are implemented using primary keys and foreign keys to maintain relational integrity.

🔎 SQL Analysis

The project contains a structured set of analytical SQL queries covering areas such as:

Transaction Analysis

Transaction volume

Transaction status analysis

Successful transaction analysis

Transaction amount analysis

Payment mode analysis

Monthly/quarterly transaction trends

Fraud Analysis

Fraud transaction count

Total fraud amount

Fraud rate

Fraud by branch

Fraud by payment mode

Customer fraud exposure

Fraud transaction distribution

Suspicious Activity Detection

High-value transactions

Transactions significantly above a customer's normal successful transaction amount

Suspicious transaction identification using CTEs and window functions

Customers with fraud activity and high successful transaction volume

Accounts with suspicious transaction activity

SQL Concepts Used

JOIN

CASE

GROUP BY

HAVING

Subqueries

Correlated subqueries

NOT EXISTS

CTEs

Window functions

Aggregations

Views

Indexes

Conditional filtering

📊 Power BI Dashboard

The final dashboard contains 3 analytical pages.

1️⃣ Executive Fraud Overview

Provides a high-level view of the bank's transaction and fraud activity.

Key KPIs

Total Transactions

Total Transaction Amount

Fraud Transactions

Total Fraud Amount

Visual analysis

Top Customers by Fraud Amount

Transaction Status Overview

Fraud by Branch

Fraud Amount by Payment Mode

Fraud Trend Over Time

Interactive filters

Payment Mode

Transaction Date

2️⃣ Customer Fraud & Transaction Risk Analysis

Focuses on customer-level fraud exposure and transaction behavior.

Key KPIs

Total Fraud Transactions

Total Fraud Amount

Customers with Fraud

Fraud Rate

Visual analysis

Top 10 Customers by Fraud Amount

Transaction Count vs Fraud Count by Payment Mode

Customers with Highest Fraud Exposure

Successful Transaction Amount vs Fraud Amount

Fraud vs Non-Fraud Transactions

Additional customer-level fraud analysis

Interactive filters

Customer

Transaction Status

3️⃣ Suspicious Transaction & Risk Analysis

Focuses on potentially suspicious and unusually high-value transactions.

Key KPIs

Suspicious Transactions

Suspicious Transaction Amount

Average Successful Transaction Amount

Average Suspicious Transaction Amount

Visual analysis

Top 10 Accounts by Suspicious Transaction Amount

Suspicious Amount vs Average Successful Amount

Suspicious Transaction Amount vs Average Successful Amount by Quarter

Suspicious Transactions by Customer

Successful Transaction Activity by Customer

Suspicious Amount by Payment Mode

Interactive filters

Transaction Date

Payment Mode

📈 Sample Dashboard Snapshot

The current dashboard dataset contains approximately:

50K transactions

~1.9K fraud transactions

~3.8% fraud rate

~237.27M total fraud amount

~6.27B total transaction amount

These figures represent the current project dataset/dashboard output and may change if the underlying data is regenerated or updated.

💡 Business Questions Answered

This project helps answer questions such as:

Which customers have the highest fraud exposure?

Which branches process the highest fraud amount?

Which payment modes show higher fraud amounts?

What proportion of transactions are fraudulent?

Which accounts show suspicious high-value activity?

How does suspicious transaction value compare with normal successful transactions?

Which customers have both fraud activity and significant successful transaction volume?

How does fraud activity change over time?

Which transaction statuses dominate overall transaction activity?

Which customers/accounts should be investigated further based on transaction behavior?

📂 Suggested Repository Structure

Bank-Fraud-Detection-SQL/
│
├── SCHEMA/
│   ├── tables/
│   ├── queries/
│   │   └── 01_data_exploration.sql
│   └── views/
│
├── DATA/
│
├── POWER_BI/
│   └── Bank_Fraud_Detection_Dashboard.pbix
│
├── README.md
└── .gitignore

🚀 Project Workflow

Database Design
      ↓
Data Generation / Loading
      ↓
SQL Data Exploration
      ↓
Fraud & Suspicious Activity Analysis
      ↓
SQL Query Validation
      ↓
Power BI Data Import
      ↓
DAX / KPI Creation
      ↓
Interactive Dashboard
      ↓
Business Insights

🎯 Skills Demonstrated

This project demonstrates practical experience with:

Relational database design

SQL querying

Fraud/risk analysis

Data cleaning and aggregation

Customer-level analysis

Transaction-level analysis

CTEs and window functions

Power BI visualization

DAX measures

Interactive slicers

Dashboard design

Git/GitHub version control

Business-oriented data storytelling

👤 Author

Vishal Mishra

Aspiring Data Analyst focused on SQL, Power BI, Excel and Python.

GitHub: vishalmishra9207-cmyk

📌 Future Improvements

Potential next iterations include:

Customer drill-through pages

Custom report tooltips

Fraud alert severity analysis

Time-based anomaly detection

More advanced DAX measures

Automated data refresh

Additional fraud detection rules

Executive-level insight summaries

⭐ Project Goal

The goal of this project is not just to write SQL queries, but to demonstrate how raw banking transaction data can be transformed into actionable fraud and risk insights using SQL + Power BI.
