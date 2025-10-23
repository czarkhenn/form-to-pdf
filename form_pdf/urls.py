from django.urls import path
from .views import UserFormView, GeneratePDFView

app_name = 'form_pdf'

urlpatterns = [
    path('', UserFormView.as_view(), name='form'),
    path('generate-pdf/', GeneratePDFView.as_view(), name='generate_pdf'),
]

