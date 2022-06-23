from django.contrib import admin
from dokk.models import SecondModel
from dokk.models import Rubrictwo


class SecondModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

admin.site.register(SecondModel, SecondModelAdmin)
admin.site.register(Rubrictwo)
