import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from report import build_report

# Read email settings from the .env file
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")


def send_report(expenses):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not EMAIL_TO:
        print("Email settings are missing in the .env file.")
        return

    message = EmailMessage()
    message["Subject"] = "Your Expense Report"
    message["From"] = EMAIL_ADDRESS
    message["To"] = EMAIL_TO
    message.set_content(build_report(expenses))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
        print(f"Report sent to {EMAIL_TO}!")
    except smtplib.SMTPAuthenticationError:
        print("Login failed. Check your email and app password in the .env file.")
    except (smtplib.SMTPException, OSError) as error:
        print(f"Could not send email: {error}")