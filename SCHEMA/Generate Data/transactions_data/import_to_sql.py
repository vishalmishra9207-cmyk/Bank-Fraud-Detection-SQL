import csv
import mysql.connector
from pathlib import Path
from getpass import getpass


# ============================================================
# 1. FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "merchants.csv"


# ============================================================
# 2. MYSQL CONNECTION
# ============================================================

print("=" * 60)
print("MERCHANTS DATA IMPORT")
print("=" * 60)

password = getpass("Enter MySQL password: ")

try:

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="bank_fraud_db"
    )

    cursor = conn.cursor()

    print("\nMySQL connection successful!")

except mysql.connector.Error as err:

    print("\nMySQL connection failed!")
    print("Error:", err)

    exit()


# ============================================================
# 3. CHECK CSV FILE
# ============================================================

if not CSV_FILE.exists():

    print("\nCSV file not found!")

    print("Expected location:")
    print(CSV_FILE)

    cursor.close()
    conn.close()

    exit()


print("\nCSV file found:")
print(CSV_FILE)


# ============================================================
# 4. READ CSV
# ============================================================

try:

    with open(
        CSV_FILE,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        rows = list(reader)

    print("\nTotal records found in CSV:", len(rows))

except Exception as err:

    print("\nError while reading CSV:")
    print(err)

    cursor.close()
    conn.close()

    exit()


# ============================================================
# 5. INSERT QUERY
# ============================================================

insert_query = """
INSERT INTO merchants
(
    merchant_code,
    merchant_name,
    merchant_category,
    merchant_type,
    contact_number,
    merchant_email,
    gst_number,
    building_no,
    street,
    city,
    state,
    pincode,
    country,
    merchant_status,
    created_at,
    risk_level
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""


# ============================================================
# 6. CLEAN FUNCTION
# ============================================================

def clean(value):

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    if value.lower() == "none":
        return None

    return value


# ============================================================
# 7. PREPARE DATA
# ============================================================

data = []


for row in rows:

    merchant_code = clean(
        row["merchant_code"]
    )

    merchant_name = clean(
        row["merchant_name"]
    )

    merchant_category = clean(
        row["merchant_category"]
    )

    merchant_type = clean(
        row["merchant_type"]
    )

    contact_number = clean(
        row["contact_number"]
    )

    merchant_email = clean(
        row["merchant_email"]
    )

    gst_number = clean(
        row["gst_number"]
    )

    building_no = clean(
        row["building_no"]
    )

    street = clean(
        row["street"]
    )

    city = clean(
        row["city"]
    )

    state = clean(
        row["state"]
    )

    pincode = clean(
        row["pincode"]
    )

    country = clean(
        row["country"]
    )

    merchant_status = clean(
        row["merchant_status"]
    )

    created_at = clean(
        row["created_at"]
    )

    risk_level = clean(
        row["risk_level"]
    )


    data.append(
        (
            merchant_code,
            merchant_name,
            merchant_category,
            merchant_type,
            contact_number,
            merchant_email,
            gst_number,
            building_no,
            street,
            city,
            state,
            pincode,
            country,
            merchant_status,
            created_at,
            risk_level
        )
    )


# ============================================================
# 8. INSERT DATA
# ============================================================

try:

    print("\nImporting merchants data...")

    cursor.executemany(
        insert_query,
        data
    )

    conn.commit()

    print(
        "\nMerchants data imported successfully!"
    )

    print(
        "Records inserted:",
        cursor.rowcount
    )


except mysql.connector.Error as err:

    conn.rollback()

    print(
        "\nERROR: Merchants data import failed!"
    )

    print(
        "MySQL Error:",
        err
    )

    cursor.close()
    conn.close()

    exit()


# ============================================================
# 9. VERIFY TOTAL RECORDS
# ============================================================

print("\n" + "=" * 60)
print("VERIFYING MERCHANTS TABLE")
print("=" * 60)


cursor.execute(
    "SELECT COUNT(*) FROM merchants"
)

total_records = cursor.fetchone()[0]


print(
    "\nTotal merchants in MySQL:",
    total_records
)


# ============================================================
# 10. SHOW FIRST 5 RECORDS
# ============================================================

cursor.execute(
    """
    SELECT
        merchant_id,
        merchant_code,
        merchant_name,
        merchant_category,
        merchant_type,
        merchant_status,
        risk_level
    FROM merchants
    ORDER BY merchant_id
    LIMIT 5
    """
)

records = cursor.fetchall()


print("\nFirst 5 merchants:")

for record in records:

    print(record)


# ============================================================
# 11. CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()


print("\n" + "=" * 60)
print("MERCHANT IMPORT COMPLETED SUCCESSFULLY!")
print("=" * 60)