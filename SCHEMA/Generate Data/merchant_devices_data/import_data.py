import csv
import mysql.connector
from pathlib import Path
from getpass import getpass


# ============================================================
# 1. FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "merchant_devices.csv"


# ============================================================
# 2. MYSQL CONNECTION
# ============================================================

print("=" * 60)
print("MERCHANT DEVICES DATA IMPORT")
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

    print(
        "\nTotal records found in CSV:",
        len(rows)
    )

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
INSERT INTO merchant_devices
(
    merchant_id,
    device_serial_number,
    device_model,
    merchant_device_type,
    merchant_device_status,
    device_issue_date,
    last_service_date,
    branch_id,
    warranty_expiry,
    last_used_at,
    firmware_version
)
VALUES
(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
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

    if value.lower() in [
        "none",
        "nan",
        "nat"
    ]:
        return None

    return value


# ============================================================
# 7. PREPARE DATA
# ============================================================

data = []


for row in rows:

    merchant_id = clean(
        row["merchant_id"]
    )

    device_serial_number = clean(
        row["device_serial_number"]
    )

    device_model = clean(
        row["device_model"]
    )

    merchant_device_type = clean(
        row["merchant_device_type"]
    )

    merchant_device_status = clean(
        row["merchant_device_status"]
    )

    device_issue_date = clean(
        row["device_issue_date"]
    )

    last_service_date = clean(
        row["last_service_date"]
    )

    branch_id = clean(
        row["branch_id"]
    )

    warranty_expiry = clean(
        row["warranty_expiry"]
    )

    last_used_at = clean(
        row["last_used_at"]
    )

    firmware_version = clean(
        row["firmware_version"]
    )


    # --------------------------------------------------------
    # INTEGER CONVERSION
    # --------------------------------------------------------

    merchant_id = int(
        merchant_id
    )

    branch_id = int(
        branch_id
    )


    # --------------------------------------------------------
    # ADD RECORD
    # --------------------------------------------------------

    data.append(
        (
            merchant_id,
            device_serial_number,
            device_model,
            merchant_device_type,
            merchant_device_status,
            device_issue_date,
            last_service_date,
            branch_id,
            warranty_expiry,
            last_used_at,
            firmware_version
        )
    )


# ============================================================
# 8. INSERT DATA
# ============================================================

try:

    print("\nImporting merchant devices data...")

    cursor.executemany(
        insert_query,
        data
    )

    conn.commit()

    print(
        "\nMerchant devices data imported successfully!"
    )

    print(
        "Records inserted:",
        cursor.rowcount
    )


except mysql.connector.Error as err:

    conn.rollback()

    print(
        "\nERROR: Merchant devices data import failed!"
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
print("VERIFYING MERCHANT_DEVICES TABLE")
print("=" * 60)


cursor.execute(
    "SELECT COUNT(*) FROM merchant_devices"
)

total_records = cursor.fetchone()[0]


print(
    "\nTotal merchant devices in MySQL:",
    total_records
)


# ============================================================
# 10. SHOW FIRST 5 RECORDS
# ============================================================

cursor.execute(
    """
    SELECT
        merchant_device_id,
        merchant_id,
        device_serial_number,
        device_model,
        merchant_device_type,
        merchant_device_status,
        branch_id
    FROM merchant_devices
    ORDER BY merchant_device_id
    LIMIT 5
    """
)

records = cursor.fetchall()


print("\nFirst 5 merchant devices:")

for record in records:

    print(record)


# ============================================================
# 11. VERIFY MERCHANT FOREIGN KEY
# ============================================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM merchant_devices md
    LEFT JOIN merchants m
        ON md.merchant_id = m.merchant_id
    WHERE m.merchant_id IS NULL
    """
)

invalid_merchants = cursor.fetchone()[0]


print(
    "\nDevices with invalid merchant_id:",
    invalid_merchants
)


# ============================================================
# 12. VERIFY BRANCH FOREIGN KEY
# ============================================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM merchant_devices md
    LEFT JOIN branches b
        ON md.branch_id = b.branch_id
    WHERE b.branch_id IS NULL
    """
)

invalid_branches = cursor.fetchone()[0]


print(
    "Devices with invalid branch_id:",
    invalid_branches
)


# ============================================================
# 13. VERIFY DUPLICATE SERIAL NUMBERS
# ============================================================

cursor.execute(
    """
    SELECT
        COUNT(*) - COUNT(
            DISTINCT device_serial_number
        )
    FROM merchant_devices
    """
)

duplicate_serials = cursor.fetchone()[0]


print(
    "Duplicate device serial numbers:",
    duplicate_serials
)


# ============================================================
# 14. CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()


print("\n" + "=" * 60)
print("MERCHANT DEVICES IMPORT COMPLETED!")
print("=" * 60)