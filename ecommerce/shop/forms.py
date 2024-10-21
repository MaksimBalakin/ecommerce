
from django import forms
from .models import Good, validate_image_square


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['name', 'description', 'price', 'image']
        
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        validate_image_square(image)
        return image

