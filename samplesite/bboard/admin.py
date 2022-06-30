from django.contrib import admin
from bboard.models import FirstModel, Rubric, Person


class FirstModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'age')
    list_display_links = ('name', 'sex')
    search_fields = ('name', 'age')


admin.site.register(FirstModel, FirstModelAdmin)
admin.site.register(Rubric)
admin.site.register(Person, PersonAdmin)
