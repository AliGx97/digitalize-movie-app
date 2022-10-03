from django.contrib import admin
from django import forms
from movies.models import Movie
from utils.utils_functions import upload_image


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

    image_file = forms.FileField()


class MovieAdmin(admin.ModelAdmin):
    form = MovieForm
    readonly_fields = ['image']

    def save_model(self, request, obj, form, change):
        # Convert number of minutes to sting representation
        time = int(obj.length)
        hours = time // 60
        minutes = time - (hours * 60)
        obj.length = f'{hours}h {minutes}m'

        # Uploading image
        obj = upload_image(obj, form.cleaned_data.get('image_file', None))
        super(MovieAdmin, self).save_model(request, obj, form, change)


admin.site.register(Movie, MovieAdmin)
