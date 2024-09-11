from django.shortcuts import render
# Import HttpResponse to send text-based responses
# from django.http import HttpResponse
# Import CreateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Import Cat model
from .models import Cat

#Temporary import of cat data
# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# Create a list of Cat instances
# cats = [
#     Cat('Lolo', 'tabby', 'Kinda rude.', 3),
#     Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
#     Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
#     Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
# ]

# Create your views here.
# Define home view function
def home(req):
    # Send a simple HTML response
    # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
    return render(req, 'home.html')

# Define about view function
def about(req):
    return render(req, 'about.html')

# Define cat index view function
def cat_index(req):
    cats = Cat.objects.all() # look familiar?
    return render(req, 'cats/index.html', {'cats': cats})

# Define cat detail view function
def cat_detail(req, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(req, 'cats/detail.html', {'cat': cat})

# Define create class-based views (CBV) class
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # fields = ['name', 'breed', 'description', 'age']
    success_url = '/cats/'

#Define update CBV class
class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']
    
#Define delete CBV class
class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'
