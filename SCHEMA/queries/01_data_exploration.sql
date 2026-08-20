-- Q1. Total customers and customers having at least one account

SELECT
    (SELECT COUNT(DISTINCT customer_id)
     FROM customers) AS total_customers,

    (SELECT COUNT(DISTINCT customer_id)
     FROM accounts) AS customers_with_account;

-- Find the consumer who has more than 2 bank accounts

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(a.account_id) AS account_count
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
HAVING COUNT(a.account_id) >= 2
ORDER BY account_count DESC;

-- Find the consumer who don't have any bank account.

SELECT
    c.customer_id,
    c.customer_name
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id
WHERE a.customer_id IS NULL
ORDER BY c.customer_id;

-- Each account type and their total balance.

select account_type , count(*) as total_accounts, sum(balance) as total_balance_in_INR
    from accounts group by account_type order by sum(balance);

-- Top 5 accounts with heighest balance.

select 
    account_id , 
    customer_id , 
    account_number , 
    account_type , 
    balance 
from accounts order by balance desc limit 5;

--  Find the consumer who have more than 2 bank accounts and their combined balance is greater than ₹5,00,000.
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(a.account_id) AS total_accounts,
    SUM(a.balance) AS total_balance
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
HAVING COUNT(a.account_id) >= 2
   AND SUM(a.balance) > 500000
ORDER BY total_balance DESC;

-- Categorize the accounts  on their balance:
SELECT
    account_id,
    account_number,
    balance,
    CASE
        WHEN balance > 200000 THEN "High"
        WHEN balance BETWEEN 50000 AND 200000 THEN "Medium"
        ELSE "Low Balance"
    END AS balance_category
FROM accounts
ORDER BY balance DESC;

-- Find out total accounts , total balance and average account balance for each balance.

SELECT
    b.branch_code,
    COUNT(a.account_id) AS total_accounts,
    SUM(a.balance) AS total_balance,
    AVG(a.balance)
FROM accounts a
JOIN branches b
    ON a.branch_id = b.branch_id
GROUP BY b.branch_code
ORDER BY SUM(a.balance) DESC;

-- Find out heighest balance from each brancj

WITH ranked_accounts AS (
    SELECT
        b.branch_code,
        a.account_id,
        a.account_number,
        a.customer_id,
        a.balance,
        ROW_NUMBER() OVER (
            PARTITION BY b.branch_code
            ORDER BY a.balance DESC
        ) AS account_rank
    FROM accounts a
    JOIN branches b
        ON a.branch_id = b.branch_id
)

SELECT
    branch_code,
    account_id,
    account_number,
    customer_id,
    balance
FROM ranked_accounts
WHERE account_rank = 1
ORDER BY branch_code;

