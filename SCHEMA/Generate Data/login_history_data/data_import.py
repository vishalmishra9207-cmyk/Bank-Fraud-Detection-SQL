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

csv_file = Path(__file__).parent / "login_history.csv"

print()
print("CSV file found:")
print(csv_file)


# ============================================================
# READ CSV
# ============================================================

df = pd.read_csv(csv_file)

print()
print(f"Total records found in CSV: {len(df)}")


# ============================================================
# CONVERT NaN TO NONE
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
INSERT INTO login_history (
    customer_id,
    device_id,
    login_time,
    logout_time,
    login_status,
    login_method,
    ip_address,
    location,
    failed_attempts,
    session_id,
    login_city,
    login_state,
    login_country,
    logout_reason,
    is_suspicious
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
)
"""


# ============================================================
# PREPARE DATA
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

    data.append(tuple(cleaned_row))


# ============================================================
# IMPORT DATA
# ============================================================

BATCH_SIZE = 500

total_records = len(data)

print()
print("Importing login history data...")
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

        batch = data[start:end]

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
    print("LOGIN HISTORY DATA IMPORT SUCCESSFUL!")
    print("=" * 60)


except mysql.connector.Error as e:

    conn.rollback()

    print()
    print("ERROR: Login history data import failed!")
    print("MySQL Error:", e)


finally:

    cursor.close()
    conn.close()