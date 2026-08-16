import pandas as pd
import mysql.connector
from pathlib import Path
from getpass import getpass


# ============================================================
# DATABASE CONNECTION
# ============================================================

password = getpass("Enter MySQL password: ")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="bank_fraud_db"
)

cursor = conn.cursor()


# ============================================================
# CSV FILE
# ============================================================

csv_file = (
    Path(__file__).parent
    / "transactions.csv"
)

print()
print("CSV file found:")
print(csv_file)


# ============================================================
# READ CSV
# ============================================================

df = pd.read_csv(
    csv_file
)

print()
print(
    f"Total records found in CSV: {len(df)}"
)


# ============================================================
# CONVERT NaN / NaT TO NONE
# ============================================================

df = df.astype(object)

df = df.where(
    pd.notna(df),
    None
)


# ============================================================
# INSERT QUERY
# ============================================================

insert_query = """
INSERT INTO transactions (
    account_id,
    reference_number,
    amount,
    transaction_type,
    transaction_time,
    transaction_status,
    payment_mode,
    transaction_location,
    receiver_account_id,
    merchant_id,
    device_id,
    ip_address,
    is_fraud,
    remarks,
    risk_score
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
)
"""


# ============================================================
# CONVERT DATA TO TUPLES
# ============================================================

data = []

for row in df.itertuples(
    index=False,
    name=None
):

    cleaned_row = []

    for value in row:

        if pd.isna(value):

            cleaned_row.append(None)

        else:

            cleaned_row.append(value)

    data.append(
        tuple(cleaned_row)
    )


# ============================================================
# BATCH IMPORT
# ============================================================

BATCH_SIZE = 1000

total_records = len(data)

print()
print("Importing transactions data...")
print()


try:

    for start in range(
        0,
        total_records,
        BATCH_SIZE
    ):

        end = min(
            start + BATCH_SIZE,
            total_records
        )

        batch = data[
            start:end
        ]

        cursor.executemany(
            insert_query,
            batch
        )

        conn.commit()

        print(
            f"Imported {end}/{total_records} records..."
        )


    print()
    print("=" * 60)
    print("TRANSACTIONS DATA IMPORT SUCCESSFUL!")
    print("=" * 60)


except mysql.connector.Error as e:

    conn.rollback()

    print()
    print("ERROR: Transactions data import failed!")
    print("MySQL Error:", e)


finally:

    cursor.close()
    conn.close()