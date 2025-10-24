from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .forms import UserDataForm
from .services import fill_pdf_form_with_data


class UserFormView(View):
    """
    Display the user data form and handle form submission.
    On valid submission, generate and download filled PDF.
    """

    template_name = 'form_pdf/form.html'

    def get(self, request):
        form = UserDataForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserDataForm(request.POST)
        
        if form.is_valid():
            return fill_pdf_form_with_data(form.cleaned_data)
        
        return render(request, self.template_name, {'form': form})


class HealthCheckView(View):
    """
    Healthcheck endpoint that returns JSON response with 200 status.
    """

    def get(self, request):
        return JsonResponse({'message': 'Ok'}, status=200)

