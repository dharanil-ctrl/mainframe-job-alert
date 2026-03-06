import os
import smtplib
import requests
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# Email configuration
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_TO = "shabnac11@gmail.com"

# Indeed RSS feed (jobs posted within last 3 days)
RSS_URL = "https://www.indeed.com/rss?q=mainframe&fromage=3"

def get_jobs():
    jobs = []

    response = requests.get(RSS_URL, timeout=30)
    soup = BeautifulSoup(response.content, "xml")

    for item in soup.find_all("item"):
        title = item.title.text.strip()
        link = item.link.text.strip()
        pub_date = item.pubDate.text.strip()

        job_text = f"{title}\n{pub_date}\n{link}\n"
        jobs.append(job_text)

    return jobs


def send_email(job_list):

    if not job_list:
        body = "No mainframe jobs found on Indeed in the last 3 days."
    else:
        body = "Mainframe Jobs Posted in Last 3 Days\n\n"
        body += "\n".join(job_list)

    msg = MIMEText(body)
    msg["Subject"] = "Daily Mainframe Job Alerts"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())


def main():
    jobs = get_jobs()
    send_email(jobs)


if __name__ == "__main__":
    main()
