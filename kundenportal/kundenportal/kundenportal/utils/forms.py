from django import forms

class CreateUserForm(forms.Form):
    VERTRAG_CHOICES = [(1, "LOW"), (2, "MIDDLE"), (3, "HIGH"), (4, "VERYHIGH")]
    username = forms.CharField(max_length=100, label="Username")
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(max_length=100, label="E-Mail")
    password = forms.CharField(
        min_length=10, label="Password", widget=forms.PasswordInput
    )
