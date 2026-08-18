import csv
import mysql.connector
from pathlib import Path


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
# CSV FILE
# ============================================================

csv_file = Path(__file__).parent / "notifications.csv"

print()
print("CSV file found:")
print(csv_file)


# ============================================================
# READ CSV
# ============================================================

with open(
    csv_file,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    rows = list(reader)


print()
print(f"Total records found in CSV: {len(rows)}")


# ============================================================
# INSERT QUERY
# ============================================================

insert_query = """
INSERT INTO notifications (
    customer_id,
    notification_type,
    title,
    message,
    channel,
    sent_time,
    delivery_status,
    read_status,
    priority,
    reference_id,
    read_at,
    retry_count,
    expires_at
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s
)
"""


# ============================================================
# PREPARE DATA
# ============================================================

data = []

for row in rows:

    data.append((
        int(row["customer_id"]),
        row["notification_type"],
        row["title"],
        row["message"],
        row["channel"],
        row["sent_time"],
        row["delivery_status"],
        row["read_status"],
        row["priority"],
        int(row["reference_id"])
            if row["reference_id"] else None,
        row["read_at"]
            if row["read_at"] else None,
        int(row["retry_count"]),
        row["expires_at"]
    ))


# ============================================================
# IMPORT DATA
# ============================================================

print()
print("Importing notifications data...")
print()


try:

    BATCH_SIZE = 500

    total_records = len(data)

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
    print("NOTIFICATIONS DATA IMPORT SUCCESSFUL!")
    print("=" * 60)


except mysql.connector.Error as error:

    conn.rollback()

    print()
    print("ERROR: Notifications data import failed!")
    print("MySQL Error:", error)


finally:

    cursor.close()
    conn.close()