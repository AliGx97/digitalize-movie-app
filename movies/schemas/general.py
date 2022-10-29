import datetime

from ninja import Schema
from pydantic.types import UUID4, Optional, Decimal

from movies.schemas.Actor import ActorOut
from movies.schemas.seasons import SeasonOut


class MovieSerialOut(Schema):
    id: UUID4
    title: str
    image: str
    release_date: datetime.date
    is_movie: bool


class AllEpisodes(Schema):
    id: UUID4
    title: str
    description: str
    trailer_url: Optional = str
    release_date: datetime.date
    rating: Decimal
    image: str
    season: SeasonOut
    actors: list[ActorOut]
