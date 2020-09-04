from django.contrib import admin
from paymentapp.models import Client, CyberSourceTransaction

admin.site.register(Client)
admin.site.register(CyberSourceTransaction)

# Register your models here.
