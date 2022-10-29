from django.contrib import admin
from django import forms
from movies.models import Movie
from utils.utils_functions import upload_image


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

    image_file = forms.FileField(required=False)


class MovieAdmin(admin.ModelAdmin):
    form = MovieForm
    readonly_fields = ['id', 'image', 'thumbnail']
    search_fields = ['title']
    ordering = ['title', 'rating']
    list_display = ['title', 'length', 'rating', 'actors_of_movie']
    list_filter = ['categories']
    list_select_related = True

    def actors_of_movie(self, obj):
        return list(obj.actors)

    actors_of_movie.admin_order_field = 'movie_actors'
    actors_of_movie.short_description = 'Actors'

    def save_model(self, request, obj, form, change):
        # Convert number of minutes to sting representation
        time = int(obj.length)
        hours = time // 60
        minutes = time - (hours * 60)
        obj.length = f'{hours}h {minutes}m'

        # Uploading image
        obj = upload_image(obj, form.cleaned_data.get('image_file', None))
        super(MovieAdmin, self).save_model(request, obj, form, change)

    # def get_deleted_objects(self, objs, request):
        

admin.site.register(Movie, MovieAdmin)
# admin.site.register(Movie)
