from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Card, BasicCard, IdentificationCard, ImageOcclusionCard

admin.site.register(Card)
admin.site.register(BasicCard)
admin.site.register(IdentificationCard)
admin.site.register(ImageOcclusionCard)