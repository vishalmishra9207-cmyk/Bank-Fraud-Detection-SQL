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

TOTAL_LOGIN_RECORDS = 10000

TOTAL_CUSTOMERS = 1000
TOTAL_DEVICES = 2000

TODAY = datetime(2026, 8, 17, 23, 59, 59)

START_DATE = datetime(2025, 1, 1, 0, 0, 0)


# ============================================================
# CONFIGURATION
# ============================================================

login_statuses = [
    "Success",
    "Failed",
    "Blocked"
]

login_status_weights = [
    88,
    9,
    3
]


login_methods = [
    "Password",
    "OTP",
    "Fingerprint",
    "Face ID"
]

login_method_weights = [
    35,
    30,
    20,
    15
]


logout_reasons = [
    "User Logout",
    "Session Timeout",
    "Forced Logout"
]

logout_reason_weights = [
    55,
    35,
    10
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_datetime(start_date, end_date):

    time_difference = (
        end_date - start_date
    )

    random_seconds = random.randint(
        0,
        int(time_difference.total_seconds())
    )

    return (
        start_date
        + timedelta(
            seconds=random_seconds
        )
    )


def generate_ip_address():

    return fake.ipv4()


def generate_session_id():

    return (
        "SES_"
        + uuid.uuid4().hex.upper()
    )


def generate_location():

    city = fake.city()

    return city


# ============================================================
# GENERATE LOGIN DATA
# ============================================================

login_records = []

used_session_ids = set()


for i in range(
    TOTAL_LOGIN_RECORDS
):

    # --------------------------------------------------------
    # CUSTOMER
    # --------------------------------------------------------

    customer_id = random.randint(
        1,
        TOTAL_CUSTOMERS
    )


    # --------------------------------------------------------
    # DEVICE
    # --------------------------------------------------------

    # Device is nullable in the table.
    # Most logins will have a device,
    # but a small percentage will be NULL.

    if random.random() < 0.05:

        device_id = None

    else:

        device_id = random.randint(
            1,
            TOTAL_DEVICES
        )


    # --------------------------------------------------------
    # LOGIN STATUS
    # --------------------------------------------------------

    login_status = random.choices(
        login_statuses,
        weights=login_status_weights
    )[0]


    # --------------------------------------------------------
    # LOGIN METHOD
    # --------------------------------------------------------

    login_method = random.choices(
        login_methods,
        weights=login_method_weights
    )[0]


    # --------------------------------------------------------
    # LOGIN TIME
    # --------------------------------------------------------

    login_time = random_datetime(
        START_DATE,
        TODAY
    )


    # --------------------------------------------------------
    # FAILED ATTEMPTS
    # --------------------------------------------------------

    if login_status == "Success":

        failed_attempts = random.choices(
            [0, 1, 2],
            weights=[95, 4, 1]
        )[0]

    elif login_status == "Failed":

        failed_attempts = random.randint(
            1,
            4
        )

    else:

        failed_attempts = random.randint(
            3,
            6
        )


    # --------------------------------------------------------
    # LOGOUT TIME / LOGOUT REASON
    # --------------------------------------------------------

    if login_status == "Success":

        # Successful login normally creates a session
        logout_time = (
            login_time
            + timedelta(
                minutes=random.randint(
                    5,
                    720
                )
            )
        )

        # Don't allow logout after current date
        if logout_time > TODAY:

            logout_time = TODAY

        logout_reason = random.choices(
            logout_reasons,
            weights=logout_reason_weights
        )[0]

    else:

        logout_time = None
        logout_reason = None


    # --------------------------------------------------------
    # IP ADDRESS
    # --------------------------------------------------------

    ip_address = generate_ip_address()


    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    location = generate_location()


    # --------------------------------------------------------
    # CITY / STATE / COUNTRY
    # --------------------------------------------------------

    login_city = fake.city()

    login_state = fake.state()

    login_country = "India"


    # --------------------------------------------------------
    # SESSION ID
    # --------------------------------------------------------

    if login_status == "Success":

        while True:

            session_id = generate_session_id()

            if session_id not in used_session_ids:

                used_session_ids.add(
                    session_id
                )

                break

    else:

        # Failed / blocked attempts may not
        # establish a session.

        if random.random() < 0.30:

            while True:

                session_id = generate_session_id()

                if session_id not in used_session_ids:

                    used_session_ids.add(
                        session_id
                    )

                    break

        else:

            session_id = None


    # --------------------------------------------------------
    # SUSPICIOUS LOGIN
    # --------------------------------------------------------

    if login_status == "Blocked":

        is_suspicious = 1

    elif login_status == "Failed":

        is_suspicious = random.choices(
            [0, 1],
            weights=[70, 30]
        )[0]

    else:

        is_suspicious = random.choices(
            [0, 1],
            weights=[97, 3]
        )[0]


    # --------------------------------------------------------
    # RECORD
    # --------------------------------------------------------

    record = {

        "customer_id":
            customer_id,

        "device_id":
            device_id,

        "login_time":
            login_time,

        "logout_time":
            logout_time,

        "login_status":
            login_status,

        "login_method":
            login_method,

        "ip_address":
            ip_address,

        "location":
            location,

        "failed_attempts":
            failed_attempts,

        "session_id":
            session_id,

        "login_city":
            login_city,

        "login_state":
            login_state,

        "login_country":
            login_country,

        "logout_reason":
            logout_reason,

        "is_suspicious":
            is_suspicious
    }

    login_records.append(
        record
    )


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    login_records
)


# ============================================================
# SAVE CSV
# ============================================================

output_file = (
    Path(__file__).parent
    / "login_history.csv"
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
print("LOGIN HISTORY DATA GENERATION COMPLETED")
print("=" * 65)

print()

print("Total login records:")
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

print("Duplicate session IDs:")

duplicate_sessions = (
    df["session_id"]
    .dropna()
    .duplicated()
    .sum()
)

print(
    duplicate_sessions
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

print("Invalid device IDs:")

invalid_devices = (
    df["device_id"].notna()
    &
    (
        (
            df["device_id"] < 1
        )
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

print("Invalid logout times:")

invalid_logout_times = (
    df["logout_time"].notna()
    &
    (
        pd.to_datetime(
            df["logout_time"]
        )
        <
        pd.to_datetime(
            df["login_time"]
        )
    )
).sum()

print(
    invalid_logout_times
)

print()

print("Successful logins without logout reason:")

success_without_logout_reason = (
    (
        df["login_status"]
        == "Success"
    )
    &
    (
        df["logout_reason"]
        .isna()
    )
).sum()

print(
    success_without_logout_reason
)

print()

print("Failed/Blocked logins with logout reason:")

failed_with_logout_reason = (
    (
        df["login_status"]
        .isin(
            [
                "Failed",
                "Blocked"
            ]
        )
    )
    &
    (
        df["logout_reason"]
        .notna()
    )
).sum()

print(
    failed_with_logout_reason
)

print()

print("Blocked logins not marked suspicious:")

blocked_not_suspicious = (
    (
        df["login_status"]
        == "Blocked"
    )
    &
    (
        df["is_suspicious"]
        != 1
    )
).sum()

print(
    blocked_not_suspicious
)

print()

print("Negative failed attempts:")

negative_failed_attempts = (
    df["failed_attempts"] < 0
).sum()

print(
    negative_failed_attempts
)

print()

print("Login status distribution:")
print(
    df["login_status"]
    .value_counts()
)

print()

print("Login method distribution:")
print(
    df["login_method"]
    .value_counts()
)

print()

print("Suspicious login distribution:")
print(
    df["is_suspicious"]
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
print("LOGIN HISTORY CSV SAVED SUCCESSFULLY!")
print("=" * 65)