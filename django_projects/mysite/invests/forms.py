from django import forms
from invests.models import Invest
from django.core.files.uploadedfile import InMemoryUploadedFile
from blogs.humanize import naturalsize


# class DateForm(forms.Form):
#     date = forms.DateField("Invest Date (mm/dd/yyy)",auto_now_add=False, auto_now=False, blank=True, null=True)
