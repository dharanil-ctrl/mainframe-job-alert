import os
import smtplib
import requests
from email.mime.text import MIMEText

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_TO = "shabnac11@gmail.com"

indeed_feed = "https://www.indeed.com/rss?q=mainframe&fromage=3"
dice_feed = "https://job-openings.monster.com/search?q=mainframe&cy=us&tm=3&rss=1"

def fetch_feed(url):
    try:
        r = requests.get(url, timeout=30)
        return r.text
    except:
        return "Failed to retrieve jobs."

def send_email(content):

    msg = MIMEText(content)

    msg["Subject"] = "Daily Mainframe Jobs"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

def main():

    indeed_jobs = fetch_feed(indeed_feed)
    dice_jobs = fetch_feed(dice_feed)

    body = f"""
Mainframe Jobs (Last 3 Days)

Indeed Feed
-----------
{indeed_jobs[:4000]}

Dice Feed
---------
{dice_jobs[:4000]}
"""

    send_email(body)

if __name__ == "__main__":
    main()
