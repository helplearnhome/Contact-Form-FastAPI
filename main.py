from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deta import Deta
from typing import Optional 
import send_mail

deta = Deta()

db_contact_form = deta.Base("contact-form")

db_sender_receiver_details = deta.Base("receiver-sender_details")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactForm(BaseModel):
    first_name: str=Form(...)
    last_name: str=Form(...)
    email_id: str=Form(...)
    subject: str=Form(...)
    message_body: str=Form(...)

class SenderReceiverDetails(BaseModel):
    sender_email: Optional[str]=None
    receiver_email: Optional[str]=None

@app.get("/")
async def read_root():
    return {"greetings": "Welcome to the Contact Form API!"}

@app.get("/contact-form")
async def get_contact_form_details():
    return next(db_contact_form.fetch())

@app.post("/contact-form/")
async def post_contact_form_details(contact_form_object: ContactForm):
    first_name = contact_form_object.first_name
    last_name = contact_form_object.last_name
    email_to_contact = contact_form_object.email_id
    subject= contact_form_object.subject
    message_body = contact_form_object.message_body
    send_mail_object = send_mail.SendEmail()
    send_mail_object.send_email(
        first_name = first_name,
        last_name = last_name,
        email_to_contact=email_to_contact,
        subject=subject,
        message_body=message_body)
    db_contact_form.put(contact_form_object.dict())
    return next(db_contact_form.fetch())[-1]
    

@app.get("/sender-receiver-details")
async def get_sender_receiver_details():
    return next(db_sender_receiver_details.fetch())

@app.post("/sender-receiver-details/")
async def post_sender_receiver_details(sender_receiver_details: SenderReceiverDetails):
    # sender_email = sender_receiver_details.sender_email
    # receiver_email = sender_receiver_details.receiver_email
    # send_mail_object = send_mail.SendEmail()
    # send_mail_object.sender_receiver_details(sender_email=sender_email,receiver_email=receiver_email)
    db_sender_receiver_details.put(sender_receiver_details.dict())
    return next(db_sender_receiver_details.fetch())[-1]
