from django import forms

class CertificateForm(forms.Form):
    template = forms.FileField(label='Upload Certificate Template')
    csvfile = forms.FileField(label='Upload CSV File')
    sender_email = forms.EmailField(label='Enter Sender\'s Email', widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    sender_password = forms.CharField(label='Enter Your Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
