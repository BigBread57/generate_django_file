from rest_framework.viewsets import ModelViewSet

from {{path_to_app}}.api.serializers import {{main_class}}Serializer
from {{path_to_app}}.models import {{main_class}}


class {{main_class}}ViewSet(ModelViewSet):
    """{{docs}}"""

    queryset = {{main_class}}.objects.all()
    serializer_class = {{main_class}}Serializer
    ordering_fields = {{list_main_fields}}
    search_fields = {{list_main_fields}}



from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from {{path_to_app}}.api.serializers import AccountSerializer
from {{path_to_app}}.models import Account

class {{main_class}}ViewSet(
    NestedViewSetMixin,
    AutoPermissionViewSetMixin,
    ModelViewSet,
):
    """{{docs}}"""

    queryset = {{main_class}}.objects.all()
    serializer_class = {{main_class}}Serializer
    ordering_fields = {{list_main_fields}}
    search_fields = {{list_main_fields}}
    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }
