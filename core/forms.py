from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import AlumniProfile, ContactMessage

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = [
            "full_name",
            "photo",
            "graduation_year",
            "department",
            "current_company",
            "current_role",
            "employment_status",
            "city",
            "country",
            "linkedin_url",
            "github_url",
            "phone",
            "bio",
            "skills",
            "available_for_mentoring",
            "is_public",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "skills": forms.TextInput(attrs={"placeholder": "Python, Django, React"}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }