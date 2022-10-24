from ninja import Schema
from pydantic.types import UUID4


class ActorOut(Schema):
    id: UUID4
    name: str
    image: str = None
