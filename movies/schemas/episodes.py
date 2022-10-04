import datetime

from ninja import Schema
from pydantic.types import UUID4, Decimal, Optional

from movies.schemas.Actor import ActorOut


class EpisodeOut(Schema):
    id: UUID4
    title: str
    description: str
    trailer_url: Optional = str
    release_date: datetime.date
    rating: Decimal
    actors: Optional = list[ActorOut]
    image: str
