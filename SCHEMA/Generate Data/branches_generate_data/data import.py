import pandas as pd
import mysql.connector
from pathlib import Path

# ----------------------------------------
# CSV FILE
# ----------------------------------------

csv_file = Path(__file__).parent / "branches.csv"

df = pd.read_csv(csv_file)

print("CSV loaded successfully")
print("Total records:", len(df))


# ----------------------------------------
# MYSQL CONNECTION
# ----------------------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vishal@12",              # Yahan apna MySQL password daalo
    database="bank_fraud_db"
)

cursor = conn.cursor()

print("MySQL connected successfully")


# ----------------------------------------
# INSERT QUERY
# ----------------------------------------

insert_query = """
INSERT INTO branches
(
    branch_code,
    branch_manager_id,
    building_no,
    street,
    area,
    city,
    state,
    pincode,
    ifsc_code,
    contact_number,
    branch_email,
    branch_status,
    created_at,
    contact_number_branch
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s
)
"""


# ----------------------------------------
# PREPARE DATA
# ----------------------------------------

records = []

for _, row in df.iterrows():

    records.append(
        (
            row["branch_code"],
            None,  # branch_manager_id will be assigned later
            row["building_no"],
            row["street"],
            row["area"],
            row["city"],
            row["state"],
            row["pincode"],
            row["ifsc_code"],
            row["contact_number"],
            row["branch_email"],
            row["branch_status"],
            row["created_at"],
            row["contact_number_branch"]
        )
    )


# ----------------------------------------
# INSERT INTO MYSQL
# ----------------------------------------

cursor.executemany(insert_query, records)

conn.commit()


# ----------------------------------------
# RESULT
# ----------------------------------------

print()
print("=" * 50)
print("BRANCH DATA IMPORTED SUCCESSFULLY")
print("=" * 50)

print("Records inserted:", cursor.rowcount)


# ----------------------------------------
# CLOSE CONNECTION
# ----------------------------------------

cursor.close()
conn.close()

print("MySQL connection closed")