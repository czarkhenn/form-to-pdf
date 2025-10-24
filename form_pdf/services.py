from django.http import HttpResponse
from pypdf import PdfReader, PdfWriter
from pathlib import Path
import io


def fill_pdf_form_with_data(user_data: dict) -> HttpResponse:
    """
    Fill the PDF form with user data and return as downloadable PDF.
    
    """
    pdf_path = Path(__file__).resolve().parent.parent / "form.pdf"
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    writer.clone_document_from_reader(reader)
    
    field_values = {}
    
    if user_data.get('name_of_school_district'):
        field_values["Name of Schoo/District"] = user_data['name_of_school_district']
    
    if user_data.get('address_of_school_district'):
        field_values["Address of School/District"] = user_data['address_of_school_district']
    
    if user_data.get('district_name'):
        field_values["District name"] = user_data['district_name']
    
    if user_data.get('employee_name'):
        field_values["Employee name"] = user_data['employee_name']
    
    if user_data.get('from_date'):
        field_values["From mm, yyyy"] = user_data['from_date']
    
    if user_data.get('to_date'):
        field_values["to mm, yyyy"] = user_data['to_date']
    
    if user_data.get('positions_held_while_employed'):
        field_values["Position(s) held while employed"] = user_data['positions_held_while_employed']
    
    reason = user_data.get('reason_for_leaving', '')
    field_values["Resignation"] = "/Yes" if reason == 'resignation' else "/Off"
    field_values["Termination"] = "/Yes" if reason == 'termination' else "/Off"
    field_values["Resignation in lieu of Termination"] = "/Yes" if reason == 'resignation_in_lieu' else "/Off"
    field_values["Retirement"] = "/Yes" if reason == 'retirement' else "/Off"
    
    if reason == 'other' and user_data.get('other_reason'):
        field_values["Other"] = user_data['other_reason']
    else:
        field_values["Other"] = ""
    
    current_employed = user_data.get('current_employed', '')
    field_values["Current employed?(1).p1"] = "/Yes" if current_employed == 'yes' else "/No"
    
    eligible_for_rehire = user_data.get('eligible_for_rehire', '')
    field_values["Is this individual eligible to be rehired(1).p1"] = "/Yes" if eligible_for_rehire == 'yes' else "/No"
    
    if user_data.get('if_no_why'):
        field_values["If no, why"] = user_data['if_no_why']
    
    subject_of_investigations = user_data.get('subject_of_investigations', '')
    field_values["Has this individual been the subject of any local employment-related investigations?(1).p1"] = "/Yes" if subject_of_investigations == 'yes' else "/No"
    
    investigation_disciplinary_action = user_data.get('investigation_disciplinary_action', '')
    field_values["If yes, did the investigation result in any local disciplinary action?(1).p1"] = "/Yes" if investigation_disciplinary_action == 'yes' else "/No"
    
    if user_data.get('contact_name'):
        field_values["Contact name"] = user_data['contact_name']
    
    if user_data.get('contact_position'):
        field_values["Contact position"] = user_data['contact_position']
    
    if user_data.get('phone'):
        field_values["phone"] = user_data['phone']
    
    if user_data.get('email'):
        field_values["email"] = user_data['email']
    
    if user_data.get('any_additional_information_optional'):
        field_values["Any additional informtion optional"] = user_data['any_additional_information_optional']
    
    if user_data.get('additional_information_500_char_limit'):
        field_values["Additional Information 500 character limit"] = user_data['additional_information_500_char_limit']
    
    for page in writer.pages:
        writer.update_page_form_field_values(
            page,
            field_values,
            auto_regenerate=False
        )
    
    pdf_buffer = io.BytesIO()
    writer.write(pdf_buffer)
    pdf_buffer.seek(0)
    
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Iowa_DOE_Employment_Reference_Form_Mar_2025.pdf"'
    
    return response
