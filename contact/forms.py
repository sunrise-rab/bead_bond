from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message", "consent_to_contact"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "bb-input", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "bb-input", "placeholder": "you@example.com"}),
            "subject": forms.TextInput(attrs={"class": "bb-input", "placeholder": "Optional"}),
            "message": forms.Textarea(attrs={"class": "bb-input", "rows": 5, "placeholder": "How can we help?"}),
        }

    consent_to_contact = forms.BooleanField(
        required=False,
        label="I’m happy for Bead Bond to contact me about this message.",
    )
