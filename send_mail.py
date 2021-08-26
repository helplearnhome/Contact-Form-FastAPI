import smtplib
from email.message import EmailMessage
import os
'''
To update .env in deta.sh  use these commands deta update -e <env_file_name> and 
uncomment below two lines while deploying because dotenv load module is not used by deta.sh
The update command is used to update env not load_dotenvv

These two below commands are required to update environmental variables in local machine.
If you want to run the fastapi in local server using uvicorn
'''
# from dotenv import load_dotenv
# load_dotenv()


class SendEmail:
    SMTP_GMAIL_SERVER = "smtp.gmail.com"
    SMTP_GMAIL_PORT = 465
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email= os.getenv("RECEIVER_EMAIL")
    def __init__(self,first_name,last_name,email_to_contact,subject,message_body):
        self.first_name = first_name
        self.last_name = last_name
        self.email_to_contact = email_to_contact
        self.subject="Contact Form: "+subject
        self.message_body = f"Name: {first_name} {last_name}\n\nEmail: {email_to_contact} \n\n{message_body}"
    def send_email(self):
        self.msg = EmailMessage()
        self.msg["From"] = self.sender_email
        self.msg["To"] = self.receiver_email
        self.msg['Subject'] = self.subject
        self.msg.set_content(self.message_body)

        server = smtplib.SMTP_SSL(self.SMTP_GMAIL_SERVER,self.SMTP_GMAIL_PORT)
        server.login(self.sender_email,self.sender_password)
        server.send_message(self.msg)
        server.quit