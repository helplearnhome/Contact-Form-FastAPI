from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deta import Deta
from typing import Optional 
import send_mail
import id_handler

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
    contact_email: str=Form(...)
    subject: str=Form(...)
    message_body: str=Form(...)

class SenderReceiverDetails(BaseModel):
    sender_email: Optional[str]=None
    sender_password: Optional[str]=None
    receiver_email: Optional[str]=None

class SenderReceiverDetailswithID(BaseModel):
    id: int
    sender_email: Optional[str]=None
    sender_password: Optional[str]=None
    receiver_email: Optional[str]=None

@app.get("/")
async def read_root():
    return {"greetings": "Welcome to the Contact Form API!"}

@app.get("/contact-form")
async def get_contact_form_details():
    return next(db_contact_form.fetch())

@app.get("/contact-form/{contact_email}")
async def get_contact_form_details_by_contact_email_id(contact_email: str):
    return next(db_contact_form.fetch({"contact_email":contact_email}))

@app.post("/contact-form/")
async def post_contact_form_details(contact_form_object: ContactForm):
    first_name = contact_form_object.first_name
    last_name = contact_form_object.last_name
    contact_email = contact_form_object.contact_email
    subject= contact_form_object.subject
    message_body = contact_form_object.message_body
    send_mail_object = send_mail.SendEmail()
    send_mail_object.send_email(
        first_name = first_name,
        last_name = last_name,
        contact_email=contact_email,
        subject=subject,
        message_body=message_body)
    db_contact_form.put(contact_form_object.dict())
    return next(db_contact_form.fetch())[-1]


@app.delete("/contact-form-details/")
async def delete_sender_receiver_details(contact_email: Optional[str]=None):
    print(contact_email)
    json_item = next(db_contact_form.fetch())
    if not json_item:
        return {"task":"No Items to Delete"}

    if contact_email == None:
        pass
    else:
        json_item = next(db_contact_form.fetch({"contact_email":contact_email}))

    for dictionary in json_item:
        db_contact_form.delete(dictionary["key"])

    return {"task":"Deleted Successfully"}




@app.get("/sender-receiver-details")
async def get_sender_receiver_details():
    return next(db_sender_receiver_details.fetch())

@app.post("/sender-receiver-details/")
async def post_sender_receiver_details(sender_receiver_details: SenderReceiverDetails):

    sender_receiver_details_with_id = SenderReceiverDetailswithID(**sender_receiver_details.dict(),id=id_handler.auto_increment())
    db_sender_receiver_details.put(sender_receiver_details_with_id.dict())
    return {"task": "Added successfully", "item": sender_receiver_details_with_id.dict()}




@app.delete("/sender-receiver-details/delete-latest-added-item")
async def delete_sender_receiver_details_latest_added_item():
    json = next(db_sender_receiver_details.fetch())
    if not json:
        return {"task":"No Items to Delete"}
    

    latest_dictionary_item = id_handler.last_item()

    db_sender_receiver_details.delete(latest_dictionary_item["key"])

    return {"task":f"Deleted Successfully ", "Deleted item":latest_dictionary_item}



@app.delete("/sender-receiver-details/")
async def delete_sender_receiver_details_all_items():
    json = next(db_sender_receiver_details.fetch())
    if not json:
        return {"task":"No Items to Delete"}
    


    json_item = next(db_sender_receiver_details.fetch())

    for dictionary in json_item:
        db_sender_receiver_details.delete(dictionary["key"])

    return {"task":"Deleted Successfully "}