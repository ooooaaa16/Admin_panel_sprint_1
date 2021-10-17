# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Genre(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = '"content"."genre"'

    def __str__(self):
        return self.name

class GenreFilmwork(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, db_column='film_work_id')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, db_column='genre_id')
    created_at = models.DateTimeField(auto_now_add=True)

    indexes = [
        models.Index(name='film_work_genre', fields=['film_work_id', 'genre_id']),
    ]

    class Meta:
        db_table = '"content"."genre_film_work"'

class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')

class PersonRoleType(models.TextChoices):
    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    PRODUCER = 'producer', _('producer')

class Person(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    full_name = models.CharField(_('Full name'), max_length=255)
    birth_date = models.DateField(_('Birth date'), blank=True)

    class Meta:
        db_table = '"content"."person"'

    def __str__(self):
        return self.full_name

class Filmwork(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    certificate = models.TextField(_('certificate'), blank=True)
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    indexes = [
        models.Index(name='film_work_creation_date_idx', fields=['creation_date']),
    ]

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = '"content"."film_work"'

    def __str__(self):
        return self.title

class FilmworkPerson(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE, db_column='film_work_id')
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(_('type'), max_length=20, choices=PersonRoleType.choices)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, db_column='person_id')

    indexes = [
        models.Index(name='film_work_person_role', fields=['film_work_id', 'person', 'role']),
    ]

    class Meta:
        db_table = '"content"."person_film_work"'
