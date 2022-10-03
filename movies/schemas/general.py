import datetime

from ninja import Schema
from pydantic.types import UUID4


class MovieSerialOut(Schema):
    id: UUID4
    title: str
    image: str
    release_date: datetime.date
    is_movie: bool
