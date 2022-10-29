from django.contrib import admin
from django import forms
from movies.models import Episode


class EpisodeInline(admin.StackedInline):
    model = Episode
    fields = ['title', 'description', 'release_date', 'number', 'length', 'guest_actors']
    extra = 1


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'


class EpisodeAdmin(admin.ModelAdmin):
    form = EpisodeForm
    readonly_fields = ['id']
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        time = int(obj.length)
        hours = time // 60
        minutes = time - (hours * 60)
        obj.length = f'{hours}h {minutes}m'
        super(EpisodeAdmin, self).save_model(request, obj, form, change)


admin.site.register(Episode, EpisodeAdmin)
# admin.site.register(Episode)
