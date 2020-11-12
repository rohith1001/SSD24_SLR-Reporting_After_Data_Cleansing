from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document', False)
        if(uploaded_file != False):
            print(uploaded_file.name)
            print(uploaded_file.size)
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def homeView(request):
    return render(request, 'home.html', {})
