from django import forms
from django.forms import inlineformset_factory
from datetime import date

from .models import Booking, BookingChild


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["booking_date", "photo_consent", "notes"]
        widgets = {
            "booking_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def clean_booking_date(self):
        d = self.cleaned_data["booking_date"]
        if d < date.today():
            raise forms.ValidationError("Please choose a future date.")
        return d


class BookingChildForm(forms.ModelForm):
    class Meta:
        model = BookingChild
        fields = ["name", "age"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }


BookingChildFormSet = inlineformset_factory(
    Booking,
    BookingChild,
    form=BookingChildForm,
    extra=1,          # shows 1 empty child row by default
    can_delete=True   # allows deleting children
)
