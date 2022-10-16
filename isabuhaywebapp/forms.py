from dataclasses import field
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'firstname',
            'lastname',
            'phone_number',
            'birthdate',
            'blood_type',
            'height',
            'weight',
            'is_admin',
            'is_active',
            'is_staff',
            'is_superuser'
        ]

        # widgets = {
        #     'birthdate' : DateInput,
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        password_val = "Must be at least 8 characters and cannot be entirely numeric."

        self.fields['username'].widget.attrs.update({'placeholder' : 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder' : 'Email'})
        self.fields['firstname'].widget.attrs.update({'placeholder' : 'Firstname'})
        self.fields['lastname'].widget.attrs.update({'placeholder' : 'Lastname'})
        self.fields['phone_number'].widget.attrs.update({'placeholder' : 'Phone Number'})
        self.fields['blood_type'].widget.attrs.update({'placeholder' : 'Blood Type'})
        self.fields['height'].widget.attrs.update({'placeholder' : 'Height'})
        self.fields['weight'].widget.attrs.update({'placeholder' : 'Weight'})
        self.fields['password1'].widget.attrs.update({
            'placeholder' : 'Password',
            'onfocus': "alert('" +password_val+"'); (this.onfocus = '');"
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder' : 'Confirm Password'
        })
        self.fields['birthdate'].widget.attrs.update({
            'placeholder' : 'Birthdate',
            'onfocus': '(this.type = \'date\')'
        })

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CBCTestResultForm(forms.ModelForm):
    class Meta:
        model = CBCTestResult
        fields = '__all__'

        widgets = {
            'testImage': forms.HiddenInput(),
            'testPDF': forms.HiddenInput(),
            'testDocx': forms.HiddenInput(),
            'source': forms.TextInput(attrs={'class': 'forms-control'}),
            'labNumber': forms.TextInput(attrs={'class': 'forms-control'}),
            'labNumber': forms.TextInput(attrs={'class': 'forms-control'}),
        }

class CBCTestResultImageForm(forms.ModelForm):
    class Meta:
        model = CBCTestResultImage
        fields = '__all__'

class CBCTestResultPDFForm(forms.ModelForm):
    class Meta:
        model = CBCTestResultPDF
        fields = '__all__'

class CBCTestResultDocxForm(forms.ModelForm):
    class Meta:
        model = CBCTestResultDocx
        fields = '__all__'


        
