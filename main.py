
import datetime
from zoneinfo import ZoneInfo
import pandas
import random
import smtplib
import os

# ==============================
# PART 1: Get Gmail Credentials
# ==============================

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

if not my_email or not password:
    raise ValueError("Gmail credentials are missing!")

# ==============================
# PART 2: Read Birthday Data
# ==============================

data = pandas.read_csv("birthdays.csv")

# ==============================
# PART 3: Check Today's Birthday
# Bangladesh Time
# ==============================

today = datetime.datetime.now(ZoneInfo("Asia/Dhaka"))
today_tuple = (today.month, today.day)

birthdays_today = data[
    (data["month"] == today.month) &
    (data["day"] == today.day)
]

if not birthdays_today.empty:

    # ==============================
    # PART 4: Generate Birthday Letter
    # ==============================

    for _, birthday_person in birthdays_today.iterrows():

        random_letter = random.randint(1, 3)

        file_path = f"letter_templates/letter_{random_letter}.txt"

        with open(file_path, encoding="utf-8") as letter_file:
            letter_contents = letter_file.read()

        personalized_letter = letter_contents.replace(
            "[NAME]",
            str(birthday_person["name"])
        )

        # ==============================
        # PART 5: Send Birthday Email
        # ==============================

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:

            connection.starttls()

            connection.login(my_email, password)

            connection.sendmail(
                from_addr=my_email,
                to_addrs=birthday_person["email"],
                msg=f"Subject: Happy Birthday!\n\n{personalized_letter}"
            )

        print(f"Birthday email sent to {birthday_person['name']}!")

else:
    print("No birthdays today.")

print("Birthday Wisher finished!")
