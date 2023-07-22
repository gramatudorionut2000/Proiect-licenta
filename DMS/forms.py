from django import forms
from DMS.models import Document, Tag, Folder
from django.contrib.auth.models import Group
from Users.models import CustomUser
class FolderForm(forms.ModelForm):
    name=forms.CharField()

    class Meta:
        model=Folder
        fields=['name',]

class TagForm(forms.ModelForm):
    name=forms.CharField()

    class Meta:
        model=Tag
        fields=['name',]

class DocumentForm(forms.ModelForm):  
    document=forms.FileField()
    description=forms.CharField()
    short_description=forms.CharField()
    folder=forms.ModelChoiceField(queryset=Folder.objects.filter())
    group=forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select)
    tags=forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(),
        required=False)
    blacklist=forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.SelectMultiple(),
        required=False)
    is_global=forms.BooleanField(required=False)

    class Meta:
        model= Document
        fields=['document', 'short_description', 'description', 'group','tags','folder', 'blacklist','is_global']

class DocumentUpdateForm(forms.ModelForm):
    document=forms.FileField()
    short_description=forms.CharField()
    description=forms.CharField()
    tags=forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(),
        required=False)
    blacklist=forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.SelectMultiple())
    is_global=forms.BooleanField(required=False)
    class Meta:
        model= Document
        fields=['document','short_description' ,'description','tags', 'blacklist','is_global']
