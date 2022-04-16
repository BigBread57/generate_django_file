from src.settings import config


DICT_PARAMS = {
    '{{path_to_app}}': config('PATH_TO_API'),
    '{{app_name}}': config('APP_NAME'),
    '{{AppName}}': config('APP_NAME'),
    '{{app-name}}': config('APP_NAME').replace('_', '-'),
}
