from django.urls import path
from . import views

urlpatterns = [
    path('terms_conditions/', views.terms_conditions, name='Users-terms_conditions'),
    path('privacy_policy/', views.privacy_policy, name='Users-privacy_policy'),
    path('profile/<int:pk>', views.ProfilePage.as_view(), name='Users-profile_data'),
    path('groups/', views.group_management, name='Users-Groups'),
    path('get_users_add', views.get_users_add, name='get_users_add'),
    path('get_users_remove', views.get_users_remove, name='get_users_remove')
]