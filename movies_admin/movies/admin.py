from django.contrib import admin
from .models import Filmwork, Genre, Person
from .models import GenreFilmwork, FilmworkPerson

class GenreInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 2

class PersonInline(admin.TabularInline):
    model = FilmworkPerson
    extra = 2

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating')
    # поиск по полям
    search_fields = ('title', 'description', 'id')
    # порядок следования полей в форме создания/редактирования
    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating'
    )
    inlines = [GenreInline, PersonInline]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('name', 'description')
    # поиск по полям
    search_fields = ('name',)
    fields = ('name', 'description')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('full_name', 'birth_date')
    # поиск по полям
    search_fields = ('full_name',)
    fields = ('full_name', 'birth_date')