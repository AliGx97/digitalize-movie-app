from django.contrib import admin
import requests
# Register your models here.
from movies.models import Movie, New
from django.conf import settings
from django import forms


class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = '__all__'

    image_file = forms.FileField(required=False)


class NewAdmin(admin.ModelAdmin):
    form = NewForm
    readonly_fields = ['id', 'image']

    def save_model(self, request, obj, form, change):
        print(request.POST)
        print(obj.image)
        image_file = form.cleaned_data.get('image_file', None)
        if image_file:
            res = requests.post(
                url=settings.IMGBB_URL,
                files={'image': image_file.read()},
                params={'key': settings.IMGBB_KEY}
            )
            if res.ok:
                obj.image = res.json()['data']['url']
            else:
                obj.image = None
        super(NewAdmin, self).save_model(request, obj, form, change)


admin.site.register(New, NewAdmin)
# admin.site.register(New)
