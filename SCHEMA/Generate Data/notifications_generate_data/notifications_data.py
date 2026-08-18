import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

import mysql.connector


# ============================================================
# SETTINGS
# ============================================================

TOTAL_NOTIFICATIONS = 10000

OUTPUT_FILE = Path(__file__).parent / "notifications.csv"


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
# FETCH CUSTOMERS
# ============================================================

cursor.execute("""
    SELECT customer_id
    FROM customers
""")

customer_ids = [
    row[0]
    for row in cursor.fetchall()
]

if not customer_ids:
    print("ERROR: No customers found!")

    cursor.close()
    conn.close()

    exit()


print()
print(f"Valid customers found: {len(customer_ids)}")


# ============================================================
# FETCH TRANSACTIONS
# ============================================================

cursor.execute("""
    SELECT transaction_id
    FROM transactions
""")

transaction_ids = [
    row[0]
    for row in cursor.fetchall()
]


# ============================================================
# FETCH FRAUD ALERTS
# ============================================================

cursor.execute("""
    SELECT fraud_alert_id
    FROM fraud_alerts
""")

fraud_alert_ids = [
    row[0]
    for row in cursor.fetchall()
]


# ============================================================
# FETCH KYC DOCUMENTS
# ============================================================

cursor.execute("""
    SELECT kyc_id
    FROM kyc_documents
""")

kyc_ids = [
    row[0]
    for row in cursor.fetchall()
]


# ============================================================
# FETCH LOANS
# ============================================================

cursor.execute("""
    SELECT loan_id
    FROM loans
""")

loan_ids = [
    row[0]
    for row in cursor.fetchall()
]


# ============================================================
# NOTIFICATION CONFIGURATION
# ============================================================

notification_config = {

    "Debit": {
        "titles": [
            "Debit Alert",
            "Money Debited",
            "Transaction Debit Alert"
        ],
        "channels": [
            "SMS",
            "WhatsApp",
            "App Notification",
            "E-mail"
        ]
    },

    "Credit": {
        "titles": [
            "Credit Alert",
            "Money Credited",
            "Transaction Credit Alert"
        ],
        "channels": [
            "SMS",
            "WhatsApp",
            "App Notification",
            "E-mail"
        ]
    },

    "OTP": {
        "titles": [
            "OTP Verification",
            "One Time Password",
            "Login OTP"
        ],
        "channels": [
            "SMS",
            "WhatsApp",
            "App Notification"
        ]
    },

    "Fraud Alert": {
        "titles": [
            "Fraud Alert",
            "Suspicious Transaction Detected",
            "Security Alert"
        ],
        "channels": [
            "SMS",
            "WhatsApp",
            "App Notification",
            "E-mail"
        ]
    },

    "KYC": {
        "titles": [
            "KYC Update",
            "KYC Verification Required",
            "KYC Status Update"
        ],
        "channels": [
            "SMS",
            "App Notification",
            "E-mail"
        ]
    },

    "Promotional": {
        "titles": [
            "Special Offer",
            "Banking Offer",
            "Exclusive Offer",
            "New Banking Benefits"
        ],
        "channels": [
            "SMS",
            "WhatsApp",
            "App Notification",
            "E-mail"
        ]
    },

    "Loan Update": {
        "titles": [
            "Loan Update",
            "Loan Application Update",
            "Loan Status Update",
            "EMI Reminder"
        ],
        "channels": [
            "SMS",
            "WhatsApp",
            "App Notification",
            "E-mail"
        ]
    }
}


notification_types = list(
    notification_config.keys()
)


# ============================================================
# MESSAGE GENERATOR
# ============================================================

def generate_message(notification_type, title):

    messages = {

        "Debit":
            f"{title}: A debit transaction has been processed from your bank account.",

        "Credit":
            f"{title}: An amount has been credited to your bank account.",

        "OTP":
            "Your one-time password is required to complete the requested banking activity.",

        "Fraud Alert":
            "Suspicious activity has been detected on your account. Please review the transaction immediately.",

        "KYC":
            "Please review your KYC status and complete the required verification if necessary.",

        "Promotional":
            "Enjoy exclusive banking offers and benefits available for a limited period.",

        "Loan Update":
            "There is an update regarding your loan application or repayment schedule."
    }

    return messages[notification_type]


# ============================================================
# GENERATE NOTIFICATIONS
# ============================================================

notification_rows = []

start_date = datetime.now() - timedelta(days=365)

for notification_number in range(
    1,
    TOTAL_NOTIFICATIONS + 1
):

    # --------------------------------------------------------
    # CUSTOMER
    # --------------------------------------------------------

    customer_id = random.choice(
        customer_ids
    )

    # --------------------------------------------------------
    # NOTIFICATION TYPE
    # --------------------------------------------------------

    notification_type = random.choices(
        notification_types,
        weights=[
            20,  # Debit
            18,  # Credit
            15,  # OTP
            10,  # Fraud Alert
            10,  # KYC
            17,  # Promotional
            10   # Loan Update
        ],
        k=1
    )[0]

    config = notification_config[
        notification_type
    ]

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = random.choice(
        config["titles"]
    )

    # --------------------------------------------------------
    # MESSAGE
    # --------------------------------------------------------

    message = generate_message(
        notification_type,
        title
    )

    # --------------------------------------------------------
    # CHANNEL
    # --------------------------------------------------------

    channel = random.choice(
        config["channels"]
    )

    # --------------------------------------------------------
    # SENT TIME
    # --------------------------------------------------------

    sent_time = start_date + timedelta(
        seconds=random.randint(
            0,
            int(
                (
                    datetime.now()
                    - start_date
                ).total_seconds()
            )
        )
    )

    # --------------------------------------------------------
    # DELIVERY STATUS
    # --------------------------------------------------------

    delivery_status = random.choices(
        [
            "Pending",
            "Delivered",
            "Failed"
        ],
        weights=[
            8,
            87,
            5
        ],
        k=1
    )[0]

    # --------------------------------------------------------
    # READ STATUS
    # --------------------------------------------------------

    if delivery_status == "Failed":

        read_status = "Unread"

    else:

        read_status = random.choices(
            [
                "Read",
                "Unread"
            ],
            weights=[
                70,
                30
            ],
            k=1
        )[0]

    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    if notification_type == "Fraud Alert":

        priority = random.choices(
            [
                "High",
                "Critical",
                "Medium"
            ],
            weights=[
                45,
                35,
                20
            ],
            k=1
        )[0]

    elif notification_type in [
        "OTP",
        "Debit",
        "Credit"
    ]:

        priority = random.choices(
            [
                "Low",
                "Medium",
                "High"
            ],
            weights=[
                15,
                65,
                20
            ],
            k=1
        )[0]

    else:

        priority = random.choices(
            [
                "Low",
                "Medium",
                "High"
            ],
            weights=[
                40,
                50,
                10
            ],
            k=1
        )[0]

    # --------------------------------------------------------
    # REFERENCE ID
    # --------------------------------------------------------

    if notification_type in [
        "Debit",
        "Credit",
        "OTP"
    ] and transaction_ids:

        reference_id = random.choice(
            transaction_ids
        )

    elif notification_type == "Fraud Alert" and fraud_alert_ids:

        reference_id = random.choice(
            fraud_alert_ids
        )

    elif notification_type == "KYC" and kyc_ids:

        reference_id = random.choice(
            kyc_ids
        )

    elif notification_type == "Loan Update" and loan_ids:

        reference_id = random.choice(
            loan_ids
        )

    else:

        reference_id = None

    # --------------------------------------------------------
    # READ AT
    # --------------------------------------------------------

    if read_status == "Read":

        max_read_seconds = max(
            1,
            int(
                (
                    datetime.now()
                    - sent_time
                ).total_seconds()
            )
        )

        read_at = sent_time + timedelta(
            seconds=random.randint(
                1,
                max_read_seconds
            )
        )

    else:

        read_at = None

    # --------------------------------------------------------
    # RETRY COUNT
    # --------------------------------------------------------

    if delivery_status == "Failed":

        retry_count = random.randint(
            1,
            3
        )

    elif delivery_status == "Pending":

        retry_count = random.randint(
            0,
            2
        )

    else:

        retry_count = 0

    # --------------------------------------------------------
    # EXPIRES AT
    # --------------------------------------------------------

    if notification_type == "OTP":

        expires_at = sent_time + timedelta(
            minutes=10
        )

    elif notification_type == "Promotional":

        expires_at = sent_time + timedelta(
            days=random.randint(7, 30)
        )

    elif notification_type == "Fraud Alert":

        expires_at = sent_time + timedelta(
            days=7
        )

    else:

        expires_at = sent_time + timedelta(
            days=random.randint(30, 90)
        )

    # --------------------------------------------------------
    # APPEND
    # --------------------------------------------------------

    notification_rows.append([
        customer_id,
        notification_type,
        title,
        message,
        channel,
        sent_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        delivery_status,
        read_status,
        priority,
        reference_id,
        (
            read_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if read_at
            else None
        ),
        retry_count,
        expires_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ])

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    if notification_number % 1000 == 0:

        print(
            f"Generated "
            f"{notification_number}/"
            f"{TOTAL_NOTIFICATIONS} "
            f"notifications..."
        )


# ============================================================
# WRITE CSV
# ============================================================

headers = [
    "customer_id",
    "notification_type",
    "title",
    "message",
    "channel",
    "sent_time",
    "delivery_status",
    "read_status",
    "priority",
    "reference_id",
    "read_at",
    "retry_count",
    "expires_at"
]


with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow(headers)

    writer.writerows(
        notification_rows
    )


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
print("NOTIFICATIONS DATA GENERATION SUCCESSFUL!")
print("=" * 60)

print()
print(
    f"Total notifications generated: "
    f"{TOTAL_NOTIFICATIONS}"
)

print()
print("CSV file saved at:")
print(OUTPUT_FILE)