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