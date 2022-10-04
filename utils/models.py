from django.db import models
import uuid


class Entity(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=False, db_column='created_at')
    updated = models.DateTimeField(auto_now=True, null=False, db_column='updated_at')
