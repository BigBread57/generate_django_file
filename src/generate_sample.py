import ast

from helpers import ModelAnalysis
from generations.admin import GenerateAdmin
from generations.conftest import GenerateConftest
from generations.rules import GenerateRules
from generations.serializers import GenerateSerializers
from generations.tests import GenerateTests
from generations.views import GenerateViews
from generations.views_this_rules import GenerateViewsThisRules
from generations.init_serializers import GenerateInitSerializers
from generations.init_views import GenerateInitViews
from generations.routers import GenerateRouters
from settings.common import formation_dict_params


class GenerateSample(object):
    """Основной класс для генерации всех файлов."""

    def __init__(self, visitor_result: dict, typer_start=None, *args, **kwargs) -> None:
        """Получаем ast дерево из анализируемой модели и словарь параметров."""
        self.dict_params = formation_dict_params(typer_start)
        self.visitor_result = visitor_result

    def start(self):
        """Основной метод для генерации документов.

        1. Получаем нужные данные при обходе ast дерева модели
        2. Формируем словарь из .env переменных и данных полученных при обходе
        3. Вызываем функции, отвечающие за формирование определенных файлов.
        """
        self.dict_params.update(self.visitor_result)
        self.generate_admin()
        self.generate_rules()
        self.generate_serializers()
        self.generate_tests()
        self.generate_conftest()
        self.generate_views()
        self.generate_init_views()
        self.generate_init_serializers()
        self.generate_routers()
        # self.generate_views_this_rules()

    def generate_admin(self):
        """Генерация файла для административной панели."""
        admin = GenerateAdmin(self.dict_params)
        admin.start_generate()

    def generate_views(self):
        """Генерация файлов для представлений."""
        admin = GenerateViews(self.dict_params)
        admin.start_generate()

    def generate_views_this_rules(self):
        """Генерация файлов для представлений с правами."""
        admin = GenerateViewsThisRules(self.dict_params)
        admin.start_generate()

    def generate_serializers(self):
        """Генерация файлов для сериализаторов."""
        admin = GenerateSerializers(self.dict_params)
        admin.start_generate()

    def generate_rules(self):
        """Генерация файлов для прав доступа пакета rules."""
        admin = GenerateRules(self.dict_params)
        admin.start_generate()

    def generate_tests(self):
        """Генерация файлов для тестов."""
        admin = GenerateTests(self.dict_params)
        admin.start_generate()

    def generate_conftest(self):
        """Генерация файла для настроек тестов - файла conftest."""
        admin = GenerateConftest(self.dict_params)
        admin.start_generate()

    def generate_init_views(self):
        """Генерация init файла для представлений."""
        admin = GenerateInitViews(self.dict_params)
        admin.start_generate()

    def generate_init_serializers(self):
        """Генерация init файла для сериализаторов."""
        admin = GenerateInitSerializers(self.dict_params)
        admin.start_generate()

    def generate_routers(self):
        """Генерация файла для маршрутизатора."""
        admin = GenerateRouters(self.dict_params)
        admin.start_generate()
