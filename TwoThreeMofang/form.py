#coding:utf-8
__author__ = 'similarface'

from django import forms
class UploadFileForm(forms.Form):
    file = forms.FileField()
    # uploaduser=forms.CharField(max_length=32)
    # uploaddate=forms.DateField()