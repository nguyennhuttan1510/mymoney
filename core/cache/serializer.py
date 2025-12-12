import json
from typing import Any

from django.core.serializers.json import DjangoJSONEncoder

from core.cache.interface import Serializer


class JsonSerializer(Serializer):
    def serialize(self, data: Any):
        return json.dumps(data, cls=DjangoJSONEncoder)

    def deserialize(self, data: Any):
        return json.loads(data)