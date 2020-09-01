import smtplib

from string import Template
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADRESS = "eliottarloveyrier@live.fr"
def main():
    s = smtplib.SMTP(host="SMTP.office365.com", port=587)
    s.starttls()
    s.login(MY_ADRESS, getpass("Enter password :"))
    msg = MIMEMultipart()
    msg["From"] = MY_ADRESS
    msg["To"] = MY_ADRESS
    msg["Subject"] = "Hello, world"
    msg.attach(MIMEText("Hello, world. it's been a while. here i am sending emails to myself.."))

    s.send_message(msg)
    s.quit()


if __name__ == "__main__":
    main()