from django.shortcuts import render, redirect
# Import HttpResponse to send text-based responses
# from django.http import HttpResponse
# Import CreateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
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
# def home(req):
#     # Send a simple HTML response
#     # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
#     return render(req, 'home.html')
class Home(LoginView):
    template_name = 'home.html'

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
    # toys = Toy.objects.all()
    # Only get the toys the cat does not have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    # Instantiate FeedingForm
    feeding_form = FeedingForm()
    return render(req, 'cats/detail.html', {
        # Include the cat and feeding_form in the context
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have # send those toys
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

def associate_toy(req, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)

def remove_toy(req, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('cat-detail', cat_id=cat_id)

def signup(req):
    error_message = ''
    if req.method == 'POST':
        # This is how to create a 'user' form object that includes the data from the browser
        form = UserCreationForm(req.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(req, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(req, 'signup.html', context)
    # Same as:
    # return render(
    #     request,
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )


# Define create class-based views (CBV) class
class CatCreate(CreateView):
    model = Cat
    # fields = '__all__'
    fields = ['name', 'breed', 'description', 'age']
    # This inherited method is called when a valid cat form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)
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

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
