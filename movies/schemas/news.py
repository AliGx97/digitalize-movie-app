import datetime

from ninja import Schema
from pydantic.types import UUID4


class NewOut(Schema):
    id: UUID4
    title: str
    description: str
    date: datetime.date
    image: str
