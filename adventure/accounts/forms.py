from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm

from adventure.accounts.models import AppProfile

UserModel = get_user_model()


# This form is required because we use a CustomUser model.
# It is registered in Django Admin to allow editing of AppUser objects.
# In this project, only the superuser is allowed to actually make changes (e.g. deactivate a user).
# Staff users will have read-only access to user data.
class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


# This forms gives the initial chance for registration by accepting email and password
class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {
            'placeholder': 'Email',
            'class': 'form-control',
        }
        self.fields['password1'].widget.attrs = {
            'placeholder': 'Password',
            'class': 'form-control',
        }
        self.fields['password2'].widget.attrs = {
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        }


# After initial registration by giving email and password the user can access the additional options to give info for
# its profile (AppProfile - model)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = AppProfile
        fields = ['first_name', 'last_name', 'date_of_birth', 'profile_picture', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'





# We use this form to change the email of the registered user in the frontend
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {
            'placeholder': 'New Email',
            'class': 'form-control',
        }


# We use the already given form from Django to change the password in the frontend
class AppUserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
