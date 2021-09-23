# Import Libraries
import os

## For Web Scraping
import requests
from bs4 import BeautifulSoup

## For Email Sending
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## For Date-Time
from datetime import datetime

now = datetime.now()

content = ""


# Extracting News
def extract_news():
    print("Extracting Hacker News Stories...")
    cnt = ""
    cnt += ("<b>HackerNews Top Stories:</b>\n" + "<br>" + "-" * 50 + "\n<br>")
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    contents = response.content
    soup = BeautifulSoup(contents, "html.parser")
    # news = soup.findAll("td", attrs={"class": "title", "valign": ""})
    # print(news)
    for i, tag in enumerate(soup.findAll("td", attrs={"class": "title", "valign": ""})):
        cnt += ((str(i + 1) + "::" + tag.text + "\n" + "<br>") if tag.text != "More" else "")
    return cnt


cnt = extract_news()
content += cnt
content += ("<br>-----------<br>")
content += ("<br><br>End of Message")

# Sending Email
SERVER = "smtp.gmail.com"
PORT = 587
FROM = os.environ.get("email")
PASSWORD = os.environ.get("password")
TO = [] # Enter your list of senders

msg = MIMEMultipart()

msg["Subject"] = f"Top Hacker News Story ({now.strftime('%A %d-%m-%Y')})"
msg.attach(MIMEText(content, "html"))

## Authenticate
server = smtplib.SMTP(SERVER, PORT)
server.ehlo()
server.starttls()
server.login(FROM, PASSWORD)

## Sending Mail
for mail in TO:
    server.sendmail(FROM, mail, msg.as_string())
    print(f"Email Sent to {mail}")

server.quit()