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

csv_file = Path(__file__).parent / "loans.csv"

print()
print(f"CSV file found:")
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
# IMPORT DATA
# ============================================================

print()
print("Importing loans data...")


insert_query = """
INSERT INTO loans (
    customer_id,
    account_id,
    loan_type,
    loan_amount,
    interest_rate,
    tenure_months,
    emi_amount,
    loan_start_date,
    loan_end_date,
    loan_status,
    approved_by,
    approved_date,
    created_at,
    outstanding_balance,
    paid_emi_count,
    next_emi_date,
    rejection_reason
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s
)
"""


try:

    data = []

    for row in rows:

        data.append((
            int(row["customer_id"]),
            int(row["account_id"]),
            row["loan_type"],
            float(row["loan_amount"]),
            float(row["interest_rate"]),
            int(row["tenure_months"]),
            float(row["emi_amount"]),
            row["loan_start_date"],
            row["loan_end_date"],
            row["loan_status"],
            int(row["approved_by"])
                if row["approved_by"] else None,
            row["approved_date"]
                if row["approved_date"] else None,
            row["created_at"],
            float(row["outstanding_balance"]),
            int(row["paid_emi_count"]),
            row["next_emi_date"]
                if row["next_emi_date"] else None,
            row["rejection_reason"]
                if row["rejection_reason"] else None
        ))

    cursor.executemany(
        insert_query,
        data
    )

    conn.commit()

    print()
    print("Loans data imported successfully!")
    print(f"Records imported: {cursor.rowcount}")


except mysql.connector.Error as error:

    conn.rollback()

    print()
    print("ERROR: Loans data import failed!")
    print(f"MySQL Error: {error}")


finally:

    cursor.close()
    conn.close()

