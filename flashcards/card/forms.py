from django import forms
from .models import BasicCard, IdentificationCard, ImageOcclusionCard
from deck.models import Deck

INPUT_CLASSES = 'form-control p-3 border border-secondary'
SELECT_CLASSES = 'form-select rounded border border-dark'

class BasicCardForm(forms.ModelForm):
    class Meta:
        model = BasicCard
        fields = ['front_field', 'back_field'] # Include deck so it renders
        widgets = {
            'front_field': forms.TextInput(attrs={'class': INPUT_CLASSES, 'style': 'height: 40px;'}),
            'back_field': forms.TextInput(attrs={'class': INPUT_CLASSES, 'style': 'height: 40px;'}),
        }
        labels = {
            'front_field': 'Front',
            'back_field': 'Back',
        }

class IdentificationCardForm(forms.ModelForm):
    class Meta:
        model = IdentificationCard
        fields = ['front_field', 'hidden_field']
        widgets = {
            'front_field': forms.TextInput(attrs={'class': INPUT_CLASSES, 'style': 'height: 40px;'}),
            'hidden_field': forms.TextInput(attrs={'class': INPUT_CLASSES, 'style': 'height: 40px;'}),
        }
        labels = {
            'front_field': 'Front',
            'hidden_field': 'Extra hint',
        }

class ImageOcclusionCardForm(forms.ModelForm):
    class Meta:
        model = ImageOcclusionCard
        fields = ['front_field', 'img_path']
        widgets = {
            'front_field': forms.TextInput(attrs={'class': INPUT_CLASSES, 'style': 'height: 40px;', 'placeholder': 'Optional prompt'}),
            'img_path': forms.FileInput(attrs={'class': 'form-control border border-secondary'}),
        }
        labels = {
            'front_field': 'Front (Optional)',
            'img_path': 'Upload Image',
        }