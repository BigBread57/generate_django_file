from rest_framework import serializers

from {{path_to_app}}.models import {{main_class}}


class {{main_class}}Serializer(serializers.ModelSerializer):
    """{{docs}}"""

    class Meta(object):
        model = {{main_class}}
        fields = {{list_main_fields}}


class {{main_class}}Serializer(serializers.Serializer):
    """{{docs}}"""
