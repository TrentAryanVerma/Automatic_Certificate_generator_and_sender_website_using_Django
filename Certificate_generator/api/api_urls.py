from django.urls import path
from .api_views import CertificateGenerateAPI

urlpatterns = [
    path('send-certificates/', CertificateGenerateAPI.as_view(), name='api-send-certificates'),
]
