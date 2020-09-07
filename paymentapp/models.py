from django.db import models
from uuid import uuid4


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    name = models.CharField(max_length=100)


class CyberSourceTransaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    transaction_id = models.UUIDField(default=uuid4())
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=100)
    cybersource_response_date = models.DateTimeField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1)
    transaction_reason_code = models.IntegerField(default=000)
    transaction_message = models.TextField(default="")
