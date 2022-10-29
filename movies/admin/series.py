from django.contrib import admin
from django import forms
from movies.models import Serial
from utils.utils_functions import upload_image


class SerialForm(forms.ModelForm):
    class Meta:
        model = Serial
        fields = '__all__'

    image_file = forms.FileField(required=False)


class SerialAdmin(admin.ModelAdmin):
    form = SerialForm
    readonly_fields = ['id', 'image', 'thumbnail']
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        # Uploading image
        obj = upload_image(obj, form.cleaned_data.get('image_file', None))
        super(SerialAdmin, self).save_model(request, obj, form, change)


admin.site.register(Serial, SerialAdmin)
# admin.site.register(Serial)
