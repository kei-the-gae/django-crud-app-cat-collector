from django.contrib import admin
# Import Cat model
from .models import Cat, Feeding, Toy

# Register your models here.
admin.site.register(Cat)
admin.site.register(Feeding)
admin.site.register(Toy)
