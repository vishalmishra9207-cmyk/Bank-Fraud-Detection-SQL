import csv
import mysql.connector
from pathlib import Path
from getpass import getpass


# ============================================================
# 1. FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "cards.csv"


# ============================================================
# 2. MYSQL CONNECTION
# ============================================================

print("=" * 60)
print("CARDS DATA IMPORT")
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
INSERT INTO cards
(
    account_id,
    card_number,
    card_holder_name,
    card_type,
    card_network,
    issue_date,
    expiry_date,
    card_status,
    daily_limit,
    international_usage,
    contactless_enabled,
    created_at,
    block_reason
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s
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

    account_id = clean(
        row["account_id"]
    )

    card_number = clean(
        row["card_number"]
    )

    card_holder_name = clean(
        row["card_holder_name"]
    )

    card_type = clean(
        row["card_type"]
    )

    card_network = clean(
        row["card_network"]
    )

    issue_date = clean(
        row["issue_date"]
    )

    expiry_date = clean(
        row["expiry_date"]
    )

    card_status = clean(
        row["card_status"]
    )

    daily_limit = clean(
        row["daily_limit"]
    )

    international_usage = clean(
        row["international_usage"]
    )

    contactless_enabled = clean(
        row["contactless_enabled"]
    )

    created_at = clean(
        row["created_at"]
    )

    block_reason = clean(
        row["block_reason"]
    )


    # --------------------------------------------------------
    # INTEGER / NUMERIC CONVERSION
    # --------------------------------------------------------

    account_id = int(account_id)

    daily_limit = float(daily_limit)

    international_usage = int(
        international_usage
    )

    contactless_enabled = int(
        contactless_enabled
    )


    # --------------------------------------------------------
    # ADD RECORD
    # --------------------------------------------------------

    data.append(
        (
            account_id,
            card_number,
            card_holder_name,
            card_type,
            card_network,
            issue_date,
            expiry_date,
            card_status,
            daily_limit,
            international_usage,
            contactless_enabled,
            created_at,
            block_reason
        )
    )


# ============================================================
# 8. INSERT DATA
# ============================================================

try:

    print("\nImporting cards data...")

    cursor.executemany(
        insert_query,
        data
    )

    conn.commit()

    print(
        "\nCards data imported successfully!"
    )

    print(
        "Records inserted:",
        cursor.rowcount
    )


except mysql.connector.Error as err:

    conn.rollback()

    print(
        "\nERROR: Cards data import failed!"
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
print("VERIFYING CARDS TABLE")
print("=" * 60)


cursor.execute(
    "SELECT COUNT(*) FROM cards"
)

total_records = cursor.fetchone()[0]


print(
    "\nTotal cards in MySQL:",
    total_records
)


# ============================================================
# 10. SHOW FIRST 5 RECORDS
# ============================================================

cursor.execute(
    """
    SELECT
        card_id,
        account_id,
        card_number,
        card_type,
        card_network,
        card_status,
        daily_limit
    FROM cards
    ORDER BY card_id
    LIMIT 5
    """
)

records = cursor.fetchall()


print("\nFirst 5 cards:")

for record in records:

    print(record)


# ============================================================
# 11. VERIFY FOREIGN KEY
# ============================================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM cards c
    LEFT JOIN accounts a
        ON c.account_id = a.account_id
    WHERE a.account_id IS NULL
    """
)

invalid_accounts = cursor.fetchone()[0]


print(
    "\nCards with invalid account_id:",
    invalid_accounts
)


# ============================================================
# 12. VERIFY DUPLICATE CARD NUMBERS
# ============================================================

cursor.execute(
    """
    SELECT
        COUNT(*) - COUNT(DISTINCT card_number)
    FROM cards
    """
)

duplicate_cards = cursor.fetchone()[0]


print(
    "Duplicate card numbers:",
    duplicate_cards
)


# ============================================================
# 13. CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()


print("\n" + "=" * 60)
print("CARD IMPORT COMPLETED SUCCESSFULLY!")
print("=" * 60)