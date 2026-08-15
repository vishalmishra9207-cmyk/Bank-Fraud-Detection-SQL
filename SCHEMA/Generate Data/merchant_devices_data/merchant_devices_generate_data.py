from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# BASIC SETUP
# ============================================================

fake = Faker("en_IN")

TOTAL_DEVICES = 800

# ACTUAL DATABASE COUNTS
TOTAL_MERCHANTS = 300
TOTAL_BRANCHES = 20


# ============================================================
# DEVICE CONFIGURATION
# ============================================================

device_types = [
    "POS",
    "QR",
    "SoundBox",
    "mPOS"
]

device_type_weights = [
    40,
    30,
    20,
    10
]


device_statuses = [
    "Active",
    "Inactive",
    "Blocked",
    "Lost",
    "Damaged",
    "Under Maintenance"
]

device_status_weights = [
    78,
    5,
    3,
    3,
    4,
    7
]


# ============================================================
# DEVICE MODELS
# ============================================================

device_models = {

    "POS": [
        "Ingenico AXIUM DX8000",
        "Verifone V240m",
        "PAX A920",
        "PAX A80",
        "Castles VEGA3000"
    ],

    "QR": [
        "Bharat QR Stand",
        "Pine Labs QR",
        "Paytm QR",
        "PhonePe QR",
        "BharatPe QR"
    ],

    "SoundBox": [
        "Paytm Soundbox",
        "PhonePe SmartSpeaker",
        "BharatPe Soundbox",
        "Pine Labs Soundbox"
    ],

    "mPOS": [
        "PAX D180",
        "Pine Labs mPOS",
        "Mswipe mPOS",
        "Verifone mPOS"
    ]
}


# ============================================================
# FIRMWARE VERSIONS
# ============================================================

firmware_versions = [
    "1.0.1",
    "1.1.0",
    "1.2.3",
    "2.0.1",
    "2.1.0",
    "2.3.1",
    "3.0.0"
]


# ============================================================
# UNIQUE SERIAL NUMBERS
# ============================================================

used_serial_numbers = set()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_serial_number():

    while True:

        serial_number = (
            "MD"
            + str(
                random.randint(
                    1000000000,
                    9999999999
                )
            )
        )

        if serial_number not in used_serial_numbers:

            used_serial_numbers.add(
                serial_number
            )

            return serial_number


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

    total_days = (
        end_date - start_date
    ).days

    return (
        start_date
        + timedelta(
            days=random.randint(
                0,
                total_days
            )
        )
    )


def generate_warranty_expiry(issue_date):

    warranty_years = random.choice(
        [1, 2, 3]
    )

    return issue_date.replace(
        year=issue_date.year + warranty_years
    ).date()


def generate_last_service_date(issue_date):

    today = datetime.now().date()

    issue_date_only = issue_date.date()

    # 20% devices have no service record
    if random.random() < 0.20:

        return None

    max_days = (
        today - issue_date_only
    ).days

    if max_days < 30:

        return None

    service_date = (
        issue_date_only
        + timedelta(
            days=random.randint(
                30,
                max_days
            )
        )
    )

    if service_date > today:

        service_date = today

    return service_date


def generate_last_used_at(
    issue_date,
    device_status
):

    today = datetime.now()

    issue_date_only = issue_date

    available_days = (
        today - issue_date_only
    ).days

    if available_days <= 0:

        return None

    if device_status in [
        "Lost",
        "Damaged"
    ]:

        return (
            issue_date_only
            + timedelta(
                days=random.randint(
                    1,
                    available_days
                )
            )
        )

    elif device_status == "Inactive":

        return (
            issue_date_only
            + timedelta(
                days=random.randint(
                    1,
                    available_days
                )
            )
        )

    elif device_status == "Under Maintenance":

        return (
            today
            - timedelta(
                days=random.randint(
                    1,
                    30
                )
            )
        )

    else:

        return (
            today
            - timedelta(
                days=random.randint(
                    0,
                    30
                )
            )
        )


# ============================================================
# GENERATE MERCHANT DEVICES
# ============================================================

merchant_devices = []


for i in range(
    TOTAL_DEVICES
):

    # --------------------------------------------------------
    # VALID MERCHANT ID
    # --------------------------------------------------------

    merchant_id = random.randint(
        1,
        TOTAL_MERCHANTS
    )


    # --------------------------------------------------------
    # VALID BRANCH ID
    # --------------------------------------------------------

    branch_id = random.randint(
        1,
        TOTAL_BRANCHES
    )


    # --------------------------------------------------------
    # DEVICE TYPE
    # --------------------------------------------------------

    device_type = random.choices(
        device_types,
        weights=device_type_weights
    )[0]


    # --------------------------------------------------------
    # DEVICE MODEL
    # --------------------------------------------------------

    device_model = random.choice(
        device_models[device_type]
    )


    # --------------------------------------------------------
    # DEVICE STATUS
    # --------------------------------------------------------

    device_status = random.choices(
        device_statuses,
        weights=device_status_weights
    )[0]


    # --------------------------------------------------------
    # ISSUE DATE
    # --------------------------------------------------------

    device_issue_date = (
        generate_issue_date()
    )


    # --------------------------------------------------------
    # WARRANTY
    # --------------------------------------------------------

    warranty_expiry = (
        generate_warranty_expiry(
            device_issue_date
        )
    )


    # --------------------------------------------------------
    # LAST SERVICE DATE
    # --------------------------------------------------------

    last_service_date = (
        generate_last_service_date(
            device_issue_date
        )
    )


    # --------------------------------------------------------
    # LAST USED
    # --------------------------------------------------------

    last_used_at = (
        generate_last_used_at(
            device_issue_date,
            device_status
        )
    )


    # --------------------------------------------------------
    # FIRMWARE
    # --------------------------------------------------------

    firmware_version = random.choice(
        firmware_versions
    )


    # --------------------------------------------------------
    # SERIAL NUMBER
    # --------------------------------------------------------

    device_serial_number = (
        generate_serial_number()
    )


    # --------------------------------------------------------
    # CREATE RECORD
    # --------------------------------------------------------

    device = {

        "merchant_id":
            merchant_id,

        "device_serial_number":
            device_serial_number,

        "device_model":
            device_model,

        "merchant_device_type":
            device_type,

        "merchant_device_status":
            device_status,

        "device_issue_date":
            device_issue_date,

        "last_service_date":
            last_service_date,

        "branch_id":
            branch_id,

        "warranty_expiry":
            warranty_expiry,

        "last_used_at":
            last_used_at,

        "firmware_version":
            firmware_version
    }

    merchant_devices.append(
        device
    )


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    merchant_devices
)


# ============================================================
# SAVE CSV
# ============================================================

output_file = (
    Path(__file__).parent
    / "merchant_devices.csv"
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
print("MERCHANT DEVICE DATA GENERATION COMPLETED")
print("=" * 60)

print()

print("Total devices:")
print(len(df))

print()

print("Data shape:")
print(df.shape)

print()

print("Missing values:")
print(
    df.isnull().sum()
)

print()

print("Duplicate serial numbers:")
print(
    df["device_serial_number"]
    .duplicated()
    .sum()
)

print()

print("Invalid merchant IDs:")
print(
    (
        (df["merchant_id"] < 1)
        |
        (df["merchant_id"] > TOTAL_MERCHANTS)
    ).sum()
)

print()

print("Invalid branch IDs:")
print(
    (
        (df["branch_id"] < 1)
        |
        (df["branch_id"] > TOTAL_BRANCHES)
    ).sum()
)

print()

print("Device type distribution:")
print(
    df["merchant_device_type"]
    .value_counts()
)

print()

print("Device status distribution:")
print(
    df["merchant_device_status"]
    .value_counts()
)

print()

print("Warranty dates before issue dates:")

invalid_warranty = (
    pd.to_datetime(
        df["warranty_expiry"]
    )
    <
    pd.to_datetime(
        df["device_issue_date"]
    )
).sum()

print(
    invalid_warranty
)

print()

print("Service dates before issue dates:")

service_dates = pd.to_datetime(
    df["last_service_date"]
)

issue_dates = pd.to_datetime(
    df["device_issue_date"]
)

invalid_service = (
    service_dates.notna()
    &
    (service_dates < issue_dates)
).sum()

print(
    invalid_service
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
print("MERCHANT DEVICES CSV SAVED SUCCESSFULLY!")
print("=" * 60)