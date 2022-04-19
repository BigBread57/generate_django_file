import ast
import glob
import os
import shutil
from typing import Optional

from helpers import ModelAnalysis
from helpers.helper import Helper

helpers = Helper()


class Preparation(object):

    @classmethod
    def formation_general_params(
        cls,
        path_to_api: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> dict:
        """Формируем общие параметры для генерации django файлов.

        :param path_to_api: путь до приложения внутри django проекта.
        :param app_name: название приложения.
        :return: словарь общих параметров.
        """
        if not path_to_api and not app_name:
            path_to_api = os.environ.get('PATH_TO_API')
            app_name = os.environ.get('APP_NAME')

        return {
            '{{path_to_app}}': path_to_api,
            '{{app_name}}': app_name,
            '{{AppName}}': helpers.str_camel(app_name),
            '{{app-name}}': app_name.replace('_', '-'),
        }

    @classmethod
    def start_analysis(
            cls,
            text_file: str,
            general_params: dict,
            rules: bool,
    ) -> Optional[dict]:
        """Запуск анализа файла с моделью.

        :param text_file: текст файла, в котором описана django модель.
        :param general_params: содержит словарь общих параметров.
        :param rules: флаг, указывающий на использование rules при генерации.
        :return: возвращает сформированный словарь всех параметров.
        """
        all_params_dict = {}
        # Осуществляем анализ файла через модуль ast
        tree = ast.parse(text_file)
        visitor = ModelAnalysis()
        visitor.visit(tree)
        # Проверяем удался ли анализ файла. Если удался возвращаем параметры.
        # В случае если модель не обнаружена возвращаем None.
        if visitor.result.get('{{MainClass}}'):
            all_params_dict.update(
                **general_params,
                **visitor.result
            )
            # Формируем структуру папки со сгенерированными файлами.
            cls.folder_structure(rules)

            return all_params_dict
        return None

    @classmethod
    def folder_structure(cls, rules: bool = False):
        """Создание структуры папок.

        :param rules: флаг, указывающие будут ли использоваться rules.
        """
        if not os.path.exists(os.path.join(os.getcwd(), 'done')):
            os.mkdir(os.path.join(os.getcwd(), 'done'))
            os.mkdir(os.path.join(os.getcwd(), 'done/api'))
            os.mkdir(os.path.join(os.getcwd(), 'done/api/views'))
            os.mkdir(os.path.join(os.getcwd(), 'done/api/serializers'))
            os.mkdir(os.path.join(os.getcwd(), 'done/tests'))
            os.mkdir(os.path.join(os.getcwd(), 'done/tests/test_app'))
            if rules:
                os.mkdir(os.path.join(os.getcwd(), 'done/rules'))

    @classmethod
    def cleaning_file_directory_done(cls):
        """Очищаем все в папке done от старых файлов."""
        directory_done = os.path.join(os.getcwd(), 'done')
        directories = (
            f'{directory_done}/rules/*',
            f'{directory_done}/api/serializers/*',
            f'{directory_done}/tests/test_app/*',
            f'{directory_done}/api/views/*',
        )
        for directory in directories:
            files = glob.glob(directory)
            for f in files:
                os.remove(f)
        with open(
            f'{directory_done}/admin.py', 'w', encoding='utf-8',
        ) as f:
            f.write('')
        with open(
            f'{directory_done}/tests/conftest.py', 'w', encoding='utf-8',
        ) as f:
            f.write('')
        with open(
            f'{directory_done}/api/routers.py', 'w', encoding='utf-8',
        ) as f:
            f.write('')

    @classmethod
    def remove_directory_done(cls):
        """Удаляем папку done."""
        shutil.rmtree(os.path.join(os.getcwd(), 'done'))
