from django.contrib import admin
from django import forms
from movies.models import Episode
from utils.utils_functions import upload_image


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'

    image_file = forms.FileField()


class EpisodeAdmin(admin.ModelAdmin):
    form = EpisodeForm
    readonly_fields = ['image']

    def save_model(self, request, obj, form, change):
        # Uploading image
        obj = upload_image(obj, form.cleaned_data.get('image_file', None))
        super(EpisodeAdmin, self).save_model(request, obj, form, change)


admin.site.register(Episode, EpisodeAdmin)
