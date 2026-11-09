



from django import forms

from .models import book_appointment
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile



class Booking_Form(forms.ModelForm):
    class Meta:
        model = book_appointment
        fields = ['patient_name', 'patient_email', 'patient_phone', 'doctor_name', 'booked_on']
        labels = {
            'patient_name': 'Patient Name',
            'patient_email': 'Patient Email',
            'patient_phone': 'Patient Phone',
            'doctor_name': 'Doctor',
            'booked_on': 'Booking date'
        }
        widgets = {
            'patient_name':forms.TextInput(attrs={'placeholder':'Enter your name','class':'form-control'}),
            'patient_email':forms.EmailInput(attrs={'placeholder':'Enter your email','class':'form-control'}),
            'patient_phone':forms.TextInput(attrs={'placeholder':'Enter your phone number','class':'form-control'}),
            'doctor_name':forms.Select(attrs={'class':'form-control'}),
            'booked_on':forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }



class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'profile-input',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Email Address'
            }),
        }


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'date_of_birth',
            'gender',
            'address',
            'profile_picture'
        ]

        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Phone Number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'profile-input',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'profile-input'
            }),
            'address': forms.Textarea(attrs={
                'class': 'profile-input',
                'rows': 3,
                'placeholder': 'Your Address'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'profile-input',
                'accept': 'image/jpeg,image/png,image/webp'
            }),
        }

    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture')

        if image and image.size > 2 * 1024 * 1024:
            raise forms.ValidationError(
                'Image size must be less than 2 MB.'
            )

        if image:
            allowed_types = [
                'image/jpeg',
                'image/png',
                'image/webp'
            ]

            if image.content_type not in allowed_types:
                raise forms.ValidationError(
                    'Only JPG, PNG and WEBP images are allowed.'
                )

        return image
