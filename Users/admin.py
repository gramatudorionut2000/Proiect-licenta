from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserRegisterForm, CustomUserChangeForm
from .models import CustomUser
from django.http import HttpResponse
import csv

admin.site.register(Profile)
admin.site.site_header = 'EDMS administration'
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserRegisterForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email",'first_name','last_name',"is_manager"]
    ordering = ['username']
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'is_manager',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    @admin.action(description="Generate CSV")
    def generateCSV(self, request, queryset):
        filename = self.model._meta
        public_fields=['username','first_name','last_name','email']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;   filename={}.csv'.format(filename)
        writer = csv.writer(response)

        writer.writerow(public_fields)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in public_fields])

        return response
    actions = [generateCSV]

admin.site.register(CustomUser, CustomUserAdmin)

