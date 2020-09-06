from django.urls import path
from paymentapp.views import sign, webhook, sign2, home

app_name = "paymentapp"
urlpatterns = [
    path("sign/", sign, name="sign"),
    path("webhook/", webhook, name="webhook"),
    path("sign2/", sign2, name="sign2"),
    path("home/", home, name="home"),
    path("", home, name="home"),
]
