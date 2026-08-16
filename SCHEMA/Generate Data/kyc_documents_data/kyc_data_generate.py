import pandas as pd
import random
import string
from faker import Faker
from datetime import date, timedelta
from pathlib import Path


# ============================================================
# SETUP
# ============================================================

fake = Faker("en_IN")

TOTAL_KYC_RECORDS = 2000

# Actual database counts
TOTAL_CUSTOMERS = 1000
TOTAL_EMPLOYEES = 100

TODAY = date(2026, 8, 15)


# ============================================================
# CONFIGURATION
# ============================================================

document_types = [
    "Aadhaar",
    "PAN",
    "Passport",
    "Driving License",
    "Voter ID"
]

document_type_weights = [
    40,
    25,
    10,
    15,
    10
]


verification_statuses = [
    "Verified",
    "Pending",
    "Rejected",
    "Failed"
]

verification_status_weights = [
    75,
    12,
    8,
    5
]


uploaded_via_options = [
    "Branch",
    "Mobile App",
    "Internet Banking"
]

uploaded_via_weights = [
    25,
    60,
    15
]


rejection_reasons = [
    "Document image unclear",
    "Document details mismatch",
    "Invalid document",
    "Document expired",
    "Verification failed",
    "Incorrect document information"
]


# ============================================================
# DOCUMENT NUMBER GENERATOR
# ============================================================

used_document_numbers = set()


def generate_document_number(document_type):

    while True:

        if document_type == "Aadhaar":

            document_number = str(
                fake.random_number(
                    digits=12,
                    fix_len=True
                )
            )

        elif document_type == "PAN":

            first_five = "".join(
                random.choices(
                    string.ascii_uppercase,
                    k=5
                )
            )

            four_digits = str(
                fake.random_number(
                    digits=4,
                    fix_len=True
                )
            )

            last_letter = random.choice(
                string.ascii_uppercase
            )

            document_number = (
                first_five
                + four_digits
                + last_letter
            )

        elif document_type == "Passport":

            document_number = (
                random.choice(
                    string.ascii_uppercase
                )
                + str(
                    fake.random_number(
                        digits=7,
                        fix_len=True
                    )
                )
            )

        elif document_type == "Driving License":

            document_number = (
                "DL"
                + str(
                    fake.random_number(
                        digits=12,
                        fix_len=True
                    )
                )
            )

        else:

            document_number = (
                "VID"
                + str(
                    fake.random_number(
                        digits=12,
                        fix_len=True
                    )
                )
            )

        if document_number not in used_document_numbers:

            used_document_numbers.add(
                document_number
            )

            return document_number


# ============================================================
# ISSUE DATE
# ============================================================

def generate_issue_date():

    start_date = date(
        2010,
        1,
        1
    )

    days_range = (
        TODAY - start_date
    ).days

    return (
        start_date
        + timedelta(
            days=random.randint(
                0,
                days_range
            )
        )
    )


# ============================================================
# EXPIRY DATE
# ============================================================

def generate_expiry_date(
    issue_date,
    document_type
):

    if document_type in [
        "Aadhaar",
        "PAN"
    ]:

        return None

    elif document_type == "Passport":

        years = random.choice(
            [5, 10]
        )

    elif document_type == "Driving License":

        years = random.choice(
            [5, 10, 20]
        )

    else:

        years = random.choice(
            [5, 10]
        )

    try:

        expiry_date = issue_date.replace(
            year=issue_date.year + years
        )

    except ValueError:

        expiry_date = issue_date.replace(
            year=issue_date.year + years,
            day=28
        )

    return expiry_date


# ============================================================
# GENERATE UNIQUE CUSTOMER + DOCUMENT TYPE PAIRS
# ============================================================

possible_pairs = [
    (
        customer_id,
        document_type
    )

    for customer_id in range(
        1,
        TOTAL_CUSTOMERS + 1
    )

    for document_type in document_types
]


selected_pairs = random.sample(
    possible_pairs,
    TOTAL_KYC_RECORDS
)


# ============================================================
# GENERATE KYC DATA
# ============================================================

kyc_records = []


for customer_id, document_type in selected_pairs:

    # --------------------------------------------------------
    # ISSUE DATE
    # --------------------------------------------------------

    issue_date = generate_issue_date()


    # --------------------------------------------------------
    # EXPIRY DATE
    # --------------------------------------------------------

    expiry_date = generate_expiry_date(
        issue_date,
        document_type
    )


    # --------------------------------------------------------
    # VERIFICATION STATUS
    # --------------------------------------------------------

    verification_status = random.choices(
        verification_statuses,
        weights=verification_status_weights
    )[0]


    # --------------------------------------------------------
    # VERIFIED BY / VERIFICATION DATE
    # --------------------------------------------------------

    if verification_status == "Verified":

        verified_by = random.randint(
            1,
            TOTAL_EMPLOYEES
        )

        verification_date = (
            issue_date
            + timedelta(
                days=random.randint(
                    1,
                    30
                )
            )
        )

        if verification_date > TODAY:

            verification_date = TODAY

        rejection_reason = None


    elif verification_status in [
        "Rejected",
        "Failed"
    ]:

        verified_by = random.randint(
            1,
            TOTAL_EMPLOYEES
        )

        verification_date = (
            issue_date
            + timedelta(
                days=random.randint(
                    1,
                    30
                )
            )
        )

        if verification_date > TODAY:

            verification_date = TODAY

        rejection_reason = random.choice(
            rejection_reasons
        )


    else:

        verified_by = None
        verification_date = None
        rejection_reason = None


    # --------------------------------------------------------
    # DOCUMENT EXPIRED
    # --------------------------------------------------------

    if (
        expiry_date is not None
        and expiry_date < TODAY
    ):

        document_expired = 1

    else:

        document_expired = 0


    # --------------------------------------------------------
    # UPLOADED AT
    # --------------------------------------------------------

    uploaded_at = (
        issue_date
        + timedelta(
            days=random.randint(
                0,
                30
            )
        )
    )

    if uploaded_at > TODAY:

        uploaded_at = TODAY


    # --------------------------------------------------------
    # UPLOADED VIA
    # --------------------------------------------------------

    uploaded_via = random.choices(
        uploaded_via_options,
        weights=uploaded_via_weights
    )[0]


    # --------------------------------------------------------
    # DOCUMENT PATH
    # --------------------------------------------------------

    document_path = (
        "documents/kyc/"
        f"CUST_{customer_id}/"
        f"{document_type.replace(' ', '_')}/"
        f"{customer_id}_{random.randint(100000, 999999)}.pdf"
    )


    # --------------------------------------------------------
    # RECORD
    # --------------------------------------------------------

    record = {

        "customer_id":
            customer_id,

        "document_type":
            document_type,

        "document_number":
            generate_document_number(
                document_type
            ),

        "issue_date":
            issue_date,

        "expiry_date":
            expiry_date,

        "verification_status":
            verification_status,

        "verified_by":
            verified_by,

        "verification_date":
            verification_date,

        "uploaded_at":
            uploaded_at,

        "document_expired":
            document_expired,

        "uploaded_via":
            uploaded_via,

        "rejection_reason":
            rejection_reason,

        "document_path":
            document_path
    }

    kyc_records.append(
        record
    )


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    kyc_records
)


# ============================================================
# SAVE CSV
# ============================================================

output_file = (
    Path(__file__).parent
    / "kyc_documents.csv"
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
print("KYC DOCUMENT DATA GENERATION COMPLETED")
print("=" * 65)

print()

print("Total KYC records:")
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

print("Duplicate document numbers:")
print(
    df["document_number"]
    .duplicated()
    .sum()
)

print()

print("Duplicate customer + document type combinations:")

duplicate_pairs = (
    df[
        [
            "customer_id",
            "document_type"
        ]
    ]
    .duplicated()
    .sum()
)

print(
    duplicate_pairs
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

print("Invalid employee IDs:")

invalid_employees = (
    df["verified_by"].notna()
    &
    (
        (
            df["verified_by"] < 1
        )
        |
        (
            df["verified_by"]
            > TOTAL_EMPLOYEES
        )
    )
).sum()

print(
    invalid_employees
)

print()

print("Pending records with verified_by:")

pending_with_employee = (
    (
        df["verification_status"]
        == "Pending"
    )
    &
    (
        df["verified_by"].notna()
    )
).sum()

print(
    pending_with_employee
)

print()

print("Verified records without verified_by:")

verified_without_employee = (
    (
        df["verification_status"]
        == "Verified"
    )
    &
    (
        df["verified_by"].isna()
    )
).sum()

print(
    verified_without_employee
)

print()

print(
    "Rejected/Failed records "
    "without rejection reason:"
)

rejected_without_reason = (
    (
        df["verification_status"]
        .isin(
            [
                "Rejected",
                "Failed"
            ]
        )
    )
    &
    (
        df["rejection_reason"].isna()
    )
).sum()

print(
    rejected_without_reason
)

print()

print("Invalid expired flag:")

invalid_expired_flag = (
    (
        df["expiry_date"].notna()
    )
    &
    (
        (
            df["expiry_date"] < TODAY
        )
        !=
        (
            df["document_expired"] == 1
        )
    )
).sum()

print(
    invalid_expired_flag
)

print()

print("Document type distribution:")
print(
    df["document_type"]
    .value_counts()
)

print()

print("Verification status distribution:")
print(
    df["verification_status"]
    .value_counts()
)

print()

print("Uploaded via distribution:")
print(
    df["uploaded_via"]
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
print("KYC DOCUMENT CSV SAVED SUCCESSFULLY!")
print("=" * 65)