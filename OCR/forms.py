from django import forms

class OCRUploadForm(forms.Form):
    file=forms.FileField(widget=forms.FileInput(attrs={
        'id': 'file_id'}))