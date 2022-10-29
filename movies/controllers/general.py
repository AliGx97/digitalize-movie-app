from django.core.paginator import Paginator
from django.db.models import Q, Value
from ninja import Router, Query
from itertools import chain
from movies.models import Movie, Serial, Episode
from movies.schemas.general import MovieSerialOut, AllEpisodes
from movies.schemas.movies import MovieOut
from movies.schemas.series import SerialOut
from utils.schemas import MessageOut

home_controller = Router(tags=['Home'])


# @home_controller.get('/search', response={200: list[MovieSerialOut], 404: MessageOut})
# def search(request, q: str = ' ', page: int = 1):
#     qs = (Q(title__icontains=q) | Q(description__icontains=q))
#     movies = Movie.objects.filter(qs).order_by('-rating').annotate(is_movie=Value(True))
#
#     series = Serial.objects.filter(qs).order_by(
#         '-rating').annotate(is_movie=Value(False))
#
#     if not movies and not series:
#         return 404, {'msg': 'There are no matches.'}
#     data = chain(movies, series)
#     sorted_data = sorted(data, key=lambda x: x.rating)
#     sorted_data = Paginator(sorted_data, 20)
#     if sorted_data.num_pages >= page:
#         return 200, list(sorted_data.page(page).object_list)
#     return 200, list(sorted_data)


@home_controller.get('/search/movies', response={200: list[MovieOut], 404: MessageOut})
def search_movies(request, q: str = ' '):
    qs = (Q(title__icontains=q) | Q(description__icontains=q))
    movies = Movie.objects.filter(qs).order_by('-rating')
    if not movies:
        return 404, {'msg': 'There are no matches.'}

    return 200, list(movies)


@home_controller.get('/search/series', response={200: list[SerialOut], 404: MessageOut})
def search_series(request, q: str = ' '):
    qs = (Q(title__icontains=q) | Q(description__icontains=q))
    series = Serial.objects.filter(qs).order_by('-rating')
    if not series:
        return 404, {'msg': 'There are no matches.'}
    return 200, list(series)


@home_controller.get('all-episodes-of-all-series', response={200: list[AllEpisodes]})
def get_all_episodes(request):
    episodes = Episode.objects.prefetch_related('guest_actors', 'season__serial__serial_actors').select_related(
        'season', 'season__serial').all()
    return 200, episodes
