import django_filters
from django_filters import DateFilter, CharFilter,ModelChoiceFilter
from django.contrib.auth.models import Group
from Users.models import CustomUser
from .models import Document,Folder, Tag
from django import forms
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit,Row,Column, HTML

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields='__all__'
        exclude=['document', 'description', 'date_posted','blacklist' ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('short_description', css_class=''),
                css_class='row'
            ),
            Row(
                Column('name', css_class='col-6 mb-0'),
                Column('extension', css_class=' col-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('group', css_class='col-4 mb-0'),
                Column('author', css_class='col-4 mb-0'),
                Column('folder', css_class='col-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column('start_date', css_class='col-6 mb-0'),
                Column('end_date', css_class='col-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('is_global', css_class='col-4 mb-0'),
                Column('tags', css_class='col-8 mb-0'),
                css_class='row'
            ),
            FormActions(Submit('submit', 'Search', css_class=' btn btn-dark', style="display: inline;"),
                    HTML('''<a class="btn btn-dark float-end" href="{% url 'DMS-home' %}">Clear</a>''')))



class DocumentFilter(django_filters.FilterSet):

    def folders(request):
        qs=Folder.objects.filter(user=request.user.id)
        return qs

    def tags(request):
        qs=Tag.objects.all()
        return qs

    def authors(request):
        qs=CustomUser.objects.filter(groups__id__in=request.user.groups.all()).distinct()
        return qs
    
    def groups(request):
        qs=Group.objects.filter(id__in=request.user.groups.all())
        return qs


    tags=django_filters.ModelMultipleChoiceFilter(field_name='tags',queryset=tags)
    start_date=DateFilter(field_name='date_posted', lookup_expr='gte')
    end_date=DateFilter(field_name='date_posted', lookup_expr='lte')
    short_description=CharFilter(field_name='short_description', lookup_expr='icontains', label='Description')
    name=CharFilter(field_name='name', lookup_expr='icontains', label='Name')
    extension=CharFilter(field_name='extension', lookup_expr='icontains', label='Extension')
    folder=ModelChoiceFilter(field_name='folder', queryset=folders)
    author=ModelChoiceFilter(field_name='author', queryset=authors)
    group=ModelChoiceFilter(field_name='group', queryset=groups)
    is_global=django_filters.BooleanFilter()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        form = DocumentForm