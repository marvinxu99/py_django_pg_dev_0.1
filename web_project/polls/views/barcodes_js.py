
from django.shortcuts import render
from django.conf import settings
import datetime
import os


def generate_barcode_js(request):
    
    return render(request, 'polls/barcode_gen_js.html')
