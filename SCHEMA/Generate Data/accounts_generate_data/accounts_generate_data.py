from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# --------------------------------------------------
# BASIC SETUP
# --------------------------------------------------

fake = Faker("en_IN")

TOTAL_ACCOUNTS = 1500

TOTAL_CUSTOMERS = 1000
TOTAL_BRANCHES = 20


# --------------------------------------------------
# ACCOUNT TYPES
# --------------------------------------------------

account_types = [
    "Savings",
    "Current",
    "Salary",
    "Premium"
]


# --------------------------------------------------
# ACCOUNT NUMBER GENERATOR
# --------------------------------------------------

used_account_numbers = set()


def generate_account_number():

    while True:

        account_number = str(
            random.randint(
                100000000000,
                999999999999
            )
        )

        if account_number not in used_account_numbers:

            used_account_numbers.add(account_number)

            return account_number


# --------------------------------------------------
# ACCOUNT STATUS
# --------------------------------------------------

def generate_account_status():

    return random.choices(
        [
            "Active",
            "Inactive",
            "Frozen",
            "Closed"
        ],
        weights=[
            90,
            5,
            2,
            3
        ]
    )[0]


# --------------------------------------------------
# ACCOUNT BALANCE
# --------------------------------------------------

def generate_balance(account_type):

    if account_type == "Savings":

        return round(
            random.uniform(500, 500000),
            2
        )

    elif account_type == "Current":

        return round(
            random.uniform(10000, 2000000),
            2
        )

    elif account_type == "Salary":

        return round(
            random.uniform(1000, 200000),
            2
        )

    else:

        return round(
            random.uniform(50000, 5000000),
            2
        )


# --------------------------------------------------
# OPEN DATE
# --------------------------------------------------

def generate_open_date():

    start_date = datetime(2018, 1, 1)

    end_date = datetime(2026, 8, 1)

    days_difference = (
        end_date - start_date
    ).days

    random_days = random.randint(
        0,
        days_difference
    )

    return (
        start_date
        + timedelta(days=random_days)
    ).date()


# --------------------------------------------------
# ACCOUNT DATA
# --------------------------------------------------

accounts = []


for i in range(TOTAL_ACCOUNTS):

    # ----------------------------------------------
    # Existing customer
    # ----------------------------------------------

    customer_id = random.randint(
        1,
        TOTAL_CUSTOMERS
    )


    # ----------------------------------------------
    # Existing branch
    # ----------------------------------------------

    branch_id = random.randint(
        1,
        TOTAL_BRANCHES
    )


    # ----------------------------------------------
    # Account type
    # ----------------------------------------------

    account_type = random.choices(

        account_types,

        weights=[
            65,
            15,
            15,
            5
        ]

    )[0]


    # ----------------------------------------------
    # Account status
    # ----------------------------------------------

    account_status = generate_account_status()


    # ----------------------------------------------
    # Open date
    # ----------------------------------------------

    open_date = generate_open_date()


    # ----------------------------------------------
    # Closed date
    # ----------------------------------------------

    closed_date = None


    if account_status == "Closed":

        closed_date = open_date + timedelta(
            days=random.randint(30, 1500)
        )

        # Make sure closed date doesn't go
        # beyond current date

        if closed_date > datetime.now().date():

            closed_date = datetime.now().date()


    # ----------------------------------------------
    # Balance
    # ----------------------------------------------

    balance = generate_balance(
        account_type
    )


    # ----------------------------------------------
    # Closed account balance
    # ----------------------------------------------

    if account_status == "Closed":

        balance = round(
            random.uniform(0, 1000),
            2
        )


    # ----------------------------------------------
    # Account record
    # ----------------------------------------------

    account = {

        # account_id is AUTO_INCREMENT
        # therefore NOT included

        "customer_id": customer_id,

        "account_number": generate_account_number(),

        "account_type": account_type,

        "balance": balance,

        "account_status": account_status,

        "open_date": open_date,

        "closed_date": closed_date,

        "created_at": datetime.combine(
            open_date,
            datetime.min.time()
        ),

        "branch_id": branch_id
    }


    accounts.append(account)


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(accounts)


# --------------------------------------------------
# SAVE CSV
# --------------------------------------------------

output_file = (
    Path(__file__).parent
    / "accounts.csv"
)


df.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

print()
print("=" * 60)
print("ACCOUNT DATA GENERATION COMPLETED")
print("=" * 60)

print()

print("Total accounts:")
print(len(df))

print()

print("Data shape:")
print(df.shape)

print()

print("Missing values:")
print(df.isnull().sum())

print()

print("Duplicate account numbers:")
print(
    df["account_number"]
    .duplicated()
    .sum()
)

print()

print("Customer ID range:")
print(
    df["customer_id"].min(),
    "to",
    df["customer_id"].max()
)

print()

print("Branch ID range:")
print(
    df["branch_id"].min(),
    "to",
    df["branch_id"].max()
)

print()

print("Account types:")
print(
    df["account_type"]
    .value_counts()
)

print()

print("Account statuses:")
print(
    df["account_status"]
    .value_counts()
)

print()

print("CSV file created:")
print(output_file)

print()

print("First 5 records:")
print(df.head())

print()

print("=" * 60)
print("ACCOUNT CSV SAVED SUCCESSFULLY!")
print("=" * 60)

print()
print("Customer IDs outside range:")
print(
    ((df["customer_id"] < 1) |
     (df["customer_id"] > 1000)).sum()
)

print()

print("Branch IDs outside range:")
print(
    ((df["branch_id"] < 1) |
     (df["branch_id"] > 20)).sum()
)

print()

print("Closed accounts with missing closed_date:")
print(
    (
        (df["account_status"] == "Closed") &
        (df["closed_date"].isnull())
    ).sum()
)

print()

print("Non-closed accounts having closed_date:")
print(
    (
        (df["account_status"] != "Closed") &
        (df["closed_date"].notnull())
    ).sum()
)