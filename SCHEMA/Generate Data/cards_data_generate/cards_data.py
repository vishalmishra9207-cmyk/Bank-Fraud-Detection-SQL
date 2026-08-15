from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# BASIC SETUP
# ============================================================

fake = Faker("en_IN")

TOTAL_CARDS = 1200
TOTAL_ACCOUNTS = 1500


# ============================================================
# CARD CONFIGURATION
# ============================================================

card_types = [
    "Debit",
    "Credit",
    "Prepaid",
    "Virtual"
]

card_type_weights = [
    65,
    20,
    8,
    7
]


card_networks = [
    "Visa",
    "RuPay",
    "Mastercard"
]

card_network_weights = [
    40,
    35,
    25
]


card_statuses = [
    "Active",
    "Inactive",
    "Blocked",
    "Expired",
    "Hotlisted"
]

card_status_weights = [
    82,
    5,
    4,
    4,
    5
]


# ============================================================
# USED CARD NUMBERS
# ============================================================

used_card_numbers = set()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_card_number():

    while True:

        # Generate 16-digit card number
        card_number = (
            str(random.randint(4000, 4999))
            + str(random.randint(1000, 9999))
            + str(random.randint(1000, 9999))
            + str(random.randint(1000, 9999))
        )

        if card_number not in used_card_numbers:

            used_card_numbers.add(
                card_number
            )

            return card_number


def generate_issue_date():

    start_date = datetime(
        2021,
        1,
        1
    )

    end_date = datetime(
        2026,
        6,
        30
    )

    days = (
        end_date - start_date
    ).days

    return (
        start_date +
        timedelta(
            days=random.randint(
                0,
                days
            )
        )
    )


def generate_expiry_date(issue_date):

    # Cards usually have around 5 years validity
    expiry_years = random.choice(
        [3, 4, 5]
    )

    expiry_date = issue_date.replace(
        year=issue_date.year + expiry_years
    )

    return expiry_date.date()


def generate_daily_limit(card_type):

    if card_type == "Debit":

        return random.choice([
            25000,
            50000,
            75000,
            100000,
            150000,
            200000
        ])

    elif card_type == "Credit":

        return random.choice([
            50000,
            100000,
            150000,
            200000,
            300000,
            500000
        ])

    elif card_type == "Prepaid":

        return random.choice([
            10000,
            25000,
            50000,
            75000
        ])

    else:

        return random.choice([
            10000,
            25000,
            50000,
            100000
        ])


def generate_block_reason(card_status):

    if card_status == "Blocked":

        return random.choice([
            "Multiple Failed PIN Attempts",
            "Suspicious Activity",
            "Customer Request",
            "Security Concern",
            "Fraud Suspected"
        ])

    elif card_status == "Hotlisted":

        return random.choice([
            "Card Reported Lost",
            "Card Reported Stolen",
            "Fraud Suspected",
            "Security Risk"
        ])

    elif card_status == "Expired":

        return "Card Expired"

    return None


# ============================================================
# GENERATE CARDS
# ============================================================

cards = []


for i in range(
    1,
    TOTAL_CARDS + 1
):

    # --------------------------------------------------------
    # ACCOUNT
    # --------------------------------------------------------

    account_id = random.randint(
        1,
        TOTAL_ACCOUNTS
    )


    # --------------------------------------------------------
    # CARD TYPE
    # --------------------------------------------------------

    card_type = random.choices(
        card_types,
        weights=card_type_weights
    )[0]


    # --------------------------------------------------------
    # CARD NETWORK
    # --------------------------------------------------------

    card_network = random.choices(
        card_networks,
        weights=card_network_weights
    )[0]


    # --------------------------------------------------------
    # ISSUE DATE
    # --------------------------------------------------------

    issue_date = generate_issue_date()


    # --------------------------------------------------------
    # EXPIRY DATE
    # --------------------------------------------------------

    expiry_date = generate_expiry_date(
        issue_date
    )


    # --------------------------------------------------------
    # CARD STATUS
    # --------------------------------------------------------

    card_status = random.choices(
        card_statuses,
        weights=card_status_weights
    )[0]


    # --------------------------------------------------------
    # MAKE EXPIRY STATUS LOGICAL
    # --------------------------------------------------------

    today = datetime.now().date()

    if expiry_date < today:

        card_status = "Expired"


    # --------------------------------------------------------
    # BLOCK REASON
    # --------------------------------------------------------

    block_reason = generate_block_reason(
        card_status
    )


    # --------------------------------------------------------
    # DAILY LIMIT
    # --------------------------------------------------------

    daily_limit = generate_daily_limit(
        card_type
    )


    # --------------------------------------------------------
    # INTERNATIONAL USAGE
    # --------------------------------------------------------

    international_usage = random.choices(
        [1, 0],
        weights=[20, 80]
    )[0]


    # Virtual cards are more likely to be
    # used internationally

    if card_type == "Virtual":

        international_usage = random.choices(
            [1, 0],
            weights=[35, 65]
        )[0]


    # --------------------------------------------------------
    # CONTACTLESS
    # --------------------------------------------------------

    contactless_enabled = random.choices(
        [1, 0],
        weights=[85, 15]
    )[0]


    # --------------------------------------------------------
    # CARD HOLDER NAME
    # --------------------------------------------------------

    card_holder_name = fake.name().upper()


    # --------------------------------------------------------
    # CREATED AT
    # --------------------------------------------------------

    created_at = issue_date


    # --------------------------------------------------------
    # CARD RECORD
    # --------------------------------------------------------

    card = {

        # card_id is AUTO_INCREMENT

        "account_id":
            account_id,

        "card_number":
            generate_card_number(),

        "card_holder_name":
            card_holder_name,

        "card_type":
            card_type,

        "card_network":
            card_network,

        "issue_date":
            issue_date,

        "expiry_date":
            expiry_date,

        "card_status":
            card_status,

        "daily_limit":
            daily_limit,

        "international_usage":
            international_usage,

        "contactless_enabled":
            contactless_enabled,

        "created_at":
            created_at,

        "block_reason":
            block_reason
    }

    cards.append(
        card
    )


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(
    cards
)


# ============================================================
# SAVE CSV
# ============================================================

output_file = (
    Path(__file__).parent /
    "cards.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print()
print("=" * 60)
print("CARD DATA GENERATION COMPLETED")
print("=" * 60)

print()

print("Total cards:")
print(len(df))

print()

print("Data shape:")
print(df.shape)

print()

print("Missing values:")
print(df.isnull().sum())

print()

print("Duplicate card numbers:")
print(
    df["card_number"]
    .duplicated()
    .sum()
)

print()

print("Card number lengths other than 16:")
print(
    (
        df["card_number"]
        .astype(str)
        .str.len() != 16
    ).sum()
)

print()

print("Account IDs outside range:")
print(
    (
        (df["account_id"] < 1) |
        (df["account_id"] > TOTAL_ACCOUNTS)
    ).sum()
)

print()

print("Card type distribution:")
print(
    df["card_type"]
    .value_counts()
)

print()

print("Card network distribution:")
print(
    df["card_network"]
    .value_counts()
)

print()

print("Card status distribution:")
print(
    df["card_status"]
    .value_counts()
)

print()

print("Cards with invalid expiry status:")

invalid_expiry_status = (
    (df["expiry_date"] < pd.Timestamp.now().date()) &
    (df["card_status"] != "Expired")
).sum()

print(
    invalid_expiry_status
)

print()

print("Blocked cards without block reason:")

blocked_without_reason = (
    (df["card_status"] == "Blocked") &
    (df["block_reason"].isnull())
).sum()

print(
    blocked_without_reason
)

print()

print("Hotlisted cards without block reason:")

hotlisted_without_reason = (
    (df["card_status"] == "Hotlisted") &
    (df["block_reason"].isnull())
).sum()

print(
    hotlisted_without_reason
)

print()

print("Active cards with block reason:")

active_with_reason = (
    (df["card_status"] == "Active") &
    (df["block_reason"].notnull())
).sum()

print(
    active_with_reason
)

print()

print("CSV file created:")
print(output_file)

print()

print("First 5 records:")
print(
    df.head()
)

print()

print("=" * 60)
print("CARDS CSV SAVED SUCCESSFULLY!")
print("=" * 60)