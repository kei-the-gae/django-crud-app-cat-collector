from django.shortcuts import render
# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Create your views here.
# Define home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')