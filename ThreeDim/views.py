from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.core.files.storage import FileSystemStorage
import os

from django.templatetags.static import static


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import tensorflow as tf
os.environ['CUDA_VISIBLE_DEVICES'] = "0"


def index(request):
    context={'a':1}
    return render(request, 'index.html', context)



###############################################################################

import sys
sys.path.insert(1, 'dl/model')

from backend_brain_pipeline import process_pipeline

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

def predict(request):
    context={'a':1}
    #print(request)
    #print(request.POST.dict)
    paths = []
    
    fs = OverwriteStorage()
    fileObj = request.FILES['filelocation1']
    filePathName1 = fs.save(fileObj.name, fileObj)
    filePathName1 = fs.url(fileObj.name)
    paths.append("."+filePathName1)
    
    fileObj = request.FILES['filelocation2']
    filePathName2 = fs.save(fileObj.name, fileObj)
    filePathName2 = fs.url(fileObj.name)
    paths.append("."+filePathName2)

    fileObj = request.FILES['filelocation3']
    filePathName3 = fs.save(fileObj.name, fileObj)
    filePathName3 = fs.url(fileObj.name)
    paths.append("."+filePathName3)

    fileObj = request.FILES['filelocation4']
    filePathName4 = fs.save(fileObj.name, fileObj)
    filePathName4 = fs.url(fileObj.name)
    paths.append("."+filePathName4)

    #context={'filePathName':filePathName}
    
    print(paths) 
    process_pipeline(paths, fname='ThreeDim/static/ThreeDim/out.gif')

    return render(request, 'index.html', context)