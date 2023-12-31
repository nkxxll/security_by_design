from django import forms

CONTRACT_CHOICES = [(1, "LOW"), (2, "MIDDLE"), (3, "HIGH"), (4, "VERYHIGH")]

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(max_length=100, label="E-Mail")
    password = forms.CharField(
        min_length=10, label="Password", widget=forms.PasswordInput
    )

class CreateUserMeta(forms.Form):
    auth_key = forms.CharField(max_length=20, min_length=20, label="Authentication Key Messtellenbetreiber")
    contract = forms.ChoiceField(label="Vertrag", choices=CONTRACT_CHOICES)
    # Address start
    street = forms.CharField(max_length=100)
    street_number = forms.CharField(max_length=10)
    postal_code = forms.CharField(max_length=10)
    city = forms.CharField(max_length=100)
    # Address end

class CreateEditData(forms.Form):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(max_length=100, label="E-Mail")
    street = forms.CharField(max_length=100, label="Street")
    street_number = forms.CharField(max_length=10, label="Street Number")
    postal_code = forms.CharField(max_length=10, label="Postal Code")
    city = forms.CharField(max_length=100, label="City")
    password = forms.CharField(
        min_length=10, label="Password", widget=forms.PasswordInput, required=False
    )
    auth_key = forms.CharField(
        max_length=20, min_length=20, label="Authentication Key Messtellenbetreiber", required=False
    )
