from django.urls import path
from .views import UserFormView, GeneratePDFView, HealthCheckView

app_name = 'form_pdf'

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('', UserFormView.as_view(), name='form'),
    path('generate-pdf/', GeneratePDFView.as_view(), name='generate_pdf'),
]

