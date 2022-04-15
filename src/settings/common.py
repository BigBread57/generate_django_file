import os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).parent.parent.parent.joinpath('config/.env')
load_dotenv(dotenv_path=env_path)

DICT_PARAMS = {
    '{{path_to_app}}': os.environ.get('PATH_TO_API'),
    '{{app_name}}': os.environ.get('APP_NAME'),
    '{{app-name}}': os.environ.get('APP_NAME').replace('_', '-'),
}
