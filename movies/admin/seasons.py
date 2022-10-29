from django.contrib import admin
from movies.models import Season
from movies.admin.episodes import EpisodeInline


class SeasonAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    inlines = (EpisodeInline,)


admin.site.register(Season, SeasonAdmin)
# admin.site.register(Season)
