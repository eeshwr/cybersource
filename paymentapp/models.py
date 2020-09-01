from django.db import models


class CyberSourceTransaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=32)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=100)
    cybersource_response_date = models.DateTimeField(null=True, blank=True)
