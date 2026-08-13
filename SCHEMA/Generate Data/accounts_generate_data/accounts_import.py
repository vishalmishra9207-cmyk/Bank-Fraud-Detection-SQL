import pandas as pd
import mysql.connector
from pathlib import Path

# ----------------------------------------
# CSV FILE
# ----------------------------------------

csv_file = Path(__file__).parent / "accounts.csv"

df = pd.read_csv(csv_file)

print("CSV loaded successfully")
print("Total records:", len(df))


# ----------------------------------------
# MYSQL CONNECTION
# ----------------------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vishal@12",          # Yahan apna MySQL password daalo
    database="bank_fraud_db"
)

cursor = conn.cursor()

print("MySQL connected successfully")


# ----------------------------------------
# INSERT QUERY
# ----------------------------------------

insert_query = """
INSERT INTO accounts
(
    customer_id,
    account_number,
    account_type,
    balance,
    account_status,
    open_date,
    closed_date,
    created_at,
    branch_id
)
VALUES
(
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s
)
"""


# ----------------------------------------
# PREPARE DATA
# ----------------------------------------

records = []

for _, row in df.iterrows():

    closed_date = row["closed_date"]

    # Pandas NaN ko MySQL NULL me convert karna
    if pd.isna(closed_date):
        closed_date = None

    records.append(
        (
            int(row["customer_id"]),
            row["account_number"],
            row["account_type"],
            float(row["balance"]),
            row["account_status"],
            row["open_date"],
            closed_date,
            row["created_at"],
            int(row["branch_id"])
        )
    )


# ----------------------------------------
# INSERT DATA
# ----------------------------------------

cursor.executemany(
    insert_query,
    records
)

conn.commit()


# ----------------------------------------
# RESULT
# ----------------------------------------

print()
print("=" * 50)
print("ACCOUNT DATA IMPORTED SUCCESSFULLY")
print("=" * 50)

print("Records inserted:", cursor.rowcount)


# ----------------------------------------
# CLOSE CONNECTION
# ----------------------------------------

cursor.close()
conn.close()

print("MySQL connection closed")