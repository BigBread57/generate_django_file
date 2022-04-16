from helpers import Helper
from settings import config


helpers = Helper()


def formation_dict_params(typer_start) -> dict:
    if typer_start:
        path_to_api = typer_start.get('path_to_api')
        app_name = typer_start.get('app_name')
    else:
        path_to_api = config('PATH_TO_API')
        app_name = config('APP_NAME')

    return {
        '{{path_to_app}}': path_to_api,
        '{{app_name}}': app_name,
        '{{AppName}}': helpers.str_camel(app_name),
        '{{app-name}}': app_name.replace('_', '-'),
    }

