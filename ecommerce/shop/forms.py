
from django import forms
from .models import Good


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['name', 'description', 'price', 'image']
        
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        return image

