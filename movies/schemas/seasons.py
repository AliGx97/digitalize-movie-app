from ninja import Schema
from pydantic.types import UUID4


class SeasonOut(Schema):
    id: UUID4
    number: int
