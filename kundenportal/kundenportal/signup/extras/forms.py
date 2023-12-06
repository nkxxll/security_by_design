from django import forms


class CreateUserForm(forms.Form):
    VERTRAG_CHOICES = [(1, "LOW"), (2, "MIDDLE"), (3, "HIGH"), (4, "VERYHIGH")]
    username = forms.CharField(max_length=100, label="Username")
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(max_length=100, label="E-Mail")
    stromzaehler_id = forms.CharField(
        min_length=10, max_length=10, label="Stromzaehler ID"
    )
    vertrag = forms.TypedChoiceField(
        coerce=int, choices=VERTRAG_CHOICES, widget=forms.RadioSelect, label="Vertrag"
    )
    password = forms.CharField(
        min_length=10, label="Password", widget=forms.PasswordInput
    )
