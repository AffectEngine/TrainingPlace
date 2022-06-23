from django.contrib import admin
from bboard.models import FirstModel
from bboard.models import Rubric


class FirstModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

admin.site.register(FirstModel, FirstModelAdmin)
admin.site.register(Rubric)
