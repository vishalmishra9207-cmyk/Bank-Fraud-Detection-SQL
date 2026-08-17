import csv
import random
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

import mysql.connector


# ============================================================
# SETTINGS
# ============================================================

TOTAL_LOANS = 5000

OUTPUT_FILE = Path(__file__).parent / "loans.csv"


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="bank_fraud_db"
)

cursor = conn.cursor()


# ============================================================
# FETCH VALID ACCOUNT + CUSTOMER MAPPING
# ============================================================

cursor.execute("""
    SELECT account_id, customer_id
    FROM accounts
    WHERE customer_id IS NOT NULL
""")

account_customer_mapping = cursor.fetchall()

if not account_customer_mapping:
    print("ERROR: No valid accounts found!")
    cursor.close()
    conn.close()
    exit()


print()
print(f"Valid account-customer mappings found: {len(account_customer_mapping)}")


# ============================================================
# FETCH EMPLOYEES
# ============================================================

cursor.execute("""
    SELECT employee_id
    FROM employees
""")

employee_ids = [row[0] for row in cursor.fetchall()]

if not employee_ids:
    print("ERROR: No employees found!")
    cursor.close()
    conn.close()
    exit()


print(f"Valid employees found: {len(employee_ids)}")


# ============================================================
# LOAN CONFIGURATION
# ============================================================

loan_config = {
    "Home Loan": {
        "amount": (1000000, 8000000),
        "interest": (7.0, 9.5),
        "tenure": (120, 240)
    },

    "Personal Loan": {
        "amount": (50000, 1500000),
        "interest": (10.0, 18.0),
        "tenure": (12, 84)
    },

    "Car Loan": {
        "amount": (300000, 2500000),
        "interest": (7.5, 11.5),
        "tenure": (36, 84)
    },

    "Education Loan": {
        "amount": (100000, 2000000),
        "interest": (6.5, 10.5),
        "tenure": (60, 180)
    },

    "Business Loan": {
        "amount": (500000, 5000000),
        "interest": (9.0, 16.0),
        "tenure": (24, 120)
    },

    "Gold Loan": {
        "amount": (50000, 1000000),
        "interest": (8.0, 14.0),
        "tenure": (12, 60)
    }
}


loan_types = list(loan_config.keys())


# ============================================================
# HELPER FUNCTION - ADD MONTHS
# ============================================================

def add_months(start_date, months):

    year = start_date.year + (start_date.month - 1 + months) // 12

    month = (start_date.month - 1 + months) % 12 + 1

    day = min(
        start_date.day,
        [
            31,
            29 if year % 4 == 0 and (
                year % 100 != 0 or year % 400 == 0
            ) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31
        ][month - 1]
    )

    return date(year, month, day)


# ============================================================
# EMI CALCULATION
# ============================================================

def calculate_emi(principal, annual_rate, tenure_months):

    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        return principal / tenure_months

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** tenure_months
        / (
            (1 + monthly_rate) ** tenure_months - 1
        )
    )

    return emi


# ============================================================
# GENERATE LOANS
# ============================================================

loan_rows = []

today = date.today()


for loan_number in range(1, TOTAL_LOANS + 1):

    # --------------------------------------------------------
    # VALID ACCOUNT + CUSTOMER PAIR
    # --------------------------------------------------------

    account_id, customer_id = random.choice(
        account_customer_mapping
    )

    # --------------------------------------------------------
    # LOAN TYPE
    # --------------------------------------------------------

    loan_type = random.choice(loan_types)

    config = loan_config[loan_type]

    # --------------------------------------------------------
    # LOAN AMOUNT
    # --------------------------------------------------------

    loan_amount = random.randint(
        config["amount"][0],
        config["amount"][1]
    )

    # Round to nearest 1000
    loan_amount = round(
        loan_amount / 1000
    ) * 1000

    # --------------------------------------------------------
    # INTEREST RATE
    # --------------------------------------------------------

    interest_rate = round(
        random.uniform(
            config["interest"][0],
            config["interest"][1]
        ),
        2
    )

    # --------------------------------------------------------
    # TENURE
    # --------------------------------------------------------

    tenure_months = random.randrange(
        config["tenure"][0],
        config["tenure"][1] + 1,
        12
    )

    # --------------------------------------------------------
    # LOAN STATUS
    # --------------------------------------------------------

    loan_status = random.choices(
        [
            "Pending",
            "Approved",
            "Rejected",
            "Active",
            "Closed",
            "Defaulted"
        ],
        weights=[
            10,
            10,
            5,
            45,
            20,
            10
        ],
        k=1
    )[0]

    # --------------------------------------------------------
    # START DATE
    # --------------------------------------------------------

    loan_start_date = today - timedelta(
        days=random.randint(30, 5 * 365)
    )

    loan_end_date = add_months(
        loan_start_date,
        tenure_months
    )

    # --------------------------------------------------------
    # EMI
    # --------------------------------------------------------

    emi_amount = calculate_emi(
        loan_amount,
        interest_rate,
        tenure_months
    )

    emi_amount = round(
        emi_amount,
        2
    )

    # --------------------------------------------------------
    # APPROVAL INFORMATION
    # --------------------------------------------------------

    if loan_status in [
        "Approved",
        "Active",
        "Closed",
        "Defaulted"
    ]:

        approved_by = random.choice(
            employee_ids
        )

        approved_date = loan_start_date - timedelta(
            days=random.randint(1, 30)
        )

    else:

        approved_by = None
        approved_date = None

    # --------------------------------------------------------
    # PAID EMI COUNT + OUTSTANDING BALANCE
    # --------------------------------------------------------

    if loan_status == "Pending":

        paid_emi_count = 0

        outstanding_balance = Decimal(
            str(loan_amount)
        )

        next_emi_date = None

    elif loan_status == "Rejected":

        paid_emi_count = 0

        outstanding_balance = Decimal("0.00")

        next_emi_date = None

    else:

        months_elapsed = (
            (today.year - loan_start_date.year) * 12
            + today.month
            - loan_start_date.month
        )

        paid_emi_count = max(
            0,
            min(
                months_elapsed,
                tenure_months
            )
        )

        if loan_status == "Closed":

            paid_emi_count = tenure_months

        elif loan_status == "Defaulted":

            paid_emi_count = min(
                paid_emi_count,
                max(1, tenure_months - 3)
            )

        # Simple outstanding principal approximation
        remaining_emi_count = max(
            0,
            tenure_months - paid_emi_count
        )

        outstanding_balance = round(
            Decimal(str(emi_amount))
            * remaining_emi_count,
            2
        )

        if loan_status == "Closed":

            outstanding_balance = Decimal(
                "0.00"
            )

        if loan_status == "Closed":

            next_emi_date = None

        else:

            next_emi_date = add_months(
                loan_start_date,
                paid_emi_count + 1
            )

    # --------------------------------------------------------
    # REJECTION REASON
    # --------------------------------------------------------

    if loan_status == "Rejected":

        rejection_reason = random.choice([
            "Low credit score",
            "Insufficient income",
            "Incomplete documentation",
            "High existing liabilities",
            "Eligibility criteria not met",
            "Unstable employment history"
        ])

    else:

        rejection_reason = None

    # --------------------------------------------------------
    # CREATED AT
    # --------------------------------------------------------

    created_at = loan_start_date

    # --------------------------------------------------------
    # APPEND ROW
    # --------------------------------------------------------

    loan_rows.append([
        customer_id,
        account_id,
        loan_type,
        loan_amount,
        interest_rate,
        tenure_months,
        emi_amount,
        loan_start_date,
        loan_end_date,
        loan_status,
        approved_by,
        approved_date,
        created_at,
        outstanding_balance,
        paid_emi_count,
        next_emi_date,
        rejection_reason
    ])

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    if loan_number % 500 == 0:

        print(
            f"Generated {loan_number}/{TOTAL_LOANS} loans..."
        )


# ============================================================
# WRITE CSV
# ============================================================

headers = [
    "customer_id",
    "account_id",
    "loan_type",
    "loan_amount",
    "interest_rate",
    "tenure_months",
    "emi_amount",
    "loan_start_date",
    "loan_end_date",
    "loan_status",
    "approved_by",
    "approved_date",
    "created_at",
    "outstanding_balance",
    "paid_emi_count",
    "next_emi_date",
    "rejection_reason"
]


with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow(headers)

    writer.writerows(loan_rows)


# ============================================================
# CLOSE DATABASE
# ============================================================

cursor.close()
conn.close()


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 60)
print("LOANS DATA GENERATION SUCCESSFUL!")
print("=" * 60)

print()
print(f"Total loans generated: {TOTAL_LOANS}")

print()
print("CSV file saved at:")
print(OUTPUT_FILE)