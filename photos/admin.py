from django.contrib import admin

# Register your models here.
from photos.models import Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    pass