from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import FormView
from .forms import OCRUploadForm
import pytesseract
from PIL import Image
from django.contrib.auth.mixins import LoginRequiredMixin
import os

class OCR(LoginRequiredMixin,FormView):
    form_class = OCRUploadForm
    template_name = 'OCR/OCR.html'
    success_url = '/'

@csrf_exempt
def image_ocr(request):
    lang = r'-l eng+ron'
    if request.method == 'POST':
        data = dict()
        upload = request.FILES['file']
        text = pytesseract.image_to_string(Image.open(upload), config=lang)
        searchable_pdf=pytesseract.image_to_pdf_or_hocr(Image.open(upload), extension='pdf')
        path=f'media\OCR\{request.user.username}'
        os.makedirs(path,exist_ok=True)
        name ,extension = upload.name.split('.')
        with open(f'{path}\{name}.pdf', 'wb') as file:
            file.write(searchable_pdf)
        data['text'] = text

        return JsonResponse(data)