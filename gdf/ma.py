import argparse

import os
from generate_sample import GenerateSample
from helpers import Preparation

preparation = Preparation()


os.environ['APP_NAME'] = 'bizone_bug_bounty'
os.environ['PATH_TO_API'] = 'server.apps.bizone_bug_bounty'

parser = argparse.ArgumentParser(prog='gdf', description='List the content of a folder')

# Add the arguments
parser.add_argument('generate', type=str,)
parser.add_argument('-pm', '--path-to-models', type=str)
parser.add_argument('-pa', '--path-to-api')
parser.add_argument('-a', '--app-name')
parser.add_argument('-r', '--rules', default=False, action='store_true')

args = parser.parse_args()
print(args)
if args.generate:
    # if all([path_to_api is None, app_name is None]) and not all([path_to_api, app_name]):  # noqa: E501
    path_to_models = os.path.join(os.getcwd(), f'{args.path_to_models}')
    general_params = preparation.formation_general_params(
        args.path_to_api, args.app_name,
    )
    # Считываем все файлы из папки models.
    for filename in os.listdir(path_to_models):
        with open(os.path.join(path_to_models, filename), 'r') as f:
            all_params = preparation.start_analysis(
                f.read(), general_params, args.rules,
            )
            # Если удалось получить параметры запускаем генерацию.
            # Если не удалось, ищем дальше в папке файлы с django моделями
            if all_params:
                generate_sample = GenerateSample(all_params)
                if args.rules:
                    generate_sample.start_with_rules()
                generate_sample.start_without_rules()
            continue
