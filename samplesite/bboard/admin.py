from django.contrib import admin
from bboard.models import FirstModel, Rubric, Person


class FirstModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

class RubricAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    list_display_links = ('name', 'owner')
    search_fields = ('name', 'owner')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'age')
    list_display_links = ('name', 'sex')
    search_fields = ('name', 'age')


admin.site.register(FirstModel, FirstModelAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Rubric, RubricAdmin)
