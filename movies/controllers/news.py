from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.responses import codes_4xx
from pydantic.types import UUID4

from movies.models import New
from movies.schemas.news import NewOut
from utils.schemas import MessageOut

news_controller = Router(tags=['News Controller'])


@news_controller.get('', response={200: list[NewOut], 404: MessageOut})
def list_news(request):
    news = New.objects.all().order_by('-date')
    if not news:
        return 404, {'msg': 'There are no news yet'}
    return 200, news


@news_controller.get('/{id}', response={200: NewOut, codes_4xx: MessageOut})
def get_new(request, id: UUID4):
    try:
        new = New.objects.get(id=id)
        return 200, new
    except New.DoesNotExist:
        return 404, {'msg': 'News with that id was not found'}
