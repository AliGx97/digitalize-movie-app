from ninja import Schema
import datetime

from pydantic.types import Decimal, UUID4

from movies.schemas.Actor import ActorOut
from movies.schemas.categories import CategoryOut


class SerialOut(Schema):
    id: UUID4
    title: str
    description: str
    trailer_url: str
    release_date: datetime.date
    rating: Decimal
    categories: list[CategoryOut]
    actors: list[ActorOut]


class FullSerialOut(SerialOut):
    seasons: list[UUID4]
