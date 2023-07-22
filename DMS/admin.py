from django.contrib import admin
from .models import Document, Tag, Folder
from reversion.admin import VersionAdmin

@admin.register(Document)
class Document(VersionAdmin):
    pass

admin.site.register(Tag)
admin.site.register(Folder)