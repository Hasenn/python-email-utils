import smtplib
import argparse
import ntpath
from string import Template

from getpass import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders 

MY_ADRESS = "eliottarloveyrier@live.fr"
MY_NAME = "Eliott Veyrier"
SMPTP_HOST = "SMTP.office365.com"
SMPTP_PORT = 587

def read_template(filename):
    with open(filename, 'r', encoding ='utf-8') as f:
        content = f.read()
    return Template(content)

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="""\
        Mails a document to someone
        """)
    parser.add_argument("path", 
                        help="""Mail the file at the specified path""")
    parser.add_argument("recipient", 
                        help="""Mail the file to the specified email""")
    parser.add_argument("doc_name", default="Le document demmandé")
    args = parser.parse_args()

    # Read template and format it
    message_template = read_template(ntpath.dirname(__file__) + "/" + "send_doc.template")
    message = message_template.substitute(DOC_NAME=args.doc_name, MY_NAME = MY_NAME)
    # Create message
    msg = MIMEMultipart()
    msg["From"] = MY_ADRESS
    msg["To"] = args.recipient
    msg["Subject"] = args.doc_name
    # Attach the main body
    msg.attach(MIMEText(message,"plain"))
    # Parse file into MIMEBase Object
    p = MIMEBase('application', 'octet-stream')
    with open(args.path, 'rb') as attachment:
        p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % ntpath.basename(args.path))
    # Attach file
    msg.attach(p)
    # Set up SMTP object
    s = smtplib.SMTP(host=SMPTP_HOST, port=SMPTP_PORT)
    s.starttls()
    s.login(MY_ADRESS, getpass("Enter password :"))
    # Send the message
    s.send_message(msg)
    s.quit()
    print("Sent message : \n----------------------\n" + message)

    


if __name__ == "__main__":
    main()