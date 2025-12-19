import json

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

# class ImageOcclusionCardForm(forms.ModelForm):
#     class Meta:
#         model = ImageOcclusionCard
#         fields = ['front_field', 'img_path']
#         widgets = {
#             'front_field': forms.TextInput(attrs={'class': INPUT_CLASSES, 'style': 'height: 40px;', 'placeholder': 'Optional prompt'}),
#             'img_path': forms.FileInput(attrs={'class': 'form-control border border-secondary'}),
#         }
#         labels = {
#             'front_field': 'Front (Optional)',
#             'img_path': 'Upload Image',
#         }

class ImageOcclusionCardForm(forms.ModelForm):
    occlusion_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ImageOcclusionCard
        fields = ['front_field', 'img_path']
        widgets = {
            'front_field': forms.TextInput(attrs={'class': INPUT_CLASSES, 'style': 'height: 40px;', 'placeholder': 'Title'}),
            'img_path': forms.FileInput(attrs={'class': 'form-control border border-secondary'}),
        }
        labels = {
            'front_field': 'Title',
            'img_path': 'Upload Image',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.front_field:
            try:
                data = json.loads(self.instance.front_field)
                if isinstance(data, dict):
                    self.initial['front_field'] = data.get('prompt', '')
                    if data.get('rect'):
                        self.initial['occlusion_data'] = json.dumps(data.get('rect'))
            except (json.JSONDecodeError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        prompt = cleaned_data.get('front_field', '')
        rect_json = cleaned_data.get('occlusion_data')

        try:
            rect_data = json.loads(rect_json) if rect_json else None
        except json.JSONDecodeError:
            rect_data = None

        payload = {
            'prompt': prompt,
            'rect': rect_data
        }

        cleaned_data['front_field'] = json.dumps(payload)
        return cleaned_data