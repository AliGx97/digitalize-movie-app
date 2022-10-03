from ninja import Schema
import datetime

from pydantic.types import Decimal, UUID4
from pydantic import Field

from movies.schemas.Actor import ActorOut
from movies.schemas.categories import CategoryOut


class MovieIn(Schema):
    title: str
    release_date: datetime.date
    description: str
    rating: Decimal = Field(..., max_digits=2, decimal_places=1)
    length: str


class MovieOut(Schema):
    id: UUID4
    title: str
    description: str
    trailer_url: str
    release_date: datetime.date
    rating: Decimal
    categories: list[CategoryOut]
    actors: list[ActorOut]
