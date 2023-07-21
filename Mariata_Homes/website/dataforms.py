from django import forms
from django.forms import ModelForm
from .models import Applicant, Admin, Notification, Source

class ApplicantSignUpForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email")
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Date of Birth")
    phone = forms.CharField(max_length=20, required=True, label="Phone Number")
    photo = forms.ImageField(required=True, label="Photo")
    illnesses = forms.CharField(max_length=255, required=False, label="Illnesses")
    disabilities = forms.CharField(max_length=255, required=False, label="Disabilities")
    last_residence = forms.CharField(max_length=255, required=False, label="Last Residence")
    next_of_kin = forms.CharField(max_length=255, required=False, label="Next of Kin")
    recommendation = forms.ModelChoiceField(queryset=Source.objects.all(), required=True, label="Recommendation")
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'dob', 'phone', 'photo', 'illnesses', 'disabilities', 'last_residence', 'next_of_kin']
        labels = {
            'name': 'Full Name',
            'email': 'Email',
            'dob': 'Date of Birth',
            'phone': 'Phone Number',
            'photo': 'Photo',
            'illnesses': 'Illnesses (if any)',
            'disabilities': 'Disabilities (if any)',
            'last_residence': 'Last Residence Address',
            'next_of_kin': 'Next of Kin Name',
            'recommendation': 'Recommendation'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recommendation'].label_from_instance = lambda obj: obj.source_type
        self.fields['photo'].widget.attrs.update({'accept': 'image/*'})
    
    def save(self, commit=True):
        applicant = super().save(commit=False)
        applicant.status = 'pending'
        if self.cleaned_data['recommendation']:
            applicant.recommendation = self.cleaned_data['recommendation']
        if commit:
            applicant.save()
        return applicant


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ApplicantStatusForm(forms.Form):
    email = forms.EmailField(required=True, label="Applicant Email")
    status_choices = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = forms.ChoiceField(choices=status_choices, required=True, label="New Status")

class ApplicantUpdateForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")
    name = forms.CharField(max_length=255, required=False, label="Full Name")
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Date of Birth")
    phone = forms.CharField(max_length=20, required=False, label="Phone Number")
    illnesses = forms.CharField(max_length=255, required=False, label="Illnesses")
    disabilities = forms.CharField(max_length=255, required=False, label="Disabilities")
    last_residence = forms.CharField(max_length=255, required=False, label="Last Residence")
    next_of_kin = forms.CharField(max_length=255, required=False, label="Next of Kin")
    recommendation = forms.ModelChoiceField(queryset=Source.objects.all(), required=False, label="Recommendation")
    status_choices = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = forms.ChoiceField(choices=status_choices, required=True, label="New Status")

    class Meta:
        model = Applicant
        fields = ['name', 'email', 'dob', 'phone', 'photo', 'illnesses', 'disabilities', 'last_residence', 'next_of_kin']
        labels = {
            'name': 'Full Name',
            'email': 'Email',
            'dob': 'Date of Birth',
            'phone': 'Phone Number',
            'illnesses': 'Illnesses (if any)',
            'disabilities': 'Disabilities (if any)',
            'last_residence': 'Last Residence Address',
            'next_of_kin': 'Next of Kin Name',
            'recommendation': 'Recommendation'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recommendation'].label_from_instance = lambda obj: obj.source_type
    
    def save(self, commit=True):
        applicant = super().save(commit=False)
        if self.cleaned_data['recommendation']:
            applicant.recommendation = self.cleaned_data['recommendation']
        if commit:
            applicant.save()
        return applicant

class ApplicantDeleteForm(forms.Form):
    email = forms.EmailField(required=True, label="Applicant Email")

class EmailForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")
