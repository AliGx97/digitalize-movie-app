from ninja import Schema
from pydantic.types import UUID4


class CategoryOut(Schema):
    id: UUID4
    name: str
