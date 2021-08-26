import os
class SendEmail:
    SMTP_GMAIL_SERVER = "smtp.gmail.com"
    SMTP_GMAIL_PORT = 465
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email= os.getenv("RECEIVER_EMAIL")
    # @classmethod
    def sender_receiver_details(cls,sender_email,receiver_email):
        if sender_email != None:
            cls.sender_email=sender_email
        if receiver_email != None:
            cls.receiver_email = receiver_email

    def send_email(self):
        print(self.sender_email)
        print(self.receiver_email)

send_email = SendEmail()
send_email.sender_receiver_details("rag","mag")
send_email.send_email()

send_email1 = SendEmail()
send_email1.send_email()
