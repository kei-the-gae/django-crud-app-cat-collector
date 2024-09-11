from django.shortcuts import render, redirect
# Import HttpResponse to send text-based responses
# from django.http import HttpResponse
# Import CreateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Import Cat model
from .models import Cat, Toy
from .forms import FeedingForm

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
    # Instantiate cat to be rendered in the template
    cat = Cat.objects.get(id=cat_id)
    # Instantiate FeedingForm
    feeding_form = FeedingForm()
    return render(req, 'cats/detail.html', {
        # Include the cat and feeding_form in the context
        'cat': cat,
        'feeding_form': feeding_form
    })

# Define add feeding view function
def add_feeding(req, cat_id):
    # create a ModelForm instance using the data in req.POST
    form = FeedingForm(req.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat-detail', cat_id=cat_id)


# Define create class-based views (CBV) class
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # fields = ['name', 'breed', 'description', 'age']
    success_url = '/cats/'

# Define update CBV class
class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

# Define delete CBV class
class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'
