# Create your views here.
import os
from urllib.request import urlretrieve

from PIL import Image
from django.core.files import File
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from photos.models import Images
from .forms import UploadImageForm, UpdateImageForm


class HomePage(ListView):
    model = Images
    template_name = 'base.html'
    context_object_name = 'images'


class CreateImage(View):
    template_name = 'update.html'
    form_class = UploadImageForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            image = Images()
            if data.get('image_url'):
                image_in_url = urlretrieve(data.get('image_url'))
                name = os.path.basename(data.get('image_url'))
                if name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    file = open(image_in_url[0], 'rb')
                    image.image.save(name, File(file))
                    image.save()
                    return redirect(image.get_absolute_url())
                form.add_error('image_url', 'Это не сылка фото')
            else:
                image.image = form.cleaned_data.get('image')
                image.save()
                return redirect(image.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class UpdateImage(View):
    template_name = 'update.html'
    form_class = UpdateImageForm
    height = None
    width = None
    object = None

    def dispatch(self, request, *args, **kwargs):
        if self.object is None:
            self.object = get_object_or_404(Images, pk=kwargs.get('pk'))
        return super(UpdateImage, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        initial = {
            'height': self.object.height,
            'width': self.object.width
        }
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form, 'object': self.object})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            file = open(self.object.image.path, 'rb')
            self.object.croup_image.save(self.object.filename(), File(file))
            self.object.save()
            width, height = [data.get('width'), data.get('height')]
            image = Image.open(self.object.croup_image.path)
            image = image.resize((width, height), Image.ANTIALIAS)
            image.save(self.object.croup_image.path)
        return render(request, self.template_name, {'form': form, 'object': self.object})
