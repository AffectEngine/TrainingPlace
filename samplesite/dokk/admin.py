from django.contrib import admin
from dokk.models import SecondModel


class SecondModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

admin.site.register(SecondModel, SecondModelAdmin)
