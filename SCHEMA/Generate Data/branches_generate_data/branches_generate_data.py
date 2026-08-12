from faker import Faker
import pandas as pd
import random
from datetime import datetime
from pathlib import Path

# --------------------------------------------------
# BASIC SETUP
# --------------------------------------------------

fake = Faker("en_IN")

TOTAL_BRANCHES = 20

# --------------------------------------------------
# INDIAN LOCATIONS
# --------------------------------------------------

locations = [
    ("Delhi", "Delhi", "110001"),
    ("Mumbai", "Maharashtra", "400001"),
    ("Pune", "Maharashtra", "411001"),
    ("Lucknow", "Uttar Pradesh", "226001"),
    ("Kanpur", "Uttar Pradesh", "208001"),
    ("Jaipur", "Rajasthan", "302001"),
    ("Kota", "Rajasthan", "324001"),
    ("Bengaluru", "Karnataka", "560001"),
    ("Hyderabad", "Telangana", "500001"),
    ("Chennai", "Tamil Nadu", "600001"),
    ("Kolkata", "West Bengal", "700001"),
    ("Ahmedabad", "Gujarat", "380001"),
    ("Bhopal", "Madhya Pradesh", "462001"),
    ("Patna", "Bihar", "800001"),
    ("Indore", "Madhya Pradesh", "452001"),
    ("Noida", "Uttar Pradesh", "201301"),
    ("Gurugram", "Haryana", "122001"),
    ("Surat", "Gujarat", "395001"),
    ("Nagpur", "Maharashtra", "440001"),
    ("Chandigarh", "Chandigarh", "160001")
]

# --------------------------------------------------
# SETS FOR UNIQUE VALUES
# --------------------------------------------------

used_branch_codes = set()
used_ifsc_codes = set()
used_contacts = set()
used_emails = set()

branches = []


# --------------------------------------------------
# GENERATE UNIQUE BRANCH CODE
# --------------------------------------------------

def generate_branch_code(branch_number):

    branch_code = f"BR{branch_number:04d}"

    while branch_code in used_branch_codes:
        branch_number += 1
        branch_code = f"BR{branch_number:04d}"

    used_branch_codes.add(branch_code)

    return branch_code


# --------------------------------------------------
# GENERATE UNIQUE IFSC CODE
# --------------------------------------------------

def generate_ifsc(branch_number):

    # SBI-style synthetic IFSC format
    ifsc_code = f"VMBK0{branch_number:05d}"

    while ifsc_code in used_ifsc_codes:

        branch_number += 1

        ifsc_code = f"VMBK0{branch_number:05d}"

    used_ifsc_codes.add(ifsc_code)

    return ifsc_code


# --------------------------------------------------
# GENERATE UNIQUE CONTACT NUMBER
# --------------------------------------------------

def generate_contact():

    while True:

        contact = str(
            random.randint(7000000000, 9999999999)
        )

        if contact not in used_contacts:

            used_contacts.add(contact)

            return contact


# --------------------------------------------------
# GENERATE UNIQUE EMAIL
# --------------------------------------------------

def generate_email(branch_number):

    email = f"branch{branch_number:03d}@vmbank.com"

    while email in used_emails:

        branch_number += 1

        email = f"branch{branch_number:03d}@vmbank.com"

    used_emails.add(email)

    return email


# --------------------------------------------------
# GENERATE BRANCHES
# --------------------------------------------------

for i in range(1, TOTAL_BRANCHES + 1):

    # -----------------------------
    # Location
    # -----------------------------

    city, state, pincode = locations[i - 1]

    # -----------------------------
    # Unique values
    # -----------------------------

    branch_code = generate_branch_code(i)

    ifsc_code = generate_ifsc(i)

    contact_number = generate_contact()

    branch_email = generate_email(i)

    # -----------------------------
    # Branch status
    # -----------------------------

    branch_status = random.choices(
        ["Active", "Inactive"],
        weights=[95, 5]
    )[0]

    # -----------------------------
    # Branch record
    # -----------------------------

    branch = {

        # AUTO_INCREMENT in MySQL
        # So branch_id is NOT included

        "branch_code": branch_code,

        # Manager will be assigned later
        "branch_manager_id": None,

        "building_no": str(
            random.randint(1, 999)
        ),

        "street": fake.street_name(),

        "area": fake.city_suffix(),

        "city": city,

        "state": state,

        "pincode": pincode,

        "ifsc_code": ifsc_code,

        "contact_number": contact_number,

        "branch_email": branch_email,

        "branch_status": branch_status,

        "created_at": fake.date_time_between(
            start_date="-5y",
            end_date="now"
        ),

        # Extra column present in your table
        "contact_number_branch": contact_number
    }

    branches.append(branch)


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(branches)


# --------------------------------------------------
# SAVE CSV
# --------------------------------------------------

output_file = (
    Path(__file__).parent
    / "branches.csv"
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
print("BRANCH DATA GENERATION COMPLETED")
print("=" * 60)

print(f"Total branches : {len(df)}")

print()
print("Data shape:")
print(df.shape)

print()
print("Missing values:")
print(df.isnull().sum())

print()
print("Duplicate branch codes:")
print(
    df["branch_code"].duplicated().sum()
)

print()
print("Duplicate IFSC codes:")
print(
    df["ifsc_code"].duplicated().sum()
)

print()
print("Duplicate contact numbers:")
print(
    df["contact_number"].duplicated().sum()
)

print()
print("Duplicate branch emails:")
print(
    df["branch_email"].duplicated().sum()
)

print()
print("CSV file created:")
print(output_file)

print()
print("First 5 records:")
print(df.head())

print()
print("=" * 60)
print("BRANCH CSV SAVED SUCCESSFULLY!")
print("=" * 60)