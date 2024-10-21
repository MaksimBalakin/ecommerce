# cart/forms.py
from django import forms

class CartAddGoodForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
