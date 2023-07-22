import os
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DocumentForm, DocumentUpdateForm, TagForm, FolderForm
from .models import Document, Tag, Folder
from Users.models import CustomUser
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from .filters import DocumentFilter
from django_filters.views import FilterView
from reversion.views import RevisionMixin
from reversion.models import Version
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from docx import Document as docx_Document
def home(request):
    return render(request, 'DMS/index.html',)

@login_required
def download(request, id):
    user_groups=set(request.user.groups.all())
    document=Document.objects.get(id=id)
    user_groups=set(request.user.groups.all())
    author=CustomUser.objects.get(id=document.author.id)
    author_groups=set(author.groups.all())
    if((user_groups & author_groups) is False) or (request.user in document.blacklist.all()):
        return redirect('unauthorised')
    path=document.get_name + '.' + document.get_extension
    file = open('media/'+ path, 'rb')
    response = FileResponse(file, as_attachment=True)
    return response

@login_required
def tag(request):
    tags=Tag.objects.all()
    documents= Document.objects.all()
    tag_numbers=dict()
    for tag in tags:
        tag_numbers[tag]=0
    for document in documents:
        for tag_d in document.tags.all():
            tag_numbers[tag_d]+=1
    tag_numbers=tag_numbers.values()
    tag_numbers=list(tag_numbers)
    if request.method == 'POST':
        if request.user.is_manager is True:
            form=TagForm(request.POST)
            if form.is_valid():
                form.save()
                name=form.cleaned_data.get('name')
                messages.success(request, f'Tag {name} Created successfuly')
                return redirect('tag')
        else:
            return redirect('tag')
    else:
        form=TagForm()
        context={'tags':tags,'tag_numbers':tag_numbers, 'form':form,}
        
    return render(request, 'DMS/tag.html', context)

class TagDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model= Tag
    success_url ='/'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

class DocListView(FilterView):
    model= Document
    template_name= 'DMS/index.html'
    context_object_name='documents'
    ordering=['-date_posted']
    paginate_by= 3
    filterset_class = DocumentFilter

    def get_queryset(self):
        Document.objects.all()
        qs=Document.objects.filter(Q(is_global=True) | Q(group__in=self.request.user.groups.all()) | Q(author=self.request.user.id) | Q(author__groups__in=self.request.user.groups.all())).exclude(blacklist=self.request.user.id).distinct()
        return qs


class DocDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model= Document
    
    def test_func(self):
        user_groups=set(self.request.user.groups.all())
        document=self.get_object()
        author=CustomUser.objects.get(id=document.author.id)
        author_groups=set(author.groups.all())
        if((user_groups & author_groups)) and (self.request.user not in document.blacklist.all()):
            return True
        else:
            return False
    
    def get_context_data(self, *args, **kwargs):
        context= super(DocDetailView, self).get_context_data(*args, **kwargs)
        document=self.get_object()
        if document.extension in ['docx','txt']:
            path=document.get_name + '.' + document.get_extension
            if document.extension == 'txt':
                file= open('media/'+ path, 'r')
            else:
                file = open('media/'+ path, 'rb')
            context['valid']='True'
            if document.extension == 'docx':
                text=docx_Document(file)
                content = []
                if text is None:
                    text="Document has no text (default message)"
                for paragraph in text.paragraphs:
                    content.append(paragraph.text)
                context['content']=content
                return context
            elif document.extension == 'txt':
                content=file.readlines()
                if content is None:
                    content="Document has no text (default message)"
                context['content']=content
            file.close()
        return context


class DocCreateView(LoginRequiredMixin, RevisionMixin, CreateView):
    model= Document
    template_name ='DMS/upload.html'
    form_class=DocumentForm
    success_url = '/'

    def get_filename(self):
        filename=os.path.basename(self.document.name)
        return filename

    def get_form(self):
        form = super().get_form(form_class=self.form_class)
        form.fields['group'].queryset = Group.objects.filter(id__in=self.request.user.groups.all())
        form.fields['folder'].queryset = Folder.objects.filter(user=self.request.user.id)
        form.fields['blacklist'].queryset = CustomUser.objects.filter(groups__in=self.request.user.groups.all()).exclude(id=self.request.user.id)
        return form


    def form_valid(self, form):
        form.instance.author=self.request.user
        return super(DocCreateView,self).form_valid(form)

class DocUpdateView(RevisionMixin ,LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model= Document
    template_name='DMS/document_update.html'
    form= DocumentUpdateForm
    success_url= '/'
    fields=['document','short_description' ,'description','tags', 'blacklist','is_global']

    def test_func(self):
        document=self.get_object()
        if self.request.user == document.author:
            return True
        return False

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['blacklist'].queryset = CustomUser.objects.filter(groups__in=self.request.user.groups.all()).exclude(id=self.request.user.id)
        return form

def document_version_list(request,id):

    document=get_object_or_404(Document, pk=id)
    if(request.user.id!=document.author.id):
        return redirect('unauthorised')
    versions = Version.objects.get_for_object(document)
    blacklists_id=list()
    tags_id=list()
    blacklists=list()
    tags=list()
    for version in versions:
        blacklists_id=version.field_dict['blacklist']
        tags_id=version.field_dict['tags']
        blacklists.append(list((CustomUser.objects.filter(id__in=blacklists_id).values_list('username'))))
        tags.append(list((Tag.objects.filter(id__in=tags_id)).values_list('name')))

    loop=zip(versions,blacklists,tags)
    
    context={'document':document, 'data':loop}
    return render(request, 'DMS/document_versions.html', context)

def document_confirm_restore(request,id,revision_id):

    document=get_object_or_404(Document, pk=id)
    if(request.user.id!=document.author.id):
        return redirect('unauthorised')
    versions = Version.objects.get_for_object(document)
    nr=int(revision_id)
    versions = Version.objects.get_for_object(document)
    context={'versions':versions, 'document':document, 'nr': nr}
    return render(request, 'DMS/document_confirm_restore.html', context)

def document_restore(request,id, revision_id):

    document=get_object_or_404(Document, pk=id)
    if(request.user.id!=document.author.id):
        return redirect('unauthorised')
    nr=int(revision_id)
    versions = Version.objects.get_for_object(document)
    versions[nr].revision.revert()
    messages.success(request, f'Document {document.name} reverted successfully')
    return redirect('DMS-home')


class DocDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Document
    success_url ='/'

    def test_func(self):
        document=self.get_object()
        if self.request.user == document.author:
            return True
        return False

class FolderCreateView(SuccessMessageMixin ,LoginRequiredMixin, CreateView):
    model= Folder
    template_name ='DMS/folder_create.html'
    form=FolderForm
    success_url = '/'
    fields=['name']
    success_message = "Folder %(name)s was created successfully"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)



class FolderListView(LoginRequiredMixin,ListView):
    model= Folder
    template_name= 'DMS/folders.html'
    context_object_name='folders'

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user.id)

class FolderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Folder
    success_url ='/folders'

    def test_func(self):
        folder=self.get_object()
        if self.request.user == folder.user:
            return True
        return False



def terms_conditions(request):
    return render(request, 'DMS/terms&conditions.html')

def about(request):
    return render(request, 'DMS/about.html',)

