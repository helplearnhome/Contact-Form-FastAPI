import os
# from dotenv import load_dotenv
# load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email= os.getenv("RECEIVER_EMAIL")
print(sender_email)


#one time you load dotenv enough for that shell or if no shell then permanent.