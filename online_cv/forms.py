from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from bootstrap_datepicker_plus import DatePickerInput
from .models import CV, cvPersonalDetails, cvProfile, cvEducation

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
            Submit('personal_details_next', 'Next')
        )

    class Meta:
        model = cvPersonalDetails
        fields = ('first_name', 'last_name', 'profession', 'city', 'postcode', 'phone_number', 'email')


class cvProfileForm(forms.ModelForm):

    class Meta:
        model = cvProfile
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control'})}
    
    
class cvEducationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('school', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('subject', css_class='form-group col-md-4 mb-0'),
                Column('grade', css_class='form-group col-md-2 mb-0'),
                Column('start_date', css_class='form-group col-md-2 mb-0'),
                Column('end_date', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Submit('education_save_and_add', 'Save and add'),
            Submit('education_next', 'Next'),
            
        )

    class Meta:
        model = cvEducation
        fields = ('school', 'location', 'subject', 'grade', 'start_date', 'end_date',)
        widgets = {
            'start_date': DatePickerInput(options={"format": "DD/MM/YYYY"}),
            'end_date': DatePickerInput(options={"format": "DD/MM/YYYY"})
            }
