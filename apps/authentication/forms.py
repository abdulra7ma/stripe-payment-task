from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.forms import Form, ModelForm
from school.models import Teacher


class LoginForm(Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Phone Number",
                "id": "login-username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )

    error_messages = {"not_valid": "Phone Number or Password is not correct"}

    def clean_phone_number(self, *args, **kwargs):
        self.phone_number = self.cleaned_data.get("phone_number")
        self.user = Teacher.objects.filter(phone_number=self.phone_number)

        if not self.user.exists():
            raise forms.ValidationError(self.error_messages["not_valid"])

        return self.phone_number

    def clean_password(self, *args, **kwargs):
        self.password = self.cleaned_data.get("password")

        if self.user.exists():
            if not check_password(self.password, self.user.first().password):
                raise forms.ValidationError(self.error_messages["not_valid"])

        return self.password

    @property
    def auth_user(self):
        return self.user.first()


class SignupForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ["email", "phone_number", "full_name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control form-control-lg",
                "placeholder": "Email",
                "aria-label": "Email",
            }
        )
        self.fields["full_name"].widget.attrs.update(
            {
                "class": "form-control form-control-lg",
                "placeholder": "Full Name",
                "aria-label": "Full Name",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control form-control-lg",
                "placeholder": "Password",
                "aria-label": "Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control form-control-lg",
                "placeholder": "Confirm Password",
                "aria-label": "Password",
            }
        )
        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "form-control form-control-lg phone-inputmask",
                "placeholder": "Phone Number",
                "aria-label": "Phone Number",
            }
        )

    def clean_email(self, *args, **kwargs):
        self.email = self.cleaned_data.get("email")

        if Teacher.objects.filter(email=self.email).exists():
            raise forms.ValidationError("This email can't be used")

        return self.email

    def clean_password1(self, *args, **kwargs):
        self.password = self.cleaned_data.get("password1")

        if len(self.password) < 8:
            raise forms.ValidationError("Passwords length can not be less than 8 characters")

        return self.password
    
    def save(self, commit):
        user = super().save(False)

        # activate any newly created user by default, 
        # if there's a need for extra validation you can send him an activation email
        user.is_active = True
        user.save()
        
        return user