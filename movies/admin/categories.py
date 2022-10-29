from django.contrib import admin

from movies.models import Category


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


admin.site.register(Category, CategoryAdmin)
# admin.site.register(Category)
