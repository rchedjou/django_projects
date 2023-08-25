from django.contrib import admin
from .models import Image

# Register your models here.
@admin.register(Image)

class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'slug', 'image', 'created']
    raw_id_fields = ['user']
    list_filter = ['created']
    

