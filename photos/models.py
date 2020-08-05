import os

from django.db import models
# Create your models here.
from django.urls import reverse


class Images(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    croup_image = models.ImageField(upload_to='images_crop/%Y/%m/%d/', blank=True)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.filename()

    def filename(self):
        return os.path.basename(self.image.name)

    def get_absolute_url(self):
        return reverse('update', kwargs={'pk': self.pk})

    def get_image_url(self):
        if self.croup_image:
            return self.croup_image.url
        return self.image.url

    def save(self, *args, **kwargs):
        if self.croup_image:
            self.height = self.croup_image.height
            self.width = self.croup_image.width
        elif self.image:
            self.height = self.image.height
            self.width = self.image.width
        return super().save(*args, **kwargs)
