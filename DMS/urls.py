from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.DocListView.as_view(), name='DMS-home'),
    path('tag/', views.tag, name='tag'),
    path('tag/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag-delete'),
    path('document/<int:pk>/', views.DocDetailView.as_view(), name='document-detail'),
    path('document/new/', views.DocCreateView.as_view(), name='DMS-upload'),
    re_path(r'^download/(?P<id>\w+)/$', views.download, name='document_download'),
    path('document/<int:pk>/delete/', views.DocDeleteView.as_view(), name='document-delete'),
    path('document/<int:pk>/update/', views.DocUpdateView.as_view(), name='document-update'),
    re_path(r'^document/(?P<id>\w+)/version_list/$', views.document_version_list, name='document-version-list'),
    re_path(r'^document/(?P<id>\w+)/version_list/(?P<revision_id>\w+)/$', views.document_confirm_restore, name='document_confirm_restore'),
    re_path(r'^document/(?P<id>\w+)/version_list/(?P<revision_id>\w+)/restore/$', views.document_restore, name='document-restore'),
    path('about/', views.about, name='DMS-about'),
    path('folders/new/', views.FolderCreateView.as_view(), name='folder-create'),
    path('folders/', views.FolderListView.as_view(), name='folders'),
    path('folders/<int:pk>/delete/', views.FolderDeleteView.as_view(), name='folder-delete'),
]