from dataclasses import field
from django import forms
from .models import *

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


        
