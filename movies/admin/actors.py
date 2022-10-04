from django.contrib import admin
from django import forms
from movies.models import Actor
from utils.utils_functions import upload_image


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = '__all__'

    image_file = forms.FileField()


class ActorAdmin(admin.ModelAdmin):
    form = ActorForm
    readonly_fields = ['id', 'image']

    def save_model(self, request, obj, form, change):
        # Uploading image
        obj = upload_image(obj, form.cleaned_data.get('image_file', None))
        super(ActorAdmin, self).save_model(request, obj, form, change)


admin.site.register(Actor, ActorAdmin)
