from django.urls import path
from .views import UserFormView, HealthCheckView

app_name = 'form_pdf'

urlpatterns = [
    path('healthcheck', HealthCheckView.as_view(), name='healthcheck'),
    path('', UserFormView.as_view(), name='form'),
]

