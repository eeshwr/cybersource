from django.urls import path
from paymentapp.views import sign, webhook

app_name = "paymentapp"
urlpatterns = [
    path("sign/", sign, name="sign"),
    path("webhook/", webhook, name="webhook"),
]
