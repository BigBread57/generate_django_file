from django.contrib import admin
from {{path_to_app}}.model import {{main_class}}


@admin.register({{main_class}})
class ConfigurableAdmin(admin.ModelAdmin[{{main_class}}]):
    """{{docs}}"""

    list_filter = {{list_main_fields}}
    search_fields = {{list_main_fields}}
    list_display = {{list_main_fields}}
