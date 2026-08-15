from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# --------------------------------------------------
# BASIC SETUP
# --------------------------------------------------

fake = Faker("en_IN")

TOTAL_DEVICES = 2000
TOTAL_CUSTOMERS = 1000


# --------------------------------------------------
# DEVICE CONFIGURATION
# --------------------------------------------------

device_types = [
    "Android",
    "iPhone",
    "Web"
]

device_type_weights = [
    55,
    30,
    15
]


android_models = [
    "Samsung Galaxy S24",
    "Samsung Galaxy A55",
    "Samsung Galaxy M35",
    "OnePlus 12",
    "OnePlus Nord CE 4",
    "Google Pixel 8",
    "Google Pixel 8a",
    "Redmi Note 13",
    "Nothing Phone 2",
    "Vivo V30"
]

iphone_models = [
    "iPhone 12",
    "iPhone 13",
    "iPhone 14",
    "iPhone 15",
    "iPhone 15 Pro",
    "iPhone 16",
    "iPhone 16 Pro"
]

web_models = [
    "Chrome Browser",
    "Microsoft Edge",
    "Firefox",
    "Safari"
]


android_os_versions = [
    "12",
    "13",
    "14",
    "15"
]

ios_versions = [
    "16",
    "17",
    "18"
]

browser_os = [
    "Windows 10",
    "Windows 11",
    "macOS",
    "Ubuntu"
]

app_versions = [
    "5.1.0",
    "5.2.0",
    "5.3.1",
    "5.4.0",
    "5.5.2",
    "6.0.0"
]


# --------------------------------------------------
# DEVICE STATUS
# --------------------------------------------------

device_statuses = [
    "Active",
    "Blocked",
    "Inactive"
]

device_status_weights = [
    92,
    3,
    5
]


# --------------------------------------------------
# REGISTERED FROM
# --------------------------------------------------

registered_from_options = [
    "Mobile App",
    "Internet Banking",
    "Branch"
]

registered_from_weights = [
    65,
    25,
    10
]


# --------------------------------------------------
# USED DEVICE IDENTIFIERS
# --------------------------------------------------

used_device_identifiers = set()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def generate_device_identifier():

    while True:

        identifier = (
            "DEV-"
            + fake.uuid4().replace("-", "").upper()
        )

        if identifier not in used_device_identifiers:

            used_device_identifiers.add(identifier)

            return identifier


def generate_ip_address():

    return fake.ipv4_private()


def generate_registered_at():

    start_date = datetime(
        2020,
        1,
        1
    )

    end_date = datetime(
        2026,
        8,
        15
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


def generate_last_login(
    registered_at,
    device_status
):

    if device_status == "Blocked":

        # Blocked devices may have a past login
        max_date = datetime.now()

    else:

        max_date = datetime.now()

    if registered_at > max_date:

        return registered_at

    days = (
        max_date - registered_at
    ).days

    if days <= 0:

        return registered_at

    return (
        registered_at +
        timedelta(
            days=random.randint(
                0,
                days
            ),
            hours=random.randint(
                0,
                23
            ),
            minutes=random.randint(
                0,
                59
            )
        )
    )


def generate_device_details(device_type):

    if device_type == "Android":

        device_model = random.choice(
            android_models
        )

        operating_system = "Android"

        os_version = random.choice(
            android_os_versions
        )

    elif device_type == "iPhone":

        device_model = random.choice(
            iphone_models
        )

        operating_system = "iOS"

        os_version = random.choice(
            ios_versions
        )

    else:

        device_model = random.choice(
            web_models
        )

        operating_system = random.choice(
            browser_os
        )

        os_version = random.choice(
            [
                "10",
                "11",
                "12",
                "13",
                "14"
            ]
        )

    return (
        device_model,
        operating_system,
        os_version
    )


# --------------------------------------------------
# GENERATE DEVICES
# --------------------------------------------------

devices = []


for i in range(
    1,
    TOTAL_DEVICES + 1
):

    # ----------------------------------------------
    # CUSTOMER
    # ----------------------------------------------

    customer_id = random.randint(
        1,
        TOTAL_CUSTOMERS
    )


    # ----------------------------------------------
    # DEVICE TYPE
    # ----------------------------------------------

    device_type = random.choices(
        device_types,
        weights=device_type_weights
    )[0]


    # ----------------------------------------------
    # DEVICE DETAILS
    # ----------------------------------------------

    (
        device_model,
        operating_system,
        os_version
    ) = generate_device_details(
        device_type
    )


    # ----------------------------------------------
    # DEVICE STATUS
    # ----------------------------------------------

    device_status = random.choices(
        device_statuses,
        weights=device_status_weights
    )[0]


    # ----------------------------------------------
    # TRUSTED STATUS
    # ----------------------------------------------

    if device_status == "Blocked":

        is_trusted = 0

    else:

        is_trusted = random.choices(
            [1, 0],
            weights=[90, 10]
        )[0]


    # ----------------------------------------------
    # REGISTERED FROM
    # ----------------------------------------------

    registered_from = random.choices(
        registered_from_options,
        weights=registered_from_weights
    )[0]


    # ----------------------------------------------
    # REGISTERED DATE
    # ----------------------------------------------

    registered_at = generate_registered_at()


    # ----------------------------------------------
    # LAST LOGIN
    # ----------------------------------------------

    last_login = generate_last_login(
        registered_at,
        device_status
    )


    # ----------------------------------------------
    # FAILED LOGIN ATTEMPTS
    # ----------------------------------------------

    if device_status == "Blocked":

        failed_login_attempts = random.randint(
            3,
            10
        )

    else:

        failed_login_attempts = random.choices(
            [
                0,
                1,
                2,
                3
            ],
            weights=[
                85,
                8,
                5,
                2
            ]
        )[0]


    # ----------------------------------------------
    # BLOCKED AT
    # ----------------------------------------------

    blocked_at = None

    if device_status == "Blocked":

        blocked_at = (
            last_login +
            timedelta(
                minutes=random.randint(
                    5,
                    120
                )
            )
        )

        if blocked_at > datetime.now():

            blocked_at = datetime.now()


    # ----------------------------------------------
    # DEVICE RECORD
    # ----------------------------------------------

    device = {

        # device_id is AUTO_INCREMENT

        "customer_id":
            customer_id,

        "device_identifier":
            generate_device_identifier(),

        "device_name":
            f"{device_model}",

        "device_type":
            device_type,

        "device_model":
            device_model,

        "operating_system":
            operating_system,

        "os_version":
            os_version,

        "app_version":
            random.choice(
                app_versions
            ),

        "device_status":
            device_status,

        "is_trusted":
            is_trusted,

        "last_ip_address":
            generate_ip_address(),

        "last_login_city":
            fake.city(),

        "last_login":
            last_login,

        "registered_at":
            registered_at,

        "registered_from":
            registered_from,

        "failed_login_attempts":
            failed_login_attempts,

        "blocked_at":
            blocked_at
    }

    devices.append(
        device
    )


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(
    devices
)


# --------------------------------------------------
# SAVE CSV
# --------------------------------------------------

output_file = (
    Path(__file__).parent /
    "devices.csv"
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
print("DEVICE DATA GENERATION COMPLETED")
print("=" * 60)

print()

print("Total devices:")
print(len(df))

print()

print("Data shape:")
print(df.shape)

print()

print("Missing values:")
print(df.isnull().sum())

print()

print("Duplicate device identifiers:")
print(
    df["device_identifier"]
    .duplicated()
    .sum()
)

print()

print("Customer IDs outside range:")
print(
    (
        (df["customer_id"] < 1) |
        (df["customer_id"] > 1000)
    ).sum()
)

print()

print("Device type distribution:")
print(
    df["device_type"]
    .value_counts()
)

print()

print("Device status distribution:")
print(
    df["device_status"]
    .value_counts()
)

print()

print("Registered from distribution:")
print(
    df["registered_from"]
    .value_counts()
)

print()

print("Blocked devices without blocked_at:")
print(
    (
        (df["device_status"] == "Blocked") &
        (df["blocked_at"].isnull())
    ).sum()
)

print()

print("Non-blocked devices with blocked_at:")
print(
    (
        (df["device_status"] != "Blocked") &
        (df["blocked_at"].notnull())
    ).sum()
)

print()

print("Blocked devices marked trusted:")
print(
    (
        (df["device_status"] == "Blocked") &
        (df["is_trusted"] == 1)
    ).sum()
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
print("DEVICE CSV SAVED SUCCESSFULLY!")
print("=" * 60)