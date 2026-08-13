import csv
import mysql.connector
from pathlib import Path
from getpass import getpass


# ============================================================
# 1. FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "employees.csv"


# ============================================================
# 2. MYSQL CONNECTION
# ============================================================

print("=" * 60)
print("EMPLOYEES DATA IMPORT")
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

    with open(CSV_FILE, mode="r", encoding="utf-8-sig", newline="") as file:

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
INSERT INTO employees
(
    employee_code,
    branch_id,
    employee_name,
    gender,
    dob,
    designation,
    department,
    mobile_number,
    email,
    hire_date,
    salary,
    emp_house_no,
    emp_street,
    emp_area,
    emp_city,
    emp_state,
    emp_pincode,
    country,
    employee_status,
    created_at,
    manager_id,
    exit_date
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""


# ============================================================
# 6. PREPARE DATA
# ============================================================

data = []

for row in rows:

    def clean(value):
        if value is None:
            return None

        value = str(value).strip()

        if value == "" or value.lower() == "none":
            return None

        return value


    employee_code = clean(row["employee_code"])
    branch_id = clean(row["branch_id"])
    employee_name = clean(row["employee_name"])
    gender = clean(row["gender"])
    dob = clean(row["dob"])
    designation = clean(row["designation"])
    department = clean(row["department"])
    mobile_number = clean(row["mobile_number"])
    email = clean(row["email"])
    hire_date = clean(row["hire_date"])
    salary = clean(row["salary"])
    emp_house_no = clean(row["emp_house_no"])
    emp_street = clean(row["emp_street"])
    emp_area = clean(row["emp_area"])
    emp_city = clean(row["emp_city"])
    emp_state = clean(row["emp_state"])
    emp_pincode = clean(row["emp_pincode"])
    country = clean(row["country"])
    employee_status = clean(row["employee_status"])
    created_at = clean(row["created_at"])
    manager_id = clean(row["manager_id"])
    exit_date = clean(row["exit_date"])


    # Convert numeric fields
    if branch_id is not None:
        branch_id = int(branch_id)

    if salary is not None:
        salary = float(salary)

    if manager_id is not None:
        manager_id = int(manager_id)


    data.append(
        (
            employee_code,
            branch_id,
            employee_name,
            gender,
            dob,
            designation,
            department,
            mobile_number,
            email,
            hire_date,
            salary,
            emp_house_no,
            emp_street,
            emp_area,
            emp_city,
            emp_state,
            emp_pincode,
            country,
            employee_status,
            created_at,
            manager_id,
            exit_date
        )
    )


# ============================================================
# 7. INSERT INTO MYSQL
# ============================================================

try:

    print("\nImporting employees data...")

    cursor.executemany(insert_query, data)

    conn.commit()

    print("\nEmployees data imported successfully!")

    print("Records inserted:", cursor.rowcount)


except mysql.connector.Error as err:

    conn.rollback()

    print("\nERROR: Employees data import failed!")
    print("MySQL Error:", err)

    cursor.close()
    conn.close()

    exit()


# ============================================================
# 8. VERIFY DATA
# ============================================================

print("\n" + "=" * 60)
print("VERIFYING EMPLOYEES TABLE")
print("=" * 60)


cursor.execute("SELECT COUNT(*) FROM employees")

total_records = cursor.fetchone()[0]

print("\nTotal employees in MySQL:", total_records)


# ============================================================
# 9. SHOW FIRST 5 RECORDS
# ============================================================

cursor.execute("""
SELECT
    employee_id,
    employee_code,
    branch_id,
    employee_name,
    designation,
    employee_status,
    manager_id
FROM employees
ORDER BY employee_id
LIMIT 5
""")

records = cursor.fetchall()

print("\nFirst 5 employees:")

for record in records:
    print(record)


# ============================================================
# 10. CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()

print("\n" + "=" * 60)
print("EMPLOYEE IMPORT COMPLETED SUCCESSFULLY!")
print("=" * 60)