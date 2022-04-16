import ast

from utils import ModelAnalysis
from generations.admin import GenerateAdmin
from generations.conftest import GenerateConftest
from generations.rules import GenerateRules
from generations.serializers import GenerateSerializers
from generations.tests import GenerateTests
from generations.views import GenerateViews
from src.settings.common import DICT_PARAMS


class GenerateSample(object):
    """Основной класс для генерации всех файлов."""

    def __init__(self, tree: ast.Module, *args, **kwargs) -> None:
        """Получаем ast дерево из анализируемой модели и словарь параметров."""
        self.tree = tree
        self.dict_params = DICT_PARAMS

    def start(self):
        """Основной метод для генерации документов.

        1. Получаем нужные данные при обходе ast дерева модели
        2. Формируем словарь из .env переменных и данных полученных при обходе
        3. Вызываем функции, отвечающие за формирование определенных файлов.
        """
        visitor = ModelAnalysis()
        visitor.visit(self.tree)

        self.dict_params.update(visitor.result)

        self.generate_admin()
        self.generate_conftest()
        self.generate_rules()
        self.generate_serializers()
        self.generate_tests()
        self.generate_views()

    def generate_admin(self):
        """Генерация файла для административной панели."""
        admin = GenerateAdmin(self.dict_params)
        admin.start_generate()

    def generate_views(self):
        """Генерация файлов для представлений."""
        admin = GenerateViews(self.dict_params)
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
