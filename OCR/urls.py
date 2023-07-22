from django.urls import path
from . import views

urlpatterns = [
    path('ocr/', views.OCR.as_view(), name='OCR-ocr'),
    path('process_file', views.image_ocr, name='image_ocr'),
]