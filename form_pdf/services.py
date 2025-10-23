from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def generate_pdf_from_data(user_data: dict) -> HttpResponse:
    """
    Generate a PDF from user data.
    """
    html_string = render_to_string('form_pdf/preview.html', {'data': user_data})
    
    html = HTML(string=html_string)
    pdf_bytes = html.write_pdf()
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="user_data.pdf"'
    
    return response

