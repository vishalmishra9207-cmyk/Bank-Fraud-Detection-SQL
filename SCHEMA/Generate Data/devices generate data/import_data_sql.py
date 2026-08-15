import csv
import mysql.connector
from pathlib import Path
from getpass import getpass


# ============================================================
# 1. FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "devices.csv"


# ============================================================
# 2. MYSQL CONNECTION
# ============================================================

print("=" * 60)
print("DEVICES DATA IMPORT")
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

# IMPORTANT:
# 17 columns = 17 placeholders

insert_query = """
INSERT INTO devices
(
    customer_id,
    device_identifier,
    device_name,
    device_type,
    device_model,
    operating_system,
    os_version,
    app_version,
    device_status,
    is_trusted,
    last_ip_address,
    last_login_city,
    last_login,
    registered_at,
    registered_from,
    failed_login_attempts,
    blocked_at
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

    if value.lower() in ["none", "nan", "nat"]:
        return None

    return value


# ============================================================
# 7. PREPARE DATA
# ============================================================

data = []


for row in rows:

    customer_id = clean(
        row["customer_id"]
    )

    device_identifier = clean(
        row["device_identifier"]
    )

    device_name = clean(
        row["device_name"]
    )

    device_type = clean(
        row["device_type"]
    )

    device_model = clean(
        row["device_model"]
    )

    operating_system = clean(
        row["operating_system"]
    )

    os_version = clean(
        row["os_version"]
    )

    app_version = clean(
        row["app_version"]
    )

    device_status = clean(
        row["device_status"]
    )

    is_trusted = clean(
        row["is_trusted"]
    )

    last_ip_address = clean(
        row["last_ip_address"]
    )

    last_login_city = clean(
        row["last_login_city"]
    )

    last_login = clean(
        row["last_login"]
    )

    registered_at = clean(
        row["registered_at"]
    )

    registered_from = clean(
        row["registered_from"]
    )

    failed_login_attempts = clean(
        row["failed_login_attempts"]
    )

    blocked_at = clean(
        row["blocked_at"]
    )


    # --------------------------------------------------------
    # INTEGER CONVERSION
    # --------------------------------------------------------

    customer_id = int(customer_id)

    is_trusted = int(is_trusted)

    failed_login_attempts = int(
        failed_login_attempts
    )


    # --------------------------------------------------------
    # ADD RECORD
    # --------------------------------------------------------

    data.append(
        (
            customer_id,
            device_identifier,
            device_name,
            device_type,
            device_model,
            operating_system,
            os_version,
            app_version,
            device_status,
            is_trusted,
            last_ip_address,
            last_login_city,
            last_login,
            registered_at,
            registered_from,
            failed_login_attempts,
            blocked_at
        )
    )


# ============================================================
# 8. INSERT DATA
# ============================================================

try:

    print("\nImporting devices data...")

    cursor.executemany(
        insert_query,
        data
    )

    conn.commit()

    print(
        "\nDevices data imported successfully!"
    )

    print(
        "Records inserted:",
        cursor.rowcount
    )


except mysql.connector.Error as err:

    conn.rollback()

    print(
        "\nERROR: Devices data import failed!"
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
print("VERIFYING DEVICES TABLE")
print("=" * 60)


cursor.execute(
    "SELECT COUNT(*) FROM devices"
)

total_records = cursor.fetchone()[0]


print(
    "\nTotal devices in MySQL:",
    total_records
)


# ============================================================
# 10. SHOW FIRST 5 RECORDS
# ============================================================

cursor.execute(
    """
    SELECT
        device_id,
        customer_id,
        device_identifier,
        device_type,
        device_model,
        device_status,
        is_trusted
    FROM devices
    ORDER BY device_id
    LIMIT 5
    """
)

records = cursor.fetchall()


print("\nFirst 5 devices:")

for record in records:

    print(record)


# ============================================================
# 11. VERIFY CUSTOMER FOREIGN KEY
# ============================================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM devices d
    LEFT JOIN customers c
        ON d.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
    """
)

invalid_customer_ids = cursor.fetchone()[0]


print(
    "\nDevices with invalid customer_id:",
    invalid_customer_ids
)


# ============================================================
# 12. VERIFY DEVICE IDENTIFIERS
# ============================================================

cursor.execute(
    """
    SELECT
        COUNT(*) - COUNT(DISTINCT device_identifier)
    FROM devices
    """
)

duplicate_device_identifiers = cursor.fetchone()[0]


print(
    "Duplicate device identifiers:",
    duplicate_device_identifiers
)


# ============================================================
# 13. CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()


print("\n" + "=" * 60)
print("DEVICE IMPORT COMPLETED SUCCESSFULLY!")
print("=" * 60)