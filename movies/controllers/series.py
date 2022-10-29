from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic.types import UUID4

from account.authorization import TokenAuthentication
from movies.models import Serial, Season, Episode
from movies.schemas.episodes import EpisodeOut
from movies.schemas.seasons import SeasonOut
from movies.schemas.series import SerialOut, FullSerialOut
from utils.schemas import MessageOut

User = get_user_model()
series_controller = Router(tags=['Series'])


@series_controller.get('', response={200: list[SerialOut], 404: MessageOut})
def list_series(request, page: int = 1):
    series = Serial.objects.prefetch_related('categories', 'serial_actors').all().order_by('title')
    if not series:
        return 404, {'msg': 'There are no series yet.'}
    data = Paginator(series, 20)
    if data.num_pages >= page:
        return 200, list(data.page(page).object_list)
    return 200, list(data)


@series_controller.get('/featured', response={200: list[SerialOut], 404: MessageOut})
def featured_series(request):
    series = Serial.objects.filter(is_featured=True).order_by('-rating')
    if series:
        return 200, series
    return 404, {'msg': 'There are no featured series.'}


@series_controller.get('/favorites', auth=TokenAuthentication(), response={200: list[SerialOut], 404: MessageOut})
def favorite_series(request):
    series = Serial.objects.filter(user__exact=request.auth['id']).order_by('-rating')
    if series:
        return 200, series
    return 404, {'msg': 'There are no featured movies.'}


@series_controller.post('/favorites/{id}', auth=TokenAuthentication(), response={200: MessageOut, 404: MessageOut})
def add_favorite_serial(request, id: UUID4):
    user = User.objects.get(id=request.auth['id'])
    serial = get_object_or_404(Serial, id=id)
    user.favorite_series.add(serial)
    return 200, {'msg': 'Serial added successfully.'}


@series_controller.delete('/favorites/{id}', auth=TokenAuthentication(), response={200: MessageOut, 404: MessageOut})
def delete_favorite_serial(request, id: UUID4):
    user = User.objects.get(id=request.auth['id'])
    serial = get_object_or_404(Serial, id=id)
    user.favorite_series.remove(serial)
    return 200, {'msg': 'Serial removed successfully.'}


@series_controller.get('/{id}', response={200: FullSerialOut, 404: MessageOut})
def get_serial(request, id: UUID4):
    try:
        serial = Serial.objects.get(id=id)
        return 200, serial
    except Serial.DoesNotExist:
        return 404, {'msg': 'There is no serial with that id.'}


@series_controller.get('/{id}/seasons', response={200: list[SeasonOut], 404: MessageOut})
def get_seasons(request, id: UUID4):
    try:
        serial = Serial.objects.get(id=id)
        seasons = serial.seasons.all().order_by('number')
        return 200, seasons
    except Serial.DoesNotExist:
        return 404, {'msg': 'There is no serial with that id.'}


@series_controller.get('/{serial_id}/seasons/{season_id}/episodes', response={200: list[EpisodeOut], 404: MessageOut})
def list_episodes(request, serial_id: UUID4, season_id: UUID4):
    try:
        season = Season.objects.get(id=season_id, serial__id=serial_id)
        episodes = season.episodes.all().order_by('number')
        print(episodes)
        return 200, episodes
    except Season.DoesNotExist:
        return 404, {'msg': 'There is no season that matches the criteria.'}


@series_controller.get('/{serial_id}/seasons/{season_id}/episodes/{episode_id}',
                       response={200: EpisodeOut, 404: MessageOut})
def get_episodes(request, serial_id: UUID4, season_id: UUID4, episode_id: UUID4):
    try:
        season = Season.objects.get(id=season_id, serial_id=serial_id)
        episode = season.episodes.get(id=episode_id)
        return 200, episode
    except Season.DoesNotExist:
        return 404, {'msg': 'There is no season with that id.'}
    except Episode.DoesNotExist:
        return 404, {'msg': 'There is no episode that matches the criteria.'}
