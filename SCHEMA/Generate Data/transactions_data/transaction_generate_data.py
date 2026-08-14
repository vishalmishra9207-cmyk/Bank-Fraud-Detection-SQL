from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# --------------------------------------------------
# BASIC SETUP
# --------------------------------------------------

fake = Faker("en_IN")

TOTAL_MERCHANTS = 300


# --------------------------------------------------
# MERCHANT CATEGORIES
# --------------------------------------------------

merchant_categories = [
    "Retail",
    "Grocery",
    "Restaurant",
    "Fuel",
    "Healthcare",
    "E-commerce",
    "Travel",
    "Entertainment",
    "Education",
    "Utilities"
]


# --------------------------------------------------
# MERCHANT TYPES
# --------------------------------------------------

merchant_types = [
    "Individual",
    "Business",
    "Corporate"
]


# --------------------------------------------------
# MERCHANT STATUS
# --------------------------------------------------

merchant_statuses = [
    "Active",
    "Inactive",
    "Suspended",
    "Blocked"
]


# --------------------------------------------------
# RISK LEVELS
# --------------------------------------------------

risk_levels = [
    "Low",
    "Medium",
    "High"
]


# --------------------------------------------------
# USED VALUES
# --------------------------------------------------

used_merchant_codes = set()
used_contact_numbers = set()
used_emails = set()
used_gst_numbers = set()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def generate_merchant_code(number):

    code = f"MER{number:05d}"

    while code in used_merchant_codes:

        number += 1

        code = f"MER{number:05d}"

    used_merchant_codes.add(code)

    return code


def generate_contact_number():

    while True:

        number = str(
            random.randint(
                7000000000,
                9999999999
            )
        )

        if number not in used_contact_numbers:

            used_contact_numbers.add(number)

            return number


def generate_email(merchant_name, number):

    clean_name = (
        merchant_name
        .lower()
        .replace(" ", "")
        .replace(".", "")
        .replace(",", "")
        .replace("&", "")
    )

    email = (
        f"{clean_name}{number}"
        "@merchant.com"
    )

    while email in used_emails:

        number += 1

        email = (
            f"{clean_name}{number}"
            "@merchant.com"
        )

    used_emails.add(email)

    return email


def generate_gst_number():

    while True:

        gst = (
            f"{random.randint(10,99)}"
            f"{random.randint(100000000,999999999)}"
            f"1"
            f"Z"
            f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')}"
        )

        if gst not in used_gst_numbers:

            used_gst_numbers.add(gst)

            return gst


def generate_created_at():

    start_date = datetime(
        2018,
        1,
        1
    )

    end_date = datetime(
        2026,
        8,
        1
    )

    days = (
        end_date - start_date
    ).days

    random_date = (
        start_date +
        timedelta(
            days=random.randint(
                0,
                days
            )
        )
    )

    return random_date


# --------------------------------------------------
# WEIGHTS
# --------------------------------------------------

category_weights = [
    15,  # Retail
    15,  # Grocery
    12,  # Restaurant
    8,   # Fuel
    10,  # Healthcare
    12,  # E-commerce
    8,   # Travel
    6,   # Entertainment
    6,   # Education
    8    # Utilities
]


merchant_type_weights = [
    20,  # Individual
    60,  # Business
    20   # Corporate
]


status_weights = [
    92,  # Active
    4,   # Inactive
    2,   # Suspended
    2    # Blocked
]


risk_weights = [
    70,  # Low
    25,  # Medium
    5    # High
]


# --------------------------------------------------
# GENERATE MERCHANTS
# --------------------------------------------------

merchants = []


for i in range(
    1,
    TOTAL_MERCHANTS + 1
):

    # ----------------------------------------------
    # MERCHANT NAME
    # ----------------------------------------------

    merchant_name = fake.company()

    # ----------------------------------------------
    # CATEGORY
    # ----------------------------------------------

    merchant_category = random.choices(
        merchant_categories,
        weights=category_weights
    )[0]

    # ----------------------------------------------
    # TYPE
    # ----------------------------------------------

    merchant_type = random.choices(
        merchant_types,
        weights=merchant_type_weights
    )[0]

    # ----------------------------------------------
    # STATUS
    # ----------------------------------------------

    merchant_status = random.choices(
        merchant_statuses,
        weights=status_weights
    )[0]

    # ----------------------------------------------
    # RISK LEVEL
    # ----------------------------------------------

    risk_level = random.choices(
        risk_levels,
        weights=risk_weights
    )[0]

    # ----------------------------------------------
    # CONTACT
    # ----------------------------------------------

    contact_number = (
        generate_contact_number()
    )

    # ----------------------------------------------
    # EMAIL
    # ----------------------------------------------

    merchant_email = generate_email(
        merchant_name,
        i
    )

    # ----------------------------------------------
    # GST
    # ----------------------------------------------

    gst_number = generate_gst_number()

    # ----------------------------------------------
    # MERCHANT RECORD
    # ----------------------------------------------

    merchant = {

        # merchant_id is AUTO_INCREMENT

        "merchant_code":
            generate_merchant_code(i),

        "merchant_name":
            merchant_name,

        "merchant_category":
            merchant_category,

        "merchant_type":
            merchant_type,

        "contact_number":
            contact_number,

        "merchant_email":
            merchant_email,

        "gst_number":
            gst_number,

        "building_no":
            str(
                random.randint(
                    1,
                    999
                )
            ),

        "street":
            fake.street_name(),

        "city":
            fake.city(),

        "state":
            fake.state(),

        "pincode":
            fake.postcode()[:10],

        "country":
            "India",

        "merchant_status":
            merchant_status,

        "created_at":
            generate_created_at(),

        "risk_level":
            risk_level
    }

    merchants.append(
        merchant
    )


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(
    merchants
)


# --------------------------------------------------
# SAVE CSV
# --------------------------------------------------

output_file = (
    Path(__file__).parent /
    "merchants.csv"
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
print("MERCHANT DATA GENERATION COMPLETED")
print("=" * 60)

print()

print("Total merchants:")
print(len(df))

print()

print("Data shape:")
print(df.shape)

print()

print("Missing values:")
print(df.isnull().sum())

print()

print("Duplicate merchant codes:")
print(
    df["merchant_code"]
    .duplicated()
    .sum()
)

print()

print("Duplicate contact numbers:")
print(
    df["contact_number"]
    .duplicated()
    .sum()
)

print()

print("Duplicate emails:")
print(
    df["merchant_email"]
    .duplicated()
    .sum()
)

print()

print("Duplicate GST numbers:")
print(
    df["gst_number"]
    .duplicated()
    .sum()
)

print()

print("Merchant category distribution:")
print(
    df["merchant_category"]
    .value_counts()
)

print()

print("Merchant type distribution:")
print(
    df["merchant_type"]
    .value_counts()
)

print()

print("Merchant status distribution:")
print(
    df["merchant_status"]
    .value_counts()
)

print()

print("Risk level distribution:")
print(
    df["risk_level"]
    .value_counts()
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
print("MERCHANT CSV SAVED SUCCESSFULLY!")
print("=" * 60)