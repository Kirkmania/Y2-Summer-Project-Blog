from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder, Div, Button, HTML
from bootstrap_datepicker_plus import DatePickerInput
from .models import *

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ('text',)

class cvPersonalDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-3 mb-0'),
                Column('last_name', css_class='form-group col-md-3 mb-0'),
                Column('profession', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('postcode', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-3 mb-0'),
                Column('email', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Submit('personal_details_next', 'Next', css_class="btn btn-secondary")
        )

    class Meta:
        model = cvPersonalDetails
        fields = ('first_name', 'last_name', 'profession', 'city', 'postcode', 'phone_number', 'email')


class cvProfileForm(forms.ModelForm):
    class Meta:
        model = cvProfile
        fields = ('text',)
    

class cvEducationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('school', css_class='form-group col-md-4 mb-0'),
                Column('location', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('level_of_study', css_class='form-group col-md-4 mb-0'),
                Column('start_date', css_class='form-group col-md-2 mb-0'),
                Column('end_date', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('subject', css_class='form-group col-md-4 mb-0'),
                Column('grade', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Submit('education_save_and_add', 'Save and add', css_class='btn btn-secondary'),
            Submit('education_next', 'Next', css_class='btn btn-secondary'),
        )

    class Meta:
        model = cvEducation
        fields = ('school', 'location', 'level_of_study', 'subject', 'grade', 'start_date', 'end_date',)
        widgets = {
            'start_date': DatePickerInput(attrs={"placeholder": "DD/MM/YYYY"}, options={"format": "DD/MM/YYYY"}),
            'end_date': DatePickerInput(attrs={"placeholder": "DD/MM/YYYY"}, options={"format": "DD/MM/YYYY"}),
            }

class cvWorkHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('job_title', css_class='form-group col-md-6 mb-0'),
                Column('employer', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('start_date', css_class='form-group col-md-2 mb-0'),
                Column('end_date', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-8 mb-0'),
            ),
            Submit('work_history_save_and_add', 'Save and add', css_class='btn btn-secondary'),
            Submit('work_history_next', 'Next', css_class='btn btn-secondary'),
        )

    class Meta:
        model = cvWorkHistory
        fields = ('job_title', 'employer', 'city', 'description', 'start_date', 'end_date',)
        widgets = {
            'start_date': DatePickerInput(attrs={"placeholder": "DD/MM/YYYY"}, options={"format": "DD/MM/YYYY"}),
            'end_date': DatePickerInput(attrs={"placeholder": "DD/MM/YYYY"}, options={"format": "DD/MM/YYYY"}),
            }

class cvExtrasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('extras_next', 'Next', css_class='btn btn-secondary'))

    class Meta:
        model = cvExtras
        fields = ('skills', 'interests', 'languages', 'certifications',)

class cvSkillForm(forms.ModelForm):
   
    class Meta:
        model = cvSkill
        fields = ('skill', 'description',)

class cvInterestForm(forms.ModelForm):

    class Meta:
        model = cvInterest
        fields = ('interest', 'description',)

class cvCertificationForm(forms.ModelForm):

    class Meta:
        model = cvCertification
        fields = ('date', 'certification',)
        widgets = {'date': DatePickerInput(attrs={"placeholder": "DD/MM/YYYY"}, options={"format": "DD/MM/YYYY"}),}
        
class cvLanguageForm(forms.ModelForm):

    class Meta:
        model = cvLanguage
        fields = ('language', 'proficiency',)