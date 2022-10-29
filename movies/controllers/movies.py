from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic.types import UUID4

from account.authorization import TokenAuthentication
from movies.models import Movie
from movies.schemas.movies import MovieOut
from utils.schemas import MessageOut

User = get_user_model()

movies_controller = Router(tags=['Movies'])


@movies_controller.get('', response={200: list[MovieOut], 404: MessageOut})
def list_movies(request, page: int = 1):
    movies = Movie.objects.prefetch_related('categories', 'movie_actors').all()
    if not movies:
        return 404, {'msg': 'There are no movies yet.'}
    data = Paginator(movies, 20)
    if data.num_pages >= page:
        return 200, list(data.page(page).object_list)
    return 200, list(data)


@movies_controller.get('/featured', response={200: list[MovieOut], 404: MessageOut})
def featured_movies(request):
    movies = Movie.objects.filter(is_featured=True).order_by('-rating')
    if movies:
        return 200, movies
    return 404, {'msg': 'There are no featured movies.'}


@movies_controller.get('/favorites', auth=TokenAuthentication(), response={200: list[MovieOut], 404: MessageOut})
def favorite_movies(request):
    movies = Movie.objects.filter(user__exact=request.auth['id']).order_by('-rating')
    if movies:
        return 200, movies
    return 404, {'msg': 'There are no featured movies.'}


@movies_controller.post('/favorites/{id}', auth=TokenAuthentication(), response={200: MessageOut, 404: MessageOut})
def add_favorite_movie(request, id: UUID4):
    user = User.objects.get(id=request.auth['id'])
    movie = get_object_or_404(Movie, id=id)
    user.favorite_movies.add(movie)
    return 200, {'msg': 'Movie added successfully.'}


@movies_controller.delete('/favorites/{id}', auth=TokenAuthentication(), response={200: MessageOut, 404: MessageOut})
def delete_favorite_movie(request, id: UUID4):
    user = User.objects.get(id=request.auth['id'])
    movie = get_object_or_404(Movie, id=id)
    user.favorite_movies.remove(movie)
    return 200, {'msg': 'Movie removed successfully.'}


@movies_controller.get('/{id}', response={200: MovieOut, 404: MessageOut})
def get_movie(request, id: UUID4):
    try:
        movie = Movie.objects.get(id=id)
        return 200, movie
    except Movie.DoesNotExist:
        return 404, {'msg': 'There is no movie with that id.'}
