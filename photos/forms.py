from django import forms


class UploadImageForm(forms.Form):
    image_url = forms.CharField(max_length=1000, required=False)
    image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        image_url = cleaned_data.get("image_url")
        image = cleaned_data.get("image")
        if image_url and image:
            msg = "Нельзя дать одно временно два инпута"
            self.add_error('image', msg)
            self.add_error('image_url', msg)
        elif not (image_url or image):
            msg = "Заполните хотябы один"
            self.add_error('image', msg)
            self.add_error('image_url', msg)


class UpdateImageForm(forms.Form):
    height = forms.IntegerField(min_value=1)
    width = forms.IntegerField(min_value=1)

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get("height")
        width = cleaned_data.get("width")
        if not (width != '' or height != ''):
            msg = "Заполните хотябы один"
            self.add_error('width', msg)
            self.add_error('height', msg)
