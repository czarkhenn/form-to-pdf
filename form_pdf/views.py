from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .forms import UserDataForm
from .services import generate_pdf_from_data


class UserFormView(View):
    """
    Display the user data form and handle form submission.
    On valid submission, show HTML preview.
    """

    template_name = 'form_pdf/form.html'

    def get(self, request):
        form = UserDataForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserDataForm(request.POST)
        
        if form.is_valid():
            request.session['user_data'] = form.cleaned_data
            
            return render(request, 'form_pdf/preview_page.html', {
                'data': form.cleaned_data
            })
        
        return render(request, self.template_name, {'form': form})


class GeneratePDFView(View):
    """
    Generate and return PDF from stored user data.
    """
    
    def get(self, request):
        user_data = request.session.get('user_data')
        
        if not user_data:
            return JsonResponse({'error': 'No data available'}, status=400)
        
        return generate_pdf_from_data(user_data)

