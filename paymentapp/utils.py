from base64 import b64encode
from hashlib import sha256
import hmac
from payment_project import settings
from django.shortcuts import redirect
import requests


def create_sha256_signature(key, message):
    digest = hmac.new(
        key.encode(),
        msg=message.encode(),
        digestmod=sha256,
    ).digest()
    return b64encode(digest).decode()


def sign_fields(fields):
    data_to_sign = []
    for key, value in fields.items():
        if (
            key == "card_type"
            or key == "card_number"
            or key == "card_expiry_date"
            or key == "signature"
        ):
            continue
        data_to_sign.append(f"{key}={value}")

    context = {}
    fields["signature"] = create_sha256_signature(
        settings.CYBERSOURCE_SECRET_KEY, ",".join(data_to_sign)
    )
    context["url"] = settings.CYBERSOURCE_TEST_URL
    context["data"] = fields
    return context

    # POST request -- for test

    # url = requests.post(settings.CYBERSOURCE_TEST_URL, data=fields).content
    # return url
