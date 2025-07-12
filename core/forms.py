from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Skill, SwapRequest

class SignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    location = forms.CharField(required=False)
    availability = forms.CharField(required=False)
    is_public = forms.BooleanField(initial=True, required=False)

    skills_offered = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    skills_wanted = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class SwapRequestForm(forms.ModelForm):
    class Meta:
        model = SwapRequest
        fields = ['offered_skill', 'wanted_skill', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add an optional message...'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'location',
            'availability',
            'is_public',
            'skills_offered',
            'skills_wanted',
            'profile_picture',
        ]
        widgets = {
            'skills_offered': forms.CheckboxSelectMultiple,
            'skills_wanted': forms.CheckboxSelectMultiple,
        }
