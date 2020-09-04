from django.urls import include, path
from django.contrib import admin


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("paymentapp.urls", namespace="paymentapp")),
    path("admin/", admin.site.urls),
]
