import io
from django.http.response import HttpResponse, Http404
from numpy import NaN
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.serializers import *
from .models import *
from django.contrib import messages
from rest_framework.decorators import api_view
import pandas as pd
import numpy as np
import os
import sys
import csv
from pathlib import Path
from django.core.files.base import ContentFile

BASE_DIR = Path(__file__).resolve().parent.parent


def error_404(request, exception):
        return render(request,'CloudProjectApp/404.html')


def processData(data):
    
    return dataProcessed.to_csv()

@api_view(['GET', 'POST'])
def home(request):
    if request.method == 'GET':
        files = FileProcessed.objects.all()
        context = {'files':files}
        return render(request, 'CloudProjectApp/index.html', context)
    elif request.method == 'POST':
        if request.FILES['file'] == None:
            messages.warning(request, 'You should ')
            pass
        else:
            file = request.FILES['file']
            name = os.path.splitext(file.name)[0]
            data = pd.read_csv(file)
            fileInitial = FileInitial.objects.create(file=file)
            fileInitial.save()
            columns = list(data.columns.values)
            for column in columns:
                strs = list(filter(lambda x : type(x) ==str, data[column].unique().tolist()))
                ints = list(filter(lambda x: type(x) == int, data[column].unique().tolist()))
                floats = list(filter(lambda x: type(x) == float, data[column].unique().tolist()))
                output = sorted(floats) + sorted(strs) + sorted(ints)
                if len(output) == 2:       
                    data.loc[data[column] == output[0], column] = 0
                    data.loc[data[column] == output[1], column] = 1
                    data[column] = data[column].astype(float)
                if len(output) == 3:
                    data.loc[data[column] == output[0], column] = 0
                    data.loc[data[column] == output[1], column] = 1
                    data.loc[data[column] == output[2], column] = 2
                    data[column] = data[column].astype(float)
                if len(data[column].unique().tolist()) == 4:
                    data.loc[data[column] == output[0], column] = 0
                    data.loc[data[column] == output[1], column] = 1
                    data.loc[data[column] == output[2], column] = 2
                    data.loc[data[column] == output[3], column] = 3
                    data[column] = data[column].astype(float)
                    
            data = data.select_dtypes(include=np.number)
            columns = list(data.columns.values)
            for column in columns:
                data[column] = data[column].fillna((data[column].mean()))
            
            file_processed = ContentFile(data.to_csv())
            file_processed.name = name+'_processed.csv'
            fileProcessed = FileProcessed.objects.create(file=fileInitial, file_cleared=file_processed)
            fileProcessed.save()
            

        files = FileProcessed.objects.filter(file=fileInitial)
        context = {'files':files}
        return render(request, 'CloudProjectApp/index.html', context)


def download_file(request, pk):
    file = get_object_or_404(FileInitial, id_file=pk)
    file_location = os.path.join(BASE_DIR, 'media/'+file.file.name)
    with open(file_location, 'r') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file)
    return response

def download_file_cleared(request, pk):
    file_processed = get_object_or_404(FileProcessed, id_file_cleared=pk)
    file_location = os.path.join(BASE_DIR, 'media/'+file_processed.file_cleared.name)
    with open(file_location, 'r') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_processed)
    return response
