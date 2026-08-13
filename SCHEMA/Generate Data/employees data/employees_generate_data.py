from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# --------------------------------------------------
# BASIC SETUP
# --------------------------------------------------

fake = Faker("en_IN")

TOTAL_EMPLOYEES = 100
TOTAL_BRANCHES = 20

# --------------------------------------------------
# DESIGNATION + DEPARTMENT + SALARY
# --------------------------------------------------

designation_data = {
    "Branch Manager": {
        "department": "Branch Operations",
        "salary": (70000, 120000)
    },
    "Assistant Branch Manager": {
        "department": "Branch Operations",
        "salary": (50000, 80000)
    },
    "Relationship Manager": {
        "department": "Sales",
        "salary": (35000, 65000)
    },
    "Loan Officer": {
        "department": "Loans",
        "salary": (35000, 60000)
    },
    "Cashier": {
        "department": "Cash Operations",
        "salary": (25000, 45000)
    },
    "Customer Service Executive": {
        "department": "Customer Service",
        "salary": (22000, 40000)
    },
    "Operations Executive": {
        "department": "Operations",
        "salary": (25000, 45000)
    },
    "IT Executive": {
        "department": "IT",
        "salary": (35000, 70000)
    },
    "HR Executive": {
        "department": "Human Resources",
        "salary": (30000, 55000)
    }
}

designations = list(designation_data.keys())

designation_weights = [
    8,   # Branch Manager
    7,   # Assistant Branch Manager
    15,  # Relationship Manager
    10,  # Loan Officer
    15,  # Cashier
    15,  # Customer Service
    15,  # Operations
    7,   # IT
    8    # HR
]

# --------------------------------------------------
# UNIQUE VALUE SETS
# --------------------------------------------------

used_employee_codes = set()
used_mobile_numbers = set()
used_emails = set()

employees = []

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def generate_employee_code(number):

    code = f"EMP{number:04d}"

    while code in used_employee_codes:
        number += 1
        code = f"EMP{number:04d}"

    used_employee_codes.add(code)

    return code


def generate_mobile_number():

    while True:

        number = str(
            random.randint(7000000000, 9999999999)
        )

        if number not in used_mobile_numbers:

            used_mobile_numbers.add(number)

            return number


def generate_email(first_name, last_name, number):

    first_name = first_name.lower()
    last_name = last_name.lower()

    email = f"{first_name}.{last_name}{number}@vmbank.com"

    while email in used_emails:

        number += 1
        email = f"{first_name}.{last_name}{number}@vmbank.com"

    used_emails.add(email)

    return email


def generate_dob():

    start_date = datetime(1965, 1, 1)
    end_date = datetime(2002, 12, 31)

    days = (end_date - start_date).days

    return (
        start_date +
        timedelta(days=random.randint(0, days))
    ).date()


def generate_hire_date():

    start_date = datetime(2015, 1, 1)
    end_date = datetime(2025, 12, 31)

    days = (end_date - start_date).days

    return (
        start_date +
        timedelta(days=random.randint(0, days))
    ).date()


def generate_employee_status():

    return random.choices(
        [
            "Active",
            "Inactive",
            "Suspended",
            "Resigned"
        ],
        weights=[
            90,
            4,
            2,
            4
        ]
    )[0]


# --------------------------------------------------
# GENERATE EMPLOYEES
# --------------------------------------------------

for i in range(1, TOTAL_EMPLOYEES + 1):

    # ----------------------------------------------
    # NAME
    # ----------------------------------------------

    first_name = fake.first_name()
    last_name = fake.last_name()

    employee_name = f"{first_name} {last_name}"

    # ----------------------------------------------
    # DESIGNATION
    # ----------------------------------------------

    designation = random.choices(
        designations,
        weights=designation_weights
    )[0]

    department = designation_data[
        designation
    ]["department"]

    salary_min, salary_max = designation_data[
        designation
    ]["salary"]

    salary = round(
        random.uniform(
            salary_min,
            salary_max
        ),
        2
    )

    # ----------------------------------------------
    # BRANCH
    # ----------------------------------------------

    branch_id = random.randint(
        1,
        TOTAL_BRANCHES
    )

    # ----------------------------------------------
    # PERSONAL DETAILS
    # ----------------------------------------------

    gender = random.choices(
        ["Male", "Female", "Other"],
        weights=[48, 51, 1]
    )[0]

    dob = generate_dob()

    # ----------------------------------------------
    # EMPLOYMENT DETAILS
    # ----------------------------------------------

    hire_date = generate_hire_date()

    employee_status = generate_employee_status()

    # ----------------------------------------------
    # EXIT DATE
    # ----------------------------------------------

    exit_date = None

    if employee_status == "Resigned":

        minimum_exit_date = (
            hire_date +
            timedelta(days=90)
        )

        maximum_exit_date = datetime.now().date()

        if minimum_exit_date <= maximum_exit_date:

            days = (
                maximum_exit_date -
                minimum_exit_date
            ).days

            exit_date = (
                minimum_exit_date +
                timedelta(
                    days=random.randint(0, days)
                )
            )

    # ----------------------------------------------
    # EMPLOYEE RECORD
    # ----------------------------------------------

    employee = {

        # employee_id is AUTO_INCREMENT
        # so we don't generate it

        "employee_code":
            generate_employee_code(i),

        "branch_id":
            branch_id,

        "employee_name":
            employee_name,

        "gender":
            gender,

        "dob":
            dob,

        "designation":
            designation,

        "department":
            department,

        "mobile_number":
            generate_mobile_number(),

        "email":
            generate_email(
                first_name,
                last_name,
                i
            ),

        "hire_date":
            hire_date,

        "salary":
            salary,

        "emp_house_no":
            str(random.randint(1, 999)),

        "emp_street":
            fake.street_name(),

        "emp_area":
            fake.city_suffix(),

        "emp_city":
            fake.city(),

        "emp_state":
            fake.state(),

        "emp_pincode":
            fake.postcode()[:6],

        "country":
            "India",

        "employee_status":
            employee_status,

        "created_at":
            datetime.combine(
                hire_date,
                datetime.min.time()
            ),

        # Manager will be assigned later
        "manager_id":
            None,

        "exit_date":
            exit_date
    }

    employees.append(employee)


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(employees)


# --------------------------------------------------
# SAVE CSV
# --------------------------------------------------

output_file = (
    Path(__file__).parent /
    "employees.csv"
)

df.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

print()
print("=" * 60)
print("EMPLOYEE DATA GENERATION COMPLETED")
print("=" * 60)

print()

print("Total employees:")
print(len(df))

print()

print("Data shape:")
print(df.shape)

print()

print("Missing values:")
print(df.isnull().sum())

print()

print("Duplicate employee codes:")
print(
    df["employee_code"].duplicated().sum()
)

print()

print("Duplicate mobile numbers:")
print(
    df["mobile_number"].duplicated().sum()
)

print()

print("Duplicate emails:")
print(
    df["email"].duplicated().sum()
)

print()

print("Branch IDs outside range:")
print(
    (
        (df["branch_id"] < 1) |
        (df["branch_id"] > 20)
    ).sum()
)

print()

print("Employee status distribution:")
print(
    df["employee_status"].value_counts()
)

print()

print("Designation distribution:")
print(
    df["designation"].value_counts()
)

print()

print("Employees with exit date but not resigned:")
print(
    (
        (df["employee_status"] != "Resigned") &
        (df["exit_date"].notnull())
    ).sum()
)

print()

print("Resigned employees without exit date:")
print(
    (
        (df["employee_status"] == "Resigned") &
        (df["exit_date"].isnull())
    ).sum()
)

print()

print("Manager IDs:")
print(
    df["manager_id"].value_counts(dropna=False)
)

print()

print("CSV file created:")
print(output_file)

print()

print("First 5 records:")
print(df.head())

print()

print("=" * 60)
print("EMPLOYEE CSV SAVED SUCCESSFULLY!")
print("=" * 60)