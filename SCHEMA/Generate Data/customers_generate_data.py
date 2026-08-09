from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# --------------------------------------------------
# BASIC SETUP
# --------------------------------------------------

fake = Faker("en_IN")

TOTAL_CUSTOMERS = 1000

# --------------------------------------------------
# INDIAN LOCATIONS
# --------------------------------------------------

locations = [
    ("Delhi", "Delhi", "110001"),
    ("Mumbai", "Maharashtra", "400001"),
    ("Pune", "Maharashtra", "411001"),
    ("Lucknow", "Uttar Pradesh", "226001"),
    ("Kanpur", "Uttar Pradesh", "208001"),
    ("Sitapur", "Uttar Pradesh", "261001"),
    ("Jaipur", "Rajasthan", "302001"),
    ("Kota", "Rajasthan", "324001"),
    ("Bengaluru", "Karnataka", "560001"),
    ("Hyderabad", "Telangana", "500001"),
    ("Chennai", "Tamil Nadu", "600001"),
    ("Kolkata", "West Bengal", "700001"),
    ("Ahmedabad", "Gujarat", "380001"),
    ("Bhopal", "Madhya Pradesh", "462001"),
    ("Patna", "Bihar", "800001")
]

# --------------------------------------------------
# OCCUPATIONS
# --------------------------------------------------

occupations = [
    "Software Engineer",
    "Teacher",
    "Business Owner",
    "Doctor",
    "Lawyer",
    "Accountant",
    "Government Employee",
    "Sales Executive",
    "Marketing Manager",
    "Student",
    "Bank Employee",
    "Self Employed",
    "Consultant",
    "Engineer",
    "HR Manager"
]

# --------------------------------------------------
# SETS FOR UNIQUE VALUES
# --------------------------------------------------

used_mobiles = set()
used_emails = set()
used_pans = set()

customers = []


# --------------------------------------------------
# GENERATE UNIQUE MOBILE NUMBER
# --------------------------------------------------

def generate_mobile():

    while True:

        mobile = str(
            random.randint(6000000000, 9999999999)
        )

        if mobile not in used_mobiles:

            used_mobiles.add(mobile)

            return mobile


# --------------------------------------------------
# GENERATE UNIQUE EMAIL
# --------------------------------------------------

def generate_email(name, number):

    clean_name = name.lower().replace(" ", ".")

    email = f"{clean_name}{number}@gmail.com"

    while email in used_emails:

        number += 1

        email = f"{clean_name}{number}@gmail.com"

    used_emails.add(email)

    return email


# --------------------------------------------------
# GENERATE UNIQUE PAN NUMBER
# --------------------------------------------------

def generate_pan():

    while True:

        first_five_letters = "".join(
            random.choices(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                k=5
            )
        )

        four_digits = "".join(
            random.choices(
                "0123456789",
                k=4
            )
        )

        last_letter = random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

        pan = (
            first_five_letters
            + four_digits
            + last_letter
        )

        if pan not in used_pans:

            used_pans.add(pan)

            return pan


# --------------------------------------------------
# GENERATE DATE OF BIRTH
# --------------------------------------------------

def random_dob():

    start_date = datetime(1970, 1, 1)

    end_date = datetime(2005, 12, 31)

    days_difference = (
        end_date - start_date
    ).days

    random_days = random.randint(
        0,
        days_difference
    )

    return (
        start_date
        + timedelta(days=random_days)
    ).date()


# --------------------------------------------------
# GENERATE CUSTOMERS
# --------------------------------------------------

for i in range(TOTAL_CUSTOMERS):

    # -----------------------------
    # Gender
    # -----------------------------

    gender = random.choices(
        ["Male", "Female", "Other"],
        weights=[48, 48, 4]
    )[0]

    # -----------------------------
    # Name
    # -----------------------------

    if gender == "Male":

        customer_name = fake.name_male()

    elif gender == "Female":

        customer_name = fake.name_female()

    else:

        customer_name = fake.name()

    # -----------------------------
    # Location
    # -----------------------------

    city, state, pincode = random.choice(
        locations
    )

    # -----------------------------
    # Unique Values
    # -----------------------------

    mobile_number = generate_mobile()

    email = generate_email(
        customer_name,
        i
    )

    pan_number = generate_pan()

    # -----------------------------
    # KYC Status
    # -----------------------------

    kyc_status = random.choices(
        ["Pending", "Verified", "Rejected"],
        weights=[10, 85, 5]
    )[0]

    # -----------------------------
    # Customer Status
    # -----------------------------

    customer_status = random.choices(
        ["Active", "Inactive", "Blocked"],
        weights=[90, 7, 3]
    )[0]

    # -----------------------------
    # Login Status
    # -----------------------------

    if customer_status == "Blocked":

        login_status = "Blocked"

    else:

        login_status = random.choices(
            ["Active", "Blocked"],
            weights=[97, 3]
        )[0]

    # -----------------------------
    # Customer Record
    # -----------------------------

    customer = {

        "customer_name": customer_name,

        "mobile_number": mobile_number,

        "email": email,

        "dob": random_dob(),

        "gender": gender,

        "occupation": random.choice(
            occupations
        ),

        "house_no": str(
            random.randint(1, 999)
        ),

        "street": fake.street_name(),

        "area": fake.city_suffix(),

        "city": city,

        "state": state,

        "pincode": pincode,

        "country": "India",

        "pan_number": pan_number,

        "kyc_status": kyc_status,

        "created_at": fake.date_time_between(
            start_date="-5y",
            end_date="now"
        ),

        "customer_status": customer_status,

        "login_status": login_status
    }

    customers.append(customer)


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(customers)


# --------------------------------------------------
# SAVE CSV IN SAME FOLDER AS PYTHON FILE
# --------------------------------------------------

output_file = (
    Path(__file__).parent
    / "customers.csv"
)

df.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# VERIFICATION
# --------------------------------------------------

print()
print("=" * 50)
print("CUSTOMER DATA GENERATION COMPLETED")
print("=" * 50)

print(f"Total customers : {len(df)}")

print(
    f"CSV file created : {output_file}"
)

print()
print("First 5 records:")
print(df.head())

print()
print("CSV file saved successfully!")
print("=" * 50)

print(df.shape)

print(df.isnull().sum())

print(df["mobile_number"].duplicated().sum())

print(df["email"].duplicated().sum())

print(df["pan_number"].duplicated().sum())