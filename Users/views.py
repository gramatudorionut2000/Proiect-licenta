import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Users.models import CustomUser
from .forms import UserRegisterForm, UserUpdateForm, ProfileForm, CustomUserRegisterForm, UsersGroupForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, unauthorised_user
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form=CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            last_name=form.cleaned_data.get('last_name')
            first_name=form.cleaned_data.get('first_name')
            messages.success(request, f'Account with the username {username} for {last_name} {first_name} created successfully.')
            return redirect('login')
    else:
        form=UserRegisterForm()    
    return render(request, 'Users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form =UserUpdateForm(request.POST ,instance =request.user)
        p_form =ProfileForm(request.POST, request.FILES ,instance =request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated successfully')
            return redirect('profile')

    else:
        u_form =UserUpdateForm(instance =request.user)
        p_form =ProfileForm(instance =request.user.profile)
    context = {'u_form': u_form,
               'p_form': p_form
             }

    return render(request, 'Users/profile.html', context)

def terms_conditions(request):
    return render(request, 'Users/terms_conditions.html')

def privacy_policy(request):
    return render(request, 'Users/privacy_policy.html')

class ProfilePage(LoginRequiredMixin ,DetailView):
    model = CustomUser
    template_name= 'Users/profile_data.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfilePage, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


@login_required
@unauthorised_user
def group_management(request):
    if request.method == "POST":
        UsersGroupForm.base_fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(id__in=request.user.groups.all()),
                                                                    )
        UsersGroupForm.base_fields['users'] = forms.ModelChoiceField(queryset=CustomUser.objects.exclude(groups__in=request.user.groups.all()).exclude(id=request.user.id),
                                                                    )
        if 'add' in request.POST:
            a_form = UsersGroupForm(request.POST)
            r_form=UsersGroupForm()
            form=a_form

        UsersGroupForm.base_fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(id__in=request.user.groups.all()),
                                                                    )
        UsersGroupForm.base_fields['users'] = forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__in=request.user.groups.all()).exclude(id=request.user.id),
                                                                    )
        if 'remove' in request.POST:
            r_form = UsersGroupForm(request.POST)
            a_form=UsersGroupForm()
            form=r_form
        
        if a_form.is_valid() or r_form.is_valid():
            group = form.cleaned_data.get("group")
            users = [CustomUser.objects.get(pk=pk) for pk in request.POST.getlist("users", "")]

            for user in users:
                if user.groups.filter(id=group.id).count():
                    messages.success(request, f'{user.username} removed from group {group.name}.')
                    user.groups.remove(group)
                else:
                    user.groups.add(group)
                    messages.success(request, f'{user.username} added to group {group.name}.')

            return redirect('DMS-home')
    elif request.method =='GET':
        UsersGroupForm.base_fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(id__in=request.user.groups.all()),
                                                                    )
        UsersGroupForm.base_fields['users'] = forms.ModelChoiceField(queryset=CustomUser.objects.exclude(groups__in=request.user.groups.all()).exclude(id=request.user.id),
                                                                    )
        a_form = UsersGroupForm()

        UsersGroupForm.base_fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(id__in=request.user.groups.all()),
                                                                    )
        UsersGroupForm.base_fields['users'] = forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__in=request.user.groups.all()).exclude(id=request.user.id),
                                                                    )
        
        r_form = UsersGroupForm()
    context = {'a_form': a_form, 'r_form': r_form
             }
    return render(request, "Users/groups.html", context)

@csrf_exempt
def get_users_add(request):
    if request.method=='POST':
        group=request.POST.get('data')
        data=list()
        item=dict()
        users=CustomUser.objects.exclude(groups__id__in=group)
        users=list(users)
        for user in users:
            item['id']=user.id
            item['name']=user.username
            data.append(item)
            item=dict()
        return JsonResponse(data, safe=False)

@csrf_exempt
def get_users_remove(request):
    if request.method=='POST':
        group=request.POST.get('data')
        data=list()
        item=dict()
        users=CustomUser.objects.filter(groups__id__in=group)
        users=list(users)
        for user in users:
            item['id']=user.id
            item['name']=user.username
            data.append(item)
            item=dict()
        return JsonResponse(data, safe=False)

def unauthorised(request):
    return render(request, 'Users/unauthorised_access.html')