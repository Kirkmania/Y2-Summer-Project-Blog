from django import forms
from .models import CV, cvPersonalDetails, cvProfile, cvEducation

class CVForm(forms.ModelForm):

    class Meta:
        model = CV
        fields = ('text',)

class cvPersonalDetailsForm(forms.ModelForm):

    class Meta:
        model = cvPersonalDetails
        fields = ('first_name', 'last_name', 'profession', 'city', 'postcode', 'phone_number', 'email')

class cvProfileForm(forms.ModelForm):

    class Meta:
        model = cvProfile
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control'})}
    
class cvEducationForm(forms.ModelForm):

    class Meta:
        model = cvEducation
        fields = ('school', 'location', 'subject', 'grade', 'start_date', 'end_date',)