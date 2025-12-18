import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='cloze_front')
def cloze_front(value):
    if not value:
        return ""
    pattern = r'\{\{(.*?)\}\}'
    result = re.sub(pattern, r'<span class="cloze-bracket">[...]</span>', value)
    return mark_safe(result)

@register.filter(name='cloze_back')
def cloze_back(value):
    if not value:
        return ""
    pattern = r'\{\{(.*?)\}\}'
    result = re.sub(pattern, r'<span class="cloze-reveal">\1</span>', value)
    return mark_safe(result)