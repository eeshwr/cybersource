# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from paymentapp.models import CyberSourceTransaction
from uuid import uuid4
from payment_project.settings import CYBERSOURCE_PROFILE_ID, CYBERSOURCE_ACCESS_KEY
from paymentapp.utils import sign_fields
from datetime import datetime
from decimal import Decimal


@api_view(["POST"])
def sign(request):
    transaction_uuid = uuid4().hex
    transaction = CyberSourceTransaction()
    transaction.transaction_uuid = transaction_uuid
    transaction.first_name = request.data.get("first_name")
    transaction.last_name = request.data.get("last_name")
    transaction.amount = request.data.get("amount")
    transaction.email = request.data.get("email")
    transaction.payment_status = "pending"
    transaction.save()

    # Fields to pass to CyberSource - see manual for a full list
    fields = {}
    fields["profile_id"] = CYBERSOURCE_PROFILE_ID
    fields["access_key"] = CYBERSOURCE_ACCESS_KEY
    fields["amount"] = request.data.get("amount")
    fields["transaction_uuid"] = transaction_uuid
    fields["bill_to_forename"] = request.data.get("first_name")
    fields["bill_to_surname"] = request.data.get("last_name")
    fields["bill_to_email"] = request.data.get("email")
    fields["locale"] = "en-us"
    fields["currency"] = "usd"
    fields["transaction_type"] = "sale"
    fields["reference_number"] = transaction.id
    data = sign_fields(fields)

    return Response(data=data)


@api_view(["POST"])
def webhook(request):
    # DECISION can be ACCEPT, REVIEW, DECLINE, ERROR, or CANCEL.
    # See page 152: http://apps.cybersource.com/library/documentation/dev_guides/Secure_Acceptance_WM/Secure_Acceptance_WM.pdf
    transaction = CyberSourceTransaction.objects.get(
        id=request.POST.get("req_reference_number"),
        uuid=request.POST.get("req_transaction_uuid"),
    )
    transaction.cybersource_response_date = datetime.utcnow()
    decision = request.POST.get("decision").upper()
    transaction.payment_status = decision
    transaction.save()
