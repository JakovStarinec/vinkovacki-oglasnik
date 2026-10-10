from django import forms
from .models import Ad, AdImage

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('title', 'description', 'price', 'location')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Naslov oglasa'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Opis oglasa'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'location': forms.TextInput(attrs={'placeholder': 'Vinkovci, Županja...'}),
        }

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ('image',)
