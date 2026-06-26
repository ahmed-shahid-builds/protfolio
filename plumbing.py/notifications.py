import smtplib
import os
from email.mime.text import MIMEText

# ----------------------------------------------------------------------
# EMAIL SETUP — read me before running
# ----------------------------------------------------------------------
# Gmail will NOT let you log in with your normal password from code.
# You need a 16-character "App Password":
#
#   1. Go to https://myaccount.google.com/security
#   2. Turn on 2-Step Verification (if not already on)
#   3. Go to https://myaccount.google.com/apppasswords
#   4. Create an app password for "Mail" and copy the 16-character code
#
# Then set these two as environment variables before running the app
# (don't hardcode your password in the code):
#
#   Windows (cmd):   set EMAIL_ADDRESS=youraddress@gmail.com
#                     set EMAIL_PASSWORD=xxxxxxxxxxxxxxxx
#   Mac/Linux:        export EMAIL_ADDRESS=youraddress@gmail.com
#                     export EMAIL_PASSWORD=xxxxxxxxxxxxxxxx
#
# If these aren't set, booking will still work fine — it just won't
# send you an email, and it will print a warning in the terminal instead.
# ----------------------------------------------------------------------

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
NOTIFY_TO = os.environ.get("NOTIFY_TO", "ahmed.shahid.builds@gmail.com")


def send_booking_notification(name, phone, date, time, service, message):
    subject = f"New Booking: {name} - {service} ({time})"
    body = (
        f"A new appointment was booked on Jake's Plumbing website.\n\n"
        f"Name: {name}\n"
        f"Phone: {phone}\n"
        f"Date: {date}\n"
        f"Time Slot: {time}\n"
        f"Service: {service}\n"
        f"Message: {message or '(none)'}\n"
    )

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("[email] EMAIL_ADDRESS / EMAIL_PASSWORD not set — skipping email, booking still saved.")
        print(body)
        return False

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = NOTIFY_TO

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"[email] Failed to send notification email: {e}")
        return False
