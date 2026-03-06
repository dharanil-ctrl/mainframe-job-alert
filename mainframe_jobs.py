import os
import smtplib
import requests
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_TO = "shabnac11@gmail.com"

rss_url = "https://www.indeed.com/rss?q=mainframe&fromage=3"

response = requests.get(rss_url)
root = ET.fromstring(response.content)

jobs = []

for item in root.findall(".//item"):
    title = item.find("title").text
    link = item.find("link").text
    jobs.append(f"{title}\n{link}\n")

if not jobs:
    body = "No mainframe jobs found in last 3 days."
else:
    body = "Mainframe Jobs (last 3 days)\n\n" + "\n".join(jobs)

msg = MIMEText(body)
msg["Subject"] = "Daily Mainframe Jobs"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL_FROM, EMAIL_PASS)
server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
server.quit()
