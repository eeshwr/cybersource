from django.urls import path
from paymentapp.views import sign, webhook, home

app_name = "paymentapp"
urlpatterns = [
    path("sign/", sign, name="sign"),
    path("webhook/", webhook, name="webhook"),
    path("home/", home, name="home"),
    path("", home, name="home"),
]
