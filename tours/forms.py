from django import forms
from .models import TravelerRegistration, TourGuide
from .models import Tour

from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = TravelerRegistration
        fields = ['traveler_first_name', 'traveler_last_name', 'traveler_phone', 'traveler_email']
        labels = {
            'traveler_first_name': 'שם פרטי',
            'traveler_last_name': 'שם משפחה',
            'traveler_phone': 'טלפון',
            'traveler_email': 'אימייל',
        }
        widgets = {
            'traveler_first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'הכנס שם פרטי',
                'required': 'required',
                'minlength': '2',
                'maxlength': '30',
                'pattern': '^[א-תA-Za-z\\s\\-]+$',
                'title': 'השם צריך להכיל אותיות בעברית או באנגלית בלבד'
            }),
            'traveler_last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'הכנס שם משפחה',
                'required': 'required',
                'minlength': '2',
                'maxlength': '30',
                'pattern': '^[א-תA-Za-z\\s\\-]+$',
                'title': 'השם צריך להכיל אותיות בעברית או באנגלית בלבד'
            }),
            'traveler_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0501234567',
                'required': 'required',
                'pattern': '^05[0-9]{8}$',
                'title': 'מספר טלפון תקני: 10 ספרות, מתחיל ב-05 (למשל: 0501234567)'
            }),
            'traveler_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
                'required': 'required',
                'maxlength': '254',
                'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$',
                'title': 'כתובת אימייל תקינה (למשל: name@example.com)'
            }),
        }

    def clean_traveler_first_name(self):
        name = self.cleaned_data['traveler_first_name']
        if not re.match(r'^[א-תA-Za-z\s\-]+$', name):
            raise ValidationError("השם הפרטי חייב להכיל אותיות בלבד.")
        return name

    def clean_traveler_last_name(self):
        name = self.cleaned_data['traveler_last_name']
        if not re.match(r'^[א-תA-Za-z\s\-]+$', name):
            raise ValidationError("שם המשפחה חייב להכיל אותיות בלבד.")
        return name

    def clean_traveler_phone(self):
        phone = self.cleaned_data['traveler_phone']
        if not re.match(r'^05[0-9]{8}$', phone):
            raise ValidationError("מספר הטלפון חייב להתחיל ב-05 ולהכיל בדיוק 10 ספרות.")
        return phone

    def clean_traveler_email(self):
        email = self.cleaned_data['traveler_email']
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise ValidationError("כתובת אימייל לא תקינה.")
        return email


class TourGuideForm(forms.ModelForm):
    class Meta:
        model = TourGuide
        fields = '__all__'
        widgets = {
            'tour_guide_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tour_guide_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tour_guide_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'tour_guide_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tour_guide_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            'languages': forms.TextInput(attrs={'class': 'form-control'}),
            'specialties': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            'facebook_link': forms.URLInput(attrs={
                'class': 'form-control', 'dir': 'ltr', 'placeholder': 'https://www.facebook.com/your-page'
            }),
            'instagram_link': forms.URLInput(attrs={
                'class': 'form-control', 'dir': 'ltr', 'placeholder': 'https://www.instagram.com/your-profile'
            }),
            'whatsapp_link': forms.URLInput(attrs={
                'class': 'form-control', 'dir': 'ltr', 'placeholder': 'https://wa.me/your-number'
            }),
            'website_link': forms.URLInput(attrs={
                'class': 'form-control', 'dir': 'ltr', 'placeholder': 'https://your-website.com'
            }),
        }


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = '__all__'
        widgets = {
            'tour_title': forms.TextInput(attrs={'class': 'form-control'}),
            'tour_subtitle': forms.TextInput(attrs={'class': 'form-control'}),

            'tour_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tour_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

            'tour_description': forms.Textarea(attrs={'class': 'form-control'}),
            'tour_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tour_end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),

            'meeting_point': forms.TextInput(attrs={'class': 'form-control'}),
            'google_maps_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'קישור למיקום במפה (למשל Google Maps)'
            }),

            'tour_guide_name': forms.Select(attrs={'class': 'form-select'}),

            'tour_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'target_audience': forms.SelectMultiple(attrs={     'class': 'form-control' }),

            ' difficulty_level': forms.Select(attrs={'class': 'form-select'}),

            'required_equipment': forms.SelectMultiple(attrs={'class': 'form-control', 'rows': 3}),



        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['שם_מדריך'].queryset = TourGuide.objects.all()