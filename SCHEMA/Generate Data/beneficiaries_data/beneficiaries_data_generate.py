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

TOTAL_RECORDS = 5000
TOTAL_CUSTOMERS = 1000

START_DATE = datetime(2024, 1, 1, 0, 0, 0)
END_DATE = datetime(2026, 8, 17, 23, 59, 59)


# ============================================================
# CONFIGURATION
# ============================================================

account_types = [
    "Savings",
    "Current"
]

account_type_weights = [
    85,
    15
]


beneficiary_statuses = [
    "Active",
    "Inactive",
    "Blocked"
]

beneficiary_status_weights = [
    85,
    12,
    3
]


added_via_options = [
    "Mobile App",
    "Internet Banking",
    "Branch"
]

added_via_weights = [
    55,
    35,
    10
]


bank_names = [
    "State Bank of India",
    "HDFC Bank",
    "ICICI Bank",
    "Axis Bank",
    "Kotak Mahindra Bank",
    "Punjab National Bank",
    "Bank of Baroda",
    "Canara Bank",
    "Union Bank of India",
    "IndusInd Bank",
    "IDFC First Bank",
    "Yes Bank"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_account_number():

    return str(
        random.randint(
            100000000000,
            9999999999999999
        )
    )


def generate_ifsc():

    bank_code = random.choice(
        [
            "SBIN",
            "HDFC",
            "ICIC",
            "UTIB",
            "KKBK",
            "PUNB",
            "BARB",
            "CNRB",
            "UBIN",
            "INDB",
            "IDFB",
            "YESB"
        ]
    )

    branch_code = f"{random.randint(1, 999999):06d}"

    return bank_code + "0" + branch_code


def generate_upi_id(name):

    clean_name = (
        name.lower()
        .replace(" ", "")
        .replace(".", "")
    )

    random_number = random.randint(
        10,
        9999
    )

    providers = [
        "oksbi",
        "okhdfcbank",
        "okicici",
        "okaxis",
        "ybl",
        "paytm"
    ]

    return (
        f"{clean_name}{random_number}@"
        f"{random.choice(providers)}"
    )


def random_datetime():

    time_difference = (
        END_DATE - START_DATE
    )

    random_seconds = random.randint(
        0,
        int(
            time_difference.total_seconds()
        )
    )

    return (
        START_DATE
        + timedelta(
            seconds=random_seconds
        )
    )


# ============================================================
# GENERATE DATA
# ============================================================

records = []

used_combinations = set()


while len(records) < TOTAL_RECORDS:

    # --------------------------------------------------------
    # CUSTOMER
    # --------------------------------------------------------

    customer_id = random.randint(
        1,
        TOTAL_CUSTOMERS
    )


    # --------------------------------------------------------
    # BENEFICIARY NAME
    # --------------------------------------------------------

    beneficiary_name = fake.name()


    # --------------------------------------------------------
    # NICKNAME
    # --------------------------------------------------------

    if random.random() < 0.70:

        nickname_options = [
            "Mom",
            "Dad",
            "Brother",
            "Sister",
            "Friend",
            "Office",
            "Home",
            "Business",
            "Personal",
            "Vendor"
        ]

        nickname = random.choice(
            nickname_options
        )

    else:

        nickname = None


    # --------------------------------------------------------
    # ACCOUNT NUMBER + IFSC
    # --------------------------------------------------------

    while True:

        account_number = (
            generate_account_number()
        )

        ifsc_code = generate_ifsc()

        combination = (
            customer_id,
            account_number,
            ifsc_code
        )

        if combination not in used_combinations:

            used_combinations.add(
                combination
            )

            break


    # --------------------------------------------------------
    # BANK
    # --------------------------------------------------------

    bank_name = random.choice(
        bank_names
    )


    # --------------------------------------------------------
    # ACCOUNT TYPE
    # --------------------------------------------------------

    account_type = random.choices(
        account_types,
        weights=account_type_weights
    )[0]


    # --------------------------------------------------------
    # MOBILE NUMBER
    # --------------------------------------------------------

    if random.random() < 0.90:

        beneficiary_mobile_number = (
            fake.numerify(
                "##########"
            )
        )

    else:

        beneficiary_mobile_number = None


    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    if random.random() < 0.80:

        email_name = (
            beneficiary_name
            .lower()
            .replace(" ", ".")
        )

        beneficiary_email = (
            f"{email_name}"
            f"{random.randint(10,999)}"
            "@example.com"
        )

    else:

        beneficiary_email = None


    # --------------------------------------------------------
    # UPI ID
    # --------------------------------------------------------

    if random.random() < 0.65:

        upi_id = generate_upi_id(
            beneficiary_name
        )

    else:

        upi_id = None


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    beneficiary_status = random.choices(
        beneficiary_statuses,
        weights=beneficiary_status_weights
    )[0]


    # --------------------------------------------------------
    # VERIFIED
    # --------------------------------------------------------

    if beneficiary_status == "Blocked":

        is_verified = 1

    elif beneficiary_status == "Active":

        is_verified = random.choices(
            [0, 1],
            weights=[15, 85]
        )[0]

    else:

        is_verified = random.choices(
            [0, 1],
            weights=[40, 60]
        )[0]


    # --------------------------------------------------------
    # ADDED ON
    # --------------------------------------------------------

    added_on = random_datetime()


    # --------------------------------------------------------
    # VERIFIED AT
    # --------------------------------------------------------

    if is_verified == 1:

        verified_at = (
            added_on
            + timedelta(
                minutes=random.randint(
                    5,
                    10080
                )
            )
        )

        if verified_at > END_DATE:

            verified_at = END_DATE

    else:

        verified_at = None


    # --------------------------------------------------------
    # ADDED VIA
    # --------------------------------------------------------

    added_via = random.choices(
        added_via_options,
        weights=added_via_weights
    )[0]


    # --------------------------------------------------------
    # RECORD
    # --------------------------------------------------------

    record = {

        "customer_id":
            customer_id,

        "beneficiary_name":
            beneficiary_name,

        "nickname":
            nickname,

        "account_number":
            account_number,

        "ifsc_code":
            ifsc_code,

        "bank_name":
            bank_name,

        "account_type":
            account_type,

        "beneficiary_mobile_number":
            beneficiary_mobile_number,

        "beneficiary_email":
            beneficiary_email,

        "upi_id":
            upi_id,

        "beneficiary_status":
            beneficiary_status,

        "is_verified":
            is_verified,

        "added_on":
            added_on,

        "verified_at":
            verified_at,

        "added_via":
            added_via
    }

    records.append(
        record
    )


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    records
)


# ============================================================
# SAVE CSV
# ============================================================

output_file = (
    Path(__file__).parent
    / "beneficiaries.csv"
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
print("BENEFICIARIES DATA GENERATION COMPLETED")
print("=" * 65)

print()

print("Total records:")
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

print("Duplicate customer/account/IFSC combinations:")

duplicate_combinations = (
    df[
        [
            "customer_id",
            "account_number",
            "ifsc_code"
        ]
    ]
    .duplicated()
    .sum()
)

print(
    duplicate_combinations
)

print()

print("Invalid customer IDs:")

invalid_customers = (
    (
        df["customer_id"] < 1
    )
    |
    (
        df["customer_id"]
        > TOTAL_CUSTOMERS
    )
).sum()

print(
    invalid_customers
)

print()

print("Invalid IFSC codes:")

invalid_ifsc = (
    ~df["ifsc_code"]
    .str.match(
        r"^[A-Z]{4}0[A-Z0-9]{6}$"
    )
).sum()

print(
    invalid_ifsc
)

print()

print("Invalid verified_at records:")

invalid_verified_at = (
    df["verified_at"].notna()
    &
    (
        pd.to_datetime(
            df["verified_at"]
        )
        <
        pd.to_datetime(
            df["added_on"]
        )
    )
).sum()

print(
    invalid_verified_at
)

print()

print("Verified status distribution:")
print(
    df["is_verified"]
    .value_counts()
)

print()

print("Beneficiary status distribution:")
print(
    df["beneficiary_status"]
    .value_counts()
)

print()

print("Added via distribution:")
print(
    df["added_via"]
    .value_counts()
)

print()

print("First 5 records:")
print(
    df.head()
)

print()

print("CSV file created:")
print(
    output_file
)

print()

print("=" * 65)
print("BENEFICIARIES CSV SAVED SUCCESSFULLY!")
print("=" * 65)