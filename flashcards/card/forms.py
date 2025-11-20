from django import forms
from card.models import BasicCard, IdentificationCard, ImageOcclusionCard


class BasicCardForm(forms.ModelForm):
    class Meta:
        model = BasicCard
        fields = ['front_field','back_field']

class IdentificationCardForm(forms.ModelForm):
    class Meta:
        model = IdentificationCard
        fields = ['front_field','hidden_field']

class ImageOcclusionCardForm(forms.ModelForm):
    class Meta:
        model = ImageOcclusionCard
        fields = ['img_path','front_field']

