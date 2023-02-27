from django.db import models

from jappl_time_log.models.base_model import BaseModel


class Example(BaseModel):
    """Database model example.

    each class represents as table in table (generate migration file and migrate this to database).
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    location = models.CharField(max_length=100, null=False, blank=False)
