import ast
from _ast import (
    Assign,
    Attribute,
    Call,
    Expr,
    Name, Constant,
)

from src.utils.utils import Utils


class ModelAnalysis(ast.NodeVisitor):
    """Проверка файла на наличие класса, удовлетворяющего условиям."""

    def __init__(self, *args, **kwargs) -> None:
        """Установка параметров и переменных для хранения данных."""
        # название родительского класса от которого наследуются модели
        self.parent_class = ['models.Model']
        # аттрибуты модели
        self.fields_django_model = {}
        # аттрибуты сериализатора
        self.fields_for_serializers = {}
        # аттрибуты для тестов
        self.fields_for_conftest = {}
        # указатель на то, что анализируем тело класса модели
        self.is_django_model = False

        self.result = {}
        self.utils = Utils()

    @staticmethod
    def convert_list(params_list: list) -> list:
        """Преобразование переданных параметров в единый список.

        Пример:
        Получаем - param_parent_class_with_packet = ['models.Model'].
        Получаем - parent_class = ['models.Model'].
        Отдаем - result = ['models', 'Model'].
        """
        result = []

        for elem in params_list:
            if elem.find('.'):
                result.extend(elem.split('.'))
            else:
                result.extend(elem)

        return result

    def analysis_body(self, node):
        """Анализ тела класса."""
        for part_body in node.body:

            # осуществляем поиск полей модели или переменных
            if isinstance(part_body, Assign):
                self.visit_Assign(part_body)

            if isinstance(part_body, Expr):
                expr = self.visit_Expr(part_body)
                if expr:
                    self.result.update({'{{docs}}': expr})

        self.is_django_model = False

        self.result.update(
            {
                '{{list_main_fields}}': list(self.fields_django_model.keys()),
                'fields_django_model': self.fields_django_model,
                'fields_for_serializers': self.fields_for_serializers,
                'fields_for_conftest': self.fields_for_conftest,
            }
        )

    def visit_ClassDef(self, node):
        """Поиск необходимых классов."""
        if hasattr(node, 'bases'):  # ищем классы, у которых есть родитель

            self.is_django_model = True
            is_model_attr = False
            is_model_name = False
            for base in node.bases:  # проверяем от чего наследуется класс
                if isinstance(base, Attribute):
                    is_model_attr = self.visit_Attribute(base)
                if isinstance(base, Name):
                    is_model_name = self.visit_Name(base)

            # Анализируем тело родительского класса
            if is_model_attr or is_model_name:
                hump_main_class = self.utils.hump_underline(node.name)
                self.result.update(
                    {
                        '{{main_class}}': node.name,
                        '{{hump_main_class}}': hump_main_class,
                        '{{lower_main_class}}': node.name.lower(),
                        '{{main-class}}': hump_main_class.replace('_', '-')
                    },
                )
                self.analysis_body(node)

        return False

    def visit_Name(self, node):
        """Проверяем узлы, которые имеют класс Name."""
        if self.is_django_model:
            # проверка при поиске родительского класса и полей модели
            if node.id in self.convert_list(self.parent_class):
                return node.id

        ast.NodeVisitor.generic_visit(self, node)
        return False

    def visit_Attribute(self, node):
        """Проверяем узлы, которые имеют класс Attribute."""
        if isinstance(node.value, Name):
            if self.visit_Name(node.value) and self.is_django_model:
                # ищем совпадения с models.Model или типами полей
                if node.attr in [
                    *self.convert_list(self.parent_class),
                    *list(self.utils.fields_django.keys()),
                ]:
                    return node.attr

        ast.NodeVisitor.generic_visit(self, node)
        return False

    def visit_Assign(self, node):
        """Проверяем узлы, которые имеют класс Assign."""
        if self.is_django_model:
            # Проверка для выявления полей модели
            if isinstance(node.value, Call):
                assign_value = self.visit_Call(node.value)

                # Если условия на соответствие полям модели пройдены,
                # то заносим данное поле в хранилище
                if assign_value:
                    if isinstance(node.targets[0], Name):
                        # Сохраняем поля модели
                        self.fields_django_model.update(
                            {
                                node.targets[0].id: assign_value
                            }
                        )
                        # Сохраняем поля для сериализатора
                        self.fields_for_serializers.update(
                            self.utils.field_for_serializers(
                                node.targets[0].id,
                                assign_value,
                            )
                        )
                        # Сохраняем поля для conftest
                        self.fields_for_conftest.update(
                            self.utils.field_for_fake(
                                node.targets[0].id,
                                assign_value,
                            )
                        )

        ast.NodeVisitor.generic_visit(self, node)
        return False

    def visit_Call(self, node):
        """Проверяем узлы, которые имеют класс Call."""
        if self.is_django_model:
            # проверка для выявления полей модели
            if isinstance(node.func, Attribute):
                return self.visit_Attribute(node.func)

        ast.NodeVisitor.generic_visit(self, node)
        return False

    def visit_Expr(self, node):
        """Проверяем узлы, которые имеют класс Expr."""
        if self.is_django_model:
            if isinstance(node.value, Constant):
                return self.visit_Constant(node.value)
            else:
                ast.NodeVisitor.generic_visit(self, node)
        return False

    def visit_Constant(self, node):
        """Проверяем узлы, которые имеют класс Constant."""
        if self.is_django_model:
            return node.value

        ast.NodeVisitor.generic_visit(self, node)
        return False