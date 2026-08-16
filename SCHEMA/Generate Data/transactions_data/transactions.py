import pandas as pd
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# SETUP
# ============================================================

fake = Faker("en_IN")

TOTAL_TRANSACTIONS = 50000

# ACTUAL DATABASE COUNTS
TOTAL_ACCOUNTS = 1500
TOTAL_MERCHANTS = 300
TOTAL_DEVICES = 2000


# ============================================================
# CONFIGURATION
# ============================================================

transaction_types = [
    "Credit",
    "Debit",
    "Transfer",
    "Withdrawal",
    "Deposit",
    "Refund"
]

transaction_type_weights = [
    20,
    35,
    20,
    10,
    10,
    5
]


transaction_statuses = [
    "Pending",
    "Success",
    "Failed",
    "Reversed"
]

transaction_status_weights = [
    5,
    88,
    5,
    2
]


payment_modes = [
    "UPI",
    "NEFT",
    "RTGS",
    "IMPS",
    "Card",
    "Cash",
    "Cheque",
    "Net Banking"
]

payment_mode_weights = [
    40,
    10,
    5,
    15,
    15,
    5,
    3,
    7
]


locations = [
    "Lucknow",
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Jaipur",
    "Ahmedabad",
    "Kanpur",
    "Noida",
    "Gurgaon",
    "Varanasi",
    "Prayagraj"
]


# ============================================================
# REFERENCE NUMBER GENERATOR
# ============================================================

used_reference_numbers = set()


def generate_reference_number():

    while True:

        reference_number = (
            "TXN"
            + datetime.now().strftime("%Y%m%d")
            + uuid.uuid4().hex[:12].upper()
        )

        if reference_number not in used_reference_numbers:

            used_reference_numbers.add(
                reference_number
            )

            return reference_number


# ============================================================
# TRANSACTION AMOUNT
# ============================================================

def generate_amount():

    amount = round(
        random.uniform(
            100,
            250000
        ),
        2
    )

    return amount


# ============================================================
# TRANSACTION TIME
# ============================================================

def generate_transaction_time():

    start_date = datetime(
        2024,
        1,
        1
    )

    end_date = datetime(
        2026,
        8,
        15
    )

    total_seconds = int(
        (
            end_date - start_date
        ).total_seconds()
    )

    random_seconds = random.randint(
        0,
        total_seconds
    )

    return (
        start_date
        + timedelta(
            seconds=random_seconds
        )
    )


# ============================================================
# FRAUD GENERATION
# ============================================================

def generate_fraud_data():

    # Around 4% transactions are fraudulent
    is_fraud = (
        1
        if random.random() < 0.04
        else 0
    )

    if is_fraud == 1:

        risk_score = random.randint(
            70,
            100
        )

        remarks = random.choice(
            [
                "Suspicious transaction",
                "Unusual transaction pattern",
                "High risk transaction",
                "Multiple failed attempts",
                "Unusual device activity",
                "Transaction flagged for review",
                "Potential fraud detected"
            ]
        )

    else:

        risk_score = random.randint(
            0,
            69
        )

        remarks = random.choice(
            [
                None,
                None,
                None,
                "Normal transaction",
                "Regular customer activity",
                "Transaction completed successfully"
            ]
        )

    return (
        is_fraud,
        risk_score,
        remarks
    )


# ============================================================
# OPTIONAL ACCOUNT REFERENCES
# ============================================================

def generate_receiver_account(account_id):

    # Receiver account mainly for transfers
    if random.random() < 0.70:

        receiver_account_id = random.randint(
            1,
            TOTAL_ACCOUNTS
        )

        # Don't allow same account as receiver
        while receiver_account_id == account_id:

            receiver_account_id = random.randint(
                1,
                TOTAL_ACCOUNTS
            )

        return receiver_account_id

    return None


def generate_merchant_id():

    # Some transactions don't involve merchants
    if random.random() < 0.65:

        return random.randint(
            1,
            TOTAL_MERCHANTS
        )

    return None


def generate_device_id():

    # Most digital transactions have device information
    if random.random() < 0.85:

        return random.randint(
            1,
            TOTAL_DEVICES
        )

    return None


# ============================================================
# GENERATE TRANSACTIONS
# ============================================================

transactions = []


for i in range(
    TOTAL_TRANSACTIONS
):

    # --------------------------------------------------------
    # ACCOUNT
    # --------------------------------------------------------

    account_id = random.randint(
        1,
        TOTAL_ACCOUNTS
    )


    # --------------------------------------------------------
    # TRANSACTION TYPE
    # --------------------------------------------------------

    transaction_type = random.choices(
        transaction_types,
        weights=transaction_type_weights
    )[0]


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    transaction_status = random.choices(
        transaction_statuses,
        weights=transaction_status_weights
    )[0]


    # --------------------------------------------------------
    # PAYMENT MODE
    # --------------------------------------------------------

    payment_mode = random.choices(
        payment_modes,
        weights=payment_mode_weights
    )[0]


    # --------------------------------------------------------
    # AMOUNT
    # --------------------------------------------------------

    amount = generate_amount()


    # --------------------------------------------------------
    # TRANSACTION TIME
    # --------------------------------------------------------

    transaction_time = (
        generate_transaction_time()
    )


    # --------------------------------------------------------
    # RECEIVER ACCOUNT
    # --------------------------------------------------------

    if transaction_type == "Transfer":

        receiver_account_id = (
            generate_receiver_account(
                account_id
            )
        )

    else:

        receiver_account_id = None


    # --------------------------------------------------------
    # MERCHANT
    # --------------------------------------------------------

    if transaction_type in [
        "Debit",
        "Credit",
        "Refund"
    ]:

        merchant_id = (
            generate_merchant_id()
        )

    else:

        merchant_id = None


    # --------------------------------------------------------
    # DEVICE
    # --------------------------------------------------------

    if payment_mode in [
        "UPI",
        "Card",
        "IMPS",
        "Net Banking"
    ]:

        device_id = (
            generate_device_id()
        )

    else:

        device_id = None


    # --------------------------------------------------------
    # IP ADDRESS
    # --------------------------------------------------------

    if device_id is not None:

        ip_address = fake.ipv4()

    else:

        ip_address = None


    # --------------------------------------------------------
    # FRAUD
    # --------------------------------------------------------

    (
        is_fraud,
        risk_score,
        remarks
    ) = generate_fraud_data()


    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    transaction_location = random.choice(
        locations
    )


    # --------------------------------------------------------
    # REFERENCE NUMBER
    # --------------------------------------------------------

    reference_number = (
        generate_reference_number()
    )


    # --------------------------------------------------------
    # CREATE RECORD
    # --------------------------------------------------------

    transaction = {

        "account_id":
            account_id,

        "reference_number":
            reference_number,

        "amount":
            amount,

        "transaction_type":
            transaction_type,

        "transaction_time":
            transaction_time,

        "transaction_status":
            transaction_status,

        "payment_mode":
            payment_mode,

        "transaction_location":
            transaction_location,

        "receiver_account_id":
            receiver_account_id,

        "merchant_id":
            merchant_id,

        "device_id":
            device_id,

        "ip_address":
            ip_address,

        "is_fraud":
            is_fraud,

        "remarks":
            remarks,

        "risk_score":
            risk_score
    }

    transactions.append(
        transaction
    )


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    transactions
)


# ============================================================
# SAVE CSV
# ============================================================

output_file = (
    Path(__file__).parent
    / "transactions.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print()
print("=" * 65)
print("TRANSACTION DATA GENERATION COMPLETED")
print("=" * 65)

print()

print("Total transactions:")
print(
    len(df)
)

print()

print("Data shape:")
print(
    df.shape
)

print()

print("Missing values:")
print(
    df.isnull().sum()
)

print()

print("Duplicate reference numbers:")
print(
    df["reference_number"]
    .duplicated()
    .sum()
)

print()

print("Invalid account IDs:")
print(
    (
        (df["account_id"] < 1)
        |
        (df["account_id"] > TOTAL_ACCOUNTS)
    ).sum()
)

print()

print("Invalid receiver account IDs:")

invalid_receiver = (
    df["receiver_account_id"].notna()
    &
    (
        (df["receiver_account_id"] < 1)
        |
        (
            df["receiver_account_id"]
            > TOTAL_ACCOUNTS
        )
    )
).sum()

print(
    invalid_receiver
)

print()

print("Invalid merchant IDs:")

invalid_merchants = (
    df["merchant_id"].notna()
    &
    (
        (df["merchant_id"] < 1)
        |
        (
            df["merchant_id"]
            > TOTAL_MERCHANTS
        )
    )
).sum()

print(
    invalid_merchants
)

print()

print("Invalid device IDs:")

invalid_devices = (
    df["device_id"].notna()
    &
    (
        (df["device_id"] < 1)
        |
        (
            df["device_id"]
            > TOTAL_DEVICES
        )
    )
).sum()

print(
    invalid_devices
)

print()

print("Fraud distribution:")
print(
    df["is_fraud"]
    .value_counts()
)

print()

print("Transaction type distribution:")
print(
    df["transaction_type"]
    .value_counts()
)

print()

print("Transaction status distribution:")
print(
    df["transaction_status"]
    .value_counts()
)

print()

print("Payment mode distribution:")
print(
    df["payment_mode"]
    .value_counts()
)

print()

print("Fraud transactions with low risk score:")

fraud_low_risk = (
    (
        df["is_fraud"] == 1
    )
    &
    (
        df["risk_score"] < 70
    )
).sum()

print(
    fraud_low_risk
)

print()

print("Non-fraud transactions with high risk score:")

nonfraud_high_risk = (
    (
        df["is_fraud"] == 0
    )
    &
    (
        df["risk_score"] >= 70
    )
).sum()

print(
    nonfraud_high_risk
)

print()

print("Transfer transactions without receiver:")

transfer_without_receiver = (
    (
        df["transaction_type"]
        == "Transfer"
    )
    &
    (
        df["receiver_account_id"]
        .isna()
    )
).sum()

print(
    transfer_without_receiver
)

print()

print("Non-transfer transactions with receiver:")

nontransfer_with_receiver = (
    (
        df["transaction_type"]
        != "Transfer"
    )
    &
    (
        df["receiver_account_id"]
        .notna()
    )
).sum()

print(
    nontransfer_with_receiver
)

print()

print("CSV file created:")
print(
    output_file
)

print()

print("First 5 records:")
print(
    df.head()
)

print()

print("=" * 65)
print("TRANSACTIONS CSV SAVED SUCCESSFULLY!")
print("=" * 65)