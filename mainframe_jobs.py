import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

EMAIL_TO = "shabnac11@gmail.com"
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_PASS = os.environ["EMAIL_PASS"]

jobs = []

def search_indeed():
    url = "https://www.indeed.com/jobs?q=mainframe&fromage=3"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.select(".job_seen_beacon"):
        title = job.select_one("h2 span")
        link = job.select_one("a")
        company = job.select_one(".companyName")

        if title and link:
            jobs.append(
                f"{title.text.strip()} - {company.text.strip() if company else ''}\nhttps://www.indeed.com{link.get('href')}\n"
            )

def search_dice():
    url = "https://www.dice.com/jobs?q=mainframe&filters.postedDate=THREE"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for job in soup.select("a.card-title-link"):
        jobs.append(
            f"{job.text.strip()}\nhttps://www.dice.com{job.get('href')}\n"
        )

def send_email():
    if not jobs:
        return

    body = "Mainframe jobs posted in last 3 days\n\n"
    body += "\n".join(jobs)

    msg = MIMEText(body)
    msg["Subject"] = "Daily Mainframe Jobs"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_FROM, EMAIL_PASS)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()

search_indeed()
search_dice()
send_email()

def send_email():
    if not jobs:
        body = "No mainframe jobs found in the last 3 days on Indeed or Dice."
    else:
        body = "Mainframe jobs posted in last 3 days\n\n"
        body += "\n".join(jobs)

    msg = MIMEText(body)
    msg["Subject"] = "Daily Mainframe Jobs"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_FROM, EMAIL_PASS)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()
