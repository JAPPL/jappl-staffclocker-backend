from dataclasses import dataclass

from dataclasses_json import dataclass_json
from rest_framework_dataclasses.serializers import DataclassSerializer


@dataclass_json
@dataclass
class FirebasePayLoadDataclass:
    """Dataclass for decoded firebase token."""

    name: str
    email: str


class FirebasePayloadSerializer(DataclassSerializer):
    """Dataclass serializer for decoded firebase token."""

    class Meta:
        """Metadata class to specify base dataclass and fields."""

        dataclass = FirebasePayLoadDataclass
        fields = "__all__"
