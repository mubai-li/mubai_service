from django.shortcuts import render

# Create your views here.

from apps.file_app import models

# views.py

from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadFileModel


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def success(request):
    return render(request, 'success.html')
