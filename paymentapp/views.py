# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from paymentapp.models import CyberSourceTransaction, Client
from uuid import uuid4
from payment_project.settings import (
    CYBERSOURCE_PROFILE_ID,
    CYBERSOURCE_ACCESS_KEY,
)
from paymentapp.utils import sign_fields
from datetime import datetime
from rest_framework import status
from django.shortcuts import render
from random import randint


@api_view(["POST"])
def sign(request):
    transaction_uuid = uuid4()
    transaction = CyberSourceTransaction()
    transaction.transaction_id = transaction_uuid
    transaction.first_name = request.data.get("first_name")
    transaction.last_name = request.data.get("last_name")
    transaction.amount = request.data.get("amount")
    transaction.email = request.data.get("email")

    client = Client.objects.get(
        id="8d241c06-364b-40bc-8b85-34d8543eb230",
    )
    transaction.client = client
    transaction.payment_status = "PENDING"
    transaction.save()

    # Fields to pass to CyberSource
    signed = "access_key,profile_id,signed_field_names,unsigned_field_names,locale,transaction_uuid,signed_date_time,transaction_type,reference_number,amount,currency,payment_method,bill_to_forename,bill_to_surname,bill_to_email,bill_to_phone,bill_to_address_line1,bill_to_address_city,bill_to_address_state,bill_to_address_country,bill_to_address_postal_code,auth_trans_ref_no"
    unsigned = "card_type,card_number,card_expiry_date"
    fields = {}
    fields["access_key"] = CYBERSOURCE_ACCESS_KEY
    fields["profile_id"] = CYBERSOURCE_PROFILE_ID
    fields["signed_field_names"] = signed
    fields["unsigned_field_names"] = unsigned
    fields["locale"] = "en-us"
    fields["transaction_uuid"] = transaction_uuid
    fields["signed_date_time"] = (
        str(datetime.utcnow().isoformat(timespec="seconds")) + "Z"
    )
    fields["transaction_type"] = "sale"
    fields["reference_number"] = str(
        (lambda x: randint(10 ** (x - 1), (10 ** x) - 1))(10)
    )
    fields["amount"] = request.data.get("amount")
    fields["currency"] = "USD"
    fields["payment_method"] = "card"
    fields["bill_to_forename"] = request.data.get("first_name")
    fields["bill_to_surname"] = request.data.get("last_name")
    fields["bill_to_email"] = request.data.get("email")
    fields["bill_to_phone"] = "1111111111"
    fields["bill_to_address_line1"] = "N/A"
    fields["bill_to_address_city"] = "N/A"
    fields["bill_to_address_state"] = "N/A"
    fields["bill_to_address_country"] = "NP"
    fields["bill_to_address_postal_code"] = "N/A"
    fields["card_type"] = "001"
    fields["card_number"] = ""
    fields["card_expiry_date"] = ""
    fields["signature"] = ""
    fields["auth_trans_ref_no"] = str(
        (lambda x: randint(10 ** (x - 1), (10 ** x) - 1))(20)
    )
    data = sign_fields(fields)

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
def webhook(request):
    transaction = CyberSourceTransaction.objects.get(
        transaction_id=request.data.get("req_transaction_uuid"),
    )
    transaction.cybersource_response_date = datetime.utcnow()
    decision = request.data.get("decision").upper()
    transaction.payment_status = decision
    transaction.transaction_reason_code = request.data.get("reason_code")
    transaction.transaction_message = request.data.get("message")
    transaction.save()
    return Response(status=status.HTTP_200_OK)


# @api_view(["POST"])
# def sign2(request):

#     client = Client.objects.get(
#         id="8d241c06-364b-40bc-8b85-34d8543eb230",
#     )

#     transaction_uuid = uuid4()
#     transaction = CyberSourceTransaction()
#     transaction.transaction_id = transaction_uuid
#     transaction.first_name = request.data.get("first_name")
#     transaction.last_name = request.data.get("last_name")
#     transaction.amount = request.data.get("amount")
#     transaction.email = request.data.get("email")
#     transaction.client = client
#     transaction.payment_status = "PENDING"
#     transaction.save()

#     # Fields to pass to CyberSource
#     signed = "access_key,profile_id,signed_field_names,unsigned_field_names,locale,transaction_uuid,signed_date_time,transaction_type,reference_number,amount,currency,payment_method"
#     unsigned = "card_type,card_number,card_expiry_date"
#     fields = {}
#     fields["access_key"] = CYBERSOURCE_ACCESS_KEY
#     fields["profile_id"] = CYBERSOURCE_PROFILE_ID
#     fields["signed_field_names"] = signed
#     fields["unsigned_field_names"] = unsigned
#     fields["locale"] = "en-us"
#     fields["transaction_uuid"] = transaction_uuid
#     fields["signed_date_time"] = (
#         str(datetime.utcnow().isoformat(timespec="seconds")) + "Z"
#     )
#     fields["transaction_type"] = "sale"
#     fields["reference_number"] = "7861063289"
#     fields["amount"] = "100.00"
#     fields["currency"] = "USD"
#     fields["payment_method"] = "card"
#     fields["card_type"] = "001"
#     fields["card_number"] = ""
#     fields["card_expiry_date"] = ""
#     fields["signature"] = ""
#     return Response(data=sign_fields(fields), status=status.HTTP_200_OK)


@api_view(["GET"])
def home(request):
    return render(request, template_name="index.html")
