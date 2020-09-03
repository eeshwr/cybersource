from base64 import b64encode
from hashlib import sha256
import hmac

from payment_project import settings


def create_sha256_signature(key, message):
    digest = hmac.new(
        bytes(key, "utf-8"),
        bytes(message, "utf-8"),
        # key.encode(),
        # msg=message.encode(),
        digestmod=sha256,
    ).digest()
    return b64encode(digest)


def sign_fields(fields):
    data_to_sign = []
    for key, value in fields.items():
        data_to_sign.append(f"{key}={value}")
    context = {}
    context["fields"] = fields
    context["signature"] = create_sha256_signature(
        settings.CYBERSOURCE_SECRET_KEY,
        ",".join(data_to_sign),
    )
    context["url"] = settings.CYBERSOURCE_TEST_URL

    return context
