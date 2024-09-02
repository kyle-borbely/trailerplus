from django import forms
from wagtailstreamforms.fields import BaseField, register


@register("mytext")
class CustomTextField(BaseField):
    field_class = forms.CharField
