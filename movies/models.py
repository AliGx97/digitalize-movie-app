from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Entity(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=False, db_column='created_at')
    updated = models.DateTimeField(auto_now=True, null=False, db_column='updated_at')


class Category(Entity):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CommonDetail(Entity):
    class Meta:
        abstract = True

    title = models.CharField(max_length=150)
    release_date = models.DateField(db_column='date')
    description = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    is_for_adults = models.BooleanField(default=False)
    trailer_url = models.URLField(null=True, blank=True)


class Actor(Entity):
    name = models.CharField(max_length=50)
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def all_movies(self):
        return self.movies.all()

    @property
    def all_series(self):
        return self.series.all()

    def get_all_series(self):
        return self.series.all()


class Movie(CommonDetail):
    is_featured = models.BooleanField(default=False)
    length = models.CharField(max_length=6)
    categories = models.ManyToManyField(Category, related_name='movies')
    user = models.ManyToManyField(User, related_name='favorite_movies', blank=True)
    image = models.URLField(null=True)
    thumbnail = models.URLField(null=True, editable=False)
    movie_actors = models.ManyToManyField(Actor, related_name='movies', blank=True)

    def __str__(self):
        return self.title

    @property
    def actors(self):
        return self.movie_actors.all()


class Serial(CommonDetail):
    is_featured = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='series')
    user = models.ManyToManyField(User, related_name='favorite_series', blank=True)
    image = models.URLField(null=True)
    thumbnail = models.URLField(null=True, editable=False)
    serial_actors = models.ManyToManyField(Actor, related_name='series', blank=True)

    def __str__(self):
        return self.title

    @property
    def actors(self):
        return self.actors.all()

    @property
    def all_seasons(self):
        return self.seasons.all()


class Season(Entity):
    number = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message='Minimum season for any series is 1')])
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name='seasons')

    def __str__(self):
        return f'{self.serial.title} || Season {self.number}'


class Episode(CommonDetail):
    number = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message='Minimum season for any episode is 1')])
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    length = models.CharField(max_length=6)
    guest_actors = models.ManyToManyField(Actor, related_name='episodes', blank=True)

    def __str__(self):
        return f'{self.season} || {self.title}'

    @property
    def actors(self):
        return list(self.season.serial.serial_actors.all()) + list(self.guest_actors.all())

    @property
    def image(self):
        return self.season.serial.image


class New(Entity):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(db_column='date')
    image = models.URLField(unique=True, null=True)

    def __str__(self):
        return self.title
