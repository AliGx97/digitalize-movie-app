from ninja import Schema
import datetime

from pydantic.types import Decimal, UUID4, Optional
from pydantic import Field

from movies.schemas.Actor import ActorOut
from movies.schemas.categories import CategoryOut


class MovieOut(Schema):
    id: UUID4
    title: str
    description: str
    image: str
    thumbnail: str
    trailer_url: Optional = str
    release_date: datetime.date
    rating: Decimal
    categories: list[CategoryOut]
    movie_actors: list[ActorOut]
