from django import forms
from django.core.validators import RegexValidator


class UserDataForm(forms.Form):
    """
    Employment Reference/Verification Form for collecting comprehensive employee information.
    """
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # School/District Information
    name_of_school_district = forms.CharField(
        label='Name of School/District',
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter school/district name',
        })
    )
    
    address_of_school_district = forms.CharField(
        label='Address of School/District',
        max_length=300,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter school/district address',
        })
    )
    
    district_name = forms.CharField(
        label='District name',
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter district name',
        })
    )
    
    # Employee Information
    employee_name = forms.CharField(
        label='Employee name',
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter employee name',
        })
    )
    
    positions_held_while_employed = forms.CharField(
        label='Position(s) held while employed',
        max_length=300,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter position(s) held',
        })
    )
    
    from_date = forms.CharField(
        label='From mm, yyyy',
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM, YYYY',
        })
    )
    
    to_date = forms.CharField(
        label='to mm, yyyy',
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM, YYYY',
        })
    )
    
    # Employment Status - Reason for leaving
    REASON_CHOICES = [
        ('resignation', 'Resignation'),
        ('termination', 'Termination'),
        ('resignation_in_lieu', 'Resignation in lieu of Termination'),
        ('retirement', 'Retirement'),
        ('other', 'Other'),
    ]
    
    reason_for_leaving = forms.ChoiceField(
        label='Reason for leaving',
        choices=REASON_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )
    
    other_reason = forms.CharField(
        label='Other',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Please specify if "Other" selected',
        })
    )
    
    # Current Employment Status
    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    current_employed = forms.ChoiceField(
        label='Current employed?',
        choices=YES_NO_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )
    
    # Eligibility & Investigation Questions
    eligible_for_rehire = forms.ChoiceField(
        label='Is this individual eligible to be rehired?',
        choices=YES_NO_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )
    
    if_no_why = forms.CharField(
        label='If no, why',
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Please explain if not eligible for rehire',
            'rows': 3,
        })
    )
    
    subject_of_investigations = forms.ChoiceField(
        label='Has this individual been the subject of any local employment-related investigations?',
        choices=YES_NO_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )
    
    investigation_disciplinary_action = forms.ChoiceField(
        label='If yes, did the investigation result in any local disciplinary action?',
        choices=YES_NO_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )
    
    # Contact Information
    contact_name = forms.CharField(
        label='Contact Name',
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact name',
        })
    )
    
    contact_position = forms.CharField(
        label='Contact position',
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact position',
        })
    )
    
    phone = forms.CharField(
        label='Phone',
        validators=[phone_regex],
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890',
            'pattern': r'^\+?1?\d{9,15}$',
        })
    )
    
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address',
            'type': 'email',
        })
    )
    
    # Additional Information
    any_additional_information_optional = forms.CharField(
        label='Any additional information optional',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter any additional information (optional)',
            'rows': 4,
        })
    )
    
    additional_information_500_char_limit = forms.CharField(
        label='Additional Information 500 character limit',
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter additional information (max 500 characters)',
            'rows': 4,
            'maxlength': '500',
        })
    )
    
    def clean_employee_name(self):
        employee_name = self.cleaned_data.get('employee_name')
        if employee_name:
            return employee_name.strip()
        return employee_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return email.lower().strip()
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        reason = cleaned_data.get('reason_for_leaving')
        other_reason = cleaned_data.get('other_reason')
        
        # Validate that "other" reason is provided if "other" is selected
        if reason == 'other' and not other_reason:
            self.add_error('other_reason', 'Please specify the reason if "Other" is selected.')
        
        return cleaned_data

