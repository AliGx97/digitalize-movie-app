from django.contrib import admin
from movies.models import Season


class SeasonAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


admin.site.register(Season, SeasonAdmin)
