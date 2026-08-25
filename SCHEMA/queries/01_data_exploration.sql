-- --  Data exploration analysis -- --

-- Q1. Total customers and customers having at least one account

SELECT
    (SELECT COUNT(DISTINCT customer_id)
     FROM customers) AS total_customers,

    (SELECT COUNT(DISTINCT customer_id)
     FROM accounts) AS customers_with_account;

-- Q2. Find the consumer who has more than 2 bank accounts

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

-- Q3. Find the consumer who don't have any bank account.

SELECT
    c.customer_id,
    c.customer_name
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id
WHERE a.customer_id IS NULL
ORDER BY c.customer_id;

-- Q4.Each account type and their total balance.

select account_type , count(*) as total_accounts, sum(balance) as total_balance_in_INR
    from accounts group by account_type order by sum(balance);

-- Q5.Top 5 accounts with heighest balance.

select 
    account_id , 
    customer_id , 
    account_number , 
    account_type , 
    balance 
from accounts order by balance desc limit 5;

--  Q6. Find the consumer who have more than 2 bank accounts and their combined balance is greater than ₹5,00,000.
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

-- Q7.Categorize the accounts  on their balance:
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

--Q8.  Find out total accounts , total balance and average account balance for each balance.

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

--Q9. Find out heighest balance from each branch

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

--Q10.  Find each consumers total transactions, total transaction amount and average transaction amount.

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

--Q11.  Find out creadit and debit transactions count and total amount seprately for each consumer.
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

--Q12. Find out total transactions, total transaction amount and average transaction amount for each transaction type.

select 
    transaction_type, 
    count(transaction_id) as total_transactions, 
    sum(amount) as total_amount ,
    avg(amount) as average_amount
from  transactions group by transaction_type order by total_amount desc;

--Q13. Find total transactions and total transaction amount for each month of year 2026

SELECT
    MONTHNAME(transaction_time) AS month_name,
    COUNT(transaction_id) AS total_transaction,
    SUM(amount) AS total_amount
FROM transactions
WHERE YEAR(transaction_time) = "2026"
GROUP BY MONTHNAME(transaction_time)
ORDER BY total_amount DESC;

--Q14. Find out those transactions where amount is more than ₹1,00,000 and transaction should be successfull.
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

--Q15. Find out the consumer who have made more than 50 transacstions.

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

------ INTERMEDIATE SQL QUERIES -----

--Q16. Find those account balance is greater than the averga balance of consumer.
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

--Q17. Find out those consumer who have more maximum transaction amount than the average transaction amount of DB.

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

-- Q18. Find out those consumer whose transaction amount than the average tranaction amount of consumer.

select
    c.customer_id , 
    c.customer_name ,
    sum(t.amount) as total_transaction_amount
from customers c
join accounts a 
    on c.customer_id = a.customer_id 
join transactions t
    on a.account_id = t.account_id
group by 
    c.customer_id ,
    c.customer_name 
having sum(t.amount) > 
(SELECT AVG(customer_total)
FROM (
    SELECT
        c.customer_id,
        SUM(t.amount) AS customer_total
    FROM customers c
    JOIN accounts a
        ON c.customer_id = a.customer_id
    JOIN transactions t
        ON a.account_id = t.account_id
    GROUP BY c.customer_id
) AS customer_totals)
order by total_transaction_amount desc;

--Q19. Rank the consumer on the basis of their transactions. Heighest transaction amount of consumer must be 1.
select 
	c.customer_id ,
	c.customer_name , 
    t.transaction_id , 
	t.amount, 
	row_number() over(partition by c.customer_id order by t.amount desc) as transaction_rank
from customers c 
join accounts a 
	on c.customer_id = a.customer_id 
join transactions t 
	on a.account_id = t.account_id ;

--Q20. Find out high transaction amount made by consumer.

WITH high_transaction AS (
    SELECT
        c.customer_id,
        c.customer_name,
        t.transaction_id,
        t.amount,
        t.transaction_time,
        ROW_NUMBER() OVER (
            PARTITION BY c.customer_id
            ORDER BY t.amount DESC
        ) AS rnk
    FROM customers c
    JOIN accounts a
        ON c.customer_id = a.customer_id
    JOIN transactions t
        ON a.account_id = t.account_id
)

SELECT
    customer_id,
    customer_name,
    transaction_id,
    amount,
    transaction_time
FROM high_transaction
WHERE rnk = 1
ORDER BY amount DESC;

--Q21 Find out those consumer who have made more than 2 transactions in a day.

select 
    c.customer_id , 
    c.customer_name , 
    date(t.transaction_time) as transaction_date, 
    count(t.transaction_id) as total_transactions,
    sum(t.amount) as total_transaction_amount
from customers c 
join accounts a 
    on c.customer_id = a.customer_id 
join transactions t 
    on t.account_id = a.account_id 
group by 
    c.customer_id ,
    c.customer_name ,
    date(t.transaction_time) 
having count(t.transaction_id) > 2;

-- Q22 Find the total account balance for each consumer in each branch.

select 
    c.customer_id , 
    c.customer_name , 
    date(t.transaction_time) as transaction_date, 
    count(t.transaction_id) as total_transactions,
    sum(t.amount) as total_transaction_amount
from customers c 
join accounts a 
    on c.customer_id = a.customer_id 
join transactions t 
    on t.account_id = a.account_id 
group by 
    c.customer_id ,
    c.customer_name ,
    date(t.transaction_time) 
having count(t.transaction_id) > 2;

-- Q22 Find the total account balance for each consumer in each branch.

WITH customer_balances AS (
    SELECT
        b.branch_id,
        b.branch_code,
        c.customer_id,
        c.customer_name,
        SUM(a.balance) AS total_balance
    FROM customers c
    JOIN accounts a
        ON c.customer_id = a.customer_id
    JOIN branches b
        ON b.branch_id = a.branch_id
    GROUP BY
        b.branch_id,
        b.branch_code,
        c.customer_id,
        c.customer_name
)

SELECT
    branch_code,
    customer_id,
    customer_name,
    total_balance,
    RANK() OVER (
        PARTITION BY branch_id
        ORDER BY total_balance DESC
    ) AS balance_rank
FROM customer_balances
ORDER BY
    branch_code,
    balance_rank;


-- Q23 Find top 3 customers for each branch by their total balance.
WITH customer_branch_balance AS (
    SELECT
        b.branch_id,
        b.branch_code,
        c.customer_id,
        c.customer_name,
        SUM(a.balance) AS total_balance
    FROM customers c
    JOIN accounts a
        ON c.customer_id = a.customer_id
    JOIN branches b
        ON a.branch_id = b.branch_id
    GROUP BY
        b.branch_id,
        b.branch_code,
        c.customer_id,
        c.customer_name
),

ranked_customers AS (
    SELECT
        branch_code,
        customer_id,
        customer_name,
        total_balance,
        RANK() OVER (
            PARTITION BY branch_code
            ORDER BY total_balance DESC
        ) AS balance_rnk
    FROM customer_branch_balance
)

SELECT
    branch_code,
    customer_id,
    customer_name,
    total_balance,
    balance_rnk
FROM ranked_customers
WHERE balance_rnk <= 3
ORDER BY branch_code, balance_rnk;

-- Q24 Calculate the total transaction amount for each month of 2026 and determine the increase or decrease in the transaction amount compared to the previous month.

WITH monthly_transactions AS (
    SELECT
        MONTH(transaction_time) AS transaction_month,
        SUM(amount) AS total_amount
    FROM transactions
    WHERE YEAR(transaction_time) = 2026
    GROUP BY MONTH(transaction_time)
),

monthly_with_previous AS (
    SELECT
        transaction_month,
        total_amount,
        LAG(total_amount) OVER (
            ORDER BY transaction_month
        ) AS previous_month_amount
    FROM monthly_transactions
)

SELECT
    transaction_month,
    total_amount,
    previous_month_amount,
    total_amount - previous_month_amount AS amount_difference
FROM monthly_with_previous
ORDER BY transaction_month;

# Calculate the total transaction amount for each month of 2026 and determine the percentage change compared to the previous month.
WITH monthly_transactions AS (
    SELECT
        MONTH(transaction_time) AS transaction_month,
        SUM(amount) AS total_amount
    FROM transactions
    WHERE YEAR(transaction_time) = 2026
    GROUP BY MONTH(transaction_time)
),

monthly_with_previous AS (
    SELECT
        transaction_month,
        total_amount,
        LAG(total_amount) OVER (
            ORDER BY transaction_month
        ) AS previous_month_amount
    FROM monthly_transactions
)

SELECT
    transaction_month,
    total_amount,
    previous_month_amount,
    round((total_amount - previous_month_amount) / previous_month_amount * 100, 2)  AS amount_difference_in_percent
FROM monthly_with_previous
ORDER BY transaction_month;

-- -- View each customer's transactions in chronological order and calculate the 
-- cumulative (running) transaction amount for that customer after each transaction.

SELECT 
    c.customer_id, 
    c.customer_name,
    t.transaction_id,
    t.transaction_time,
    t.amount,
    SUM(t.amount) OVER (
        PARTITION BY c.customer_id
        ORDER BY t.transaction_time
    ) AS running_total
FROM customers c
JOIN accounts a 
    ON c.customer_id = a.customer_id
JOIN transactions t 
    ON t.account_id = a.account_id;

-- Q27 — Customer's Highest Transaction vs Current Transaction.

WITH customer_transactions AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        t.transaction_id,
        t.amount,
        FIRST_VALUE(t.amount) OVER (
            PARTITION BY c.customer_id
            ORDER BY t.amount DESC
        ) AS highest_transaction_amount
    FROM customers c
    JOIN accounts a
        ON c.customer_id = a.customer_id
    JOIN transactions t
        ON t.account_id = a.account_id
)

SELECT
    customer_id,
    customer_name,
    transaction_id,
    amount,
    highest_transaction_amount,
    highest_transaction_amount - amount AS difference_from_highest
FROM customer_transactions;
