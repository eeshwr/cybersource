import datetime
from base64 import b64encode
from hashlib import sha256
import hmac

from payment_project import settings


def create_sha256_signature(key, message):
    """
    Signs an HMAC SHA-256 signature to a message with Base 64
    encoding. This is required by CyberSource.
    """
    digest = hmac.new(
        key.encode(),
        msg=message.encode(),
        digestmod=sha256,
    ).digest()
    return b64encode(digest).decode()


def sign_fields(fields):
    """
    Builds the list of file names and data to sign, and created the
    signature required by CyberSource.
    """

    signed_field_names = []
    data_to_sign = []
    for key, value in fields.items():
        signed_field_names.append(key)

    # After adding all the included fields, we need to also add
    # `unsigned_field_names` and `signed_field_names` to the data
    # to be signed.
    signed_field_names.insert(2, "signed_field_names")
    signed_field_names.insert(3, "unsigned_field_names")

    unsigned_field_names = ["card_type", "card_number", "card_expiry_date"]
    unsigned = ",".join(unsigned_field_names)
    signed = ",".join(signed_field_names)

    # Build the fields into a list to sign, which will become
    # a string when joined by a comma
    for key, value in fields.items():
        data_to_sign.append(f"{key}={value}")

    data_to_sign.insert(2, f"singed_field_names={signed}")
    data_to_sign.insert(3, f"unsinged_field_names={unsigned}")
    fields["signed_field_names"] = signed
    fields["unsigned_field_names"] = unsigned

    context = {}
    context["fields"] = fields
    context["signature"] = create_sha256_signature(
        settings.CYBERSOURCE_SECRET_KEY,
        ",".join(data_to_sign),
    )
    context["url"] = settings.CYBERSOURCE_TEST_URL

    return context
