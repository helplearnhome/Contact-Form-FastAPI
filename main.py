from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deta import Deta
from typing import Optional 
import send_mail

deta = Deta()

db = deta.Base("contact-form")

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


@app.get("/")
async def read_root():
    return {"greetings": "Welcome to the Bus Tracking API!"}

@app.get("/contactform")
async def get_form_details():
    return next(db.fetch())


@app.post("/contactform/")
async def post_form_details(contact_form_object: ContactForm):
    first_name = contact_form_object.first_name
    last_name = contact_form_object.last_name
    email_to_contact = contact_form_object.email_id
    subject= contact_form_object.subject
    message_body = contact_form_object.message_body
    send_mail_object = send_mail.SendEmail(
        first_name = first_name,
        last_name = last_name,
        email_to_contact=email_to_contact,
        subject=subject,
        message_body=message_body
    )
    send_mail_object.send_email()
    db.put(contact_form_object.dict())
    return next(db.fetch())[-1]
    
