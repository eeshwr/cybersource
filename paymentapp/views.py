# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from paymentapp.models import CyberSourceTransaction
from uuid import uuid4
from payment_project.settings import CYBERSOURCE_PROFILE_ID, CYBERSOURCE_ACCESS_KEY
from paymentapp.utils import sign_fields
from datetime import datetime
from rest_framework import status


@api_view(["POST"])
def sign(request):
    transaction_uuid = uuid4().hex
    transaction = CyberSourceTransaction()
    transaction.uuid = transaction_uuid
    transaction.first_name = request.data.get("first_name")
    transaction.last_name = request.data.get("last_name")
    transaction.amount = request.data.get("amount")
    transaction.email = request.data.get("email")
    transaction.payment_status = "PENDING"
    transaction.save()

    # Fields to pass to CyberSource - see manual for a full list
    fields = {}
    fields["access_key"] = CYBERSOURCE_ACCESS_KEY
    fields["profile_id"] = CYBERSOURCE_PROFILE_ID
    fields["locale"] = "en-us"
    fields["transaction_uuid"] = transaction_uuid
    fields["signed_date_time"] = (
        str(datetime.utcnow().isoformat(timespec="seconds")) + "Z"
    )
    fields["transaction_type"] = "sale"
    fields["reference_number"] = uuid4().hex
    fields["amount"] = request.data.get("amount")
    fields["currency"] = "USD"
    fields["payment_method"] = "card"
    fields["bill_to_forename"] = request.data.get("first_name")
    fields["bill_to_surname"] = request.data.get("last_name")
    fields["bill_to_email"] = request.data.get("email")
    fields["bill_to_phone"] = "9849066741"
    fields["bill_to_address_line1"] = "Dhapasi"
    fields["bill_to_address_city"] = "Kathmandu"
    fields["bill_to_address_state"] = "N/A"
    fields["bill_to_address_country"] = "NP"
    fields["bill_to_address_postal_code"] = "N/A"
    fields["auth_trans_ref_no"] = uuid4().hex
    data = sign_fields(fields)

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
def webhook(request):
    transaction = CyberSourceTransaction.objects.get(
        uuid=request.data.get("req_transaction_uuid"),
    )
    transaction.cybersource_response_date = datetime.utcnow()
    decision = request.data.get("decision").upper()
    transaction.payment_status = decision
    transaction.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def home(request):
    return Response(status=status.HTTP_200_OK)
