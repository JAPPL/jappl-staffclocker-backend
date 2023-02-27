from django.db import models
from rest_framework import status
from rest_framework.exceptions import APIException


class BaseModel(models.Model):
    """Base mode to keep modify and create time."""

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class NotFoundAPIException(APIException):
        """Error API exception handling."""

        status_code = status.HTTP_404_NOT_FOUND
        default_code = 'Not found'
        default_detail = 'That object cannot be found'

    class Meta:
        """Meta data to tell this class is abstract."""

        abstract = True
