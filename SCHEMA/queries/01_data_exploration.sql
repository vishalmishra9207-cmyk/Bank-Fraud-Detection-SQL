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

-- Find out heighest balance from each branch

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

--  Find each consumers total transactions, total transaction amount and average transaction amount.

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_transaction_amount,
    AVG(t.amount) AS average_transaction_amount
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
JOIN transactions t
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.customer_name
HAVING SUM(t.amount) > 100000
ORDER BY total_transaction_amount DESC;

--  Find out creadit and debit transactions count and total amount seprately for each consumer.
SELECT
    c.customer_id,
    c.customer_name,

    SUM(
        CASE
            WHEN t.transaction_type = 'Credit' THEN 1
            ELSE 0
        END
    ) AS credit_transactions,

    SUM(
        CASE
            WHEN t.transaction_type = 'Credit' THEN t.amount
            ELSE 0
        END
    ) AS credit_amount,

    SUM(
        CASE
            WHEN t.transaction_type = 'Debit' THEN 1
            ELSE 0
        END
    ) AS debit_transactions,

    SUM(
        CASE
            WHEN t.transaction_type = 'Debit' THEN t.amount
            ELSE 0
        END
    ) AS debit_amount

FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
JOIN transactions t
    ON a.account_id = t.account_id

GROUP BY
    c.customer_id,
    c.customer_name;

-- Find out total transactions, total transaction amount and average transaction amount for each transaction type.

select 
    transaction_type, 
    count(transaction_id) as total_transactions, 
    sum(amount) as total_amount ,
    avg(amount) as average_amount
from  transactions group by transaction_type order by total_amount desc;

-- Find total transactions and total transaction amount for each month of year 2026

SELECT
    MONTHNAME(transaction_time) AS month_name,
    COUNT(transaction_id) AS total_transaction,
    SUM(amount) AS total_amount
FROM transactions
WHERE YEAR(transaction_time) = "2026"
GROUP BY MONTHNAME(transaction_time)
ORDER BY total_amount DESC;

-- Find out those transactions where amount is more than ₹1,00,000 and transaction should be successfull.
SELECT 
    transaction_id,
    account_id,
    transaction_type,
    amount,
    transaction_time,
    transaction_status
FROM transactions
WHERE transaction_status = 'Success'
  AND amount > 100000
ORDER BY amount DESC
LIMIT 10;

-- Find out the consumer who have made more than 50 transacstions.

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(t.transaction_id) AS total_transactions
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
JOIN transactions t
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.customer_name
HAVING COUNT(t.transaction_id) > 50
ORDER BY total_transactions DESC;



-- Find those account balance is greater than the averga balance of consumer.
-- 1st query
SELECT 
    c.customer_id, 
    c.customer_name, 
    SUM(a.balance) AS total_balance
FROM customers c  
JOIN accounts a 
    ON c.customer_id = a.customer_id 
GROUP BY c.customer_id
HAVING SUM(a.balance) > (
    SELECT AVG(balance)
    FROM accounts
);

-- 2nd query 
SELECT
    c.customer_id,
    c.customer_name,
    SUM(a.balance) AS total_balance
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
HAVING SUM(a.balance) > (
    SELECT AVG(customer_balance)
    FROM (
        SELECT
            customer_id,
            SUM(balance) AS customer_balance
        FROM accounts
        GROUP BY customer_id
    ) AS customer_totals
)
ORDER BY total_balance DESC;

-- Find out those consumer who have more maximum transaction amount than the average transaction amount of DB.

SELECT
    c.customer_id,
    c.customer_name,
    MAX(t.amount) AS max_transaction_amount
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
JOIN transactions t
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.customer_name
HAVING MAX(t.amount) > (
    SELECT AVG(amount)
    FROM transactions
)
ORDER BY max_transaction_amount DESC;