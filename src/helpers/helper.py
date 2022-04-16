import glob
import os
import re
from abc import abstractmethod
from pathlib import Path

from settings import config


def add_change_me(field, test=False) -> str:
    """
    Добавляет __change_me__, если передано None.

    :param field: поле для сериализатора или теста
    :param test: флаг указывающий, что поле для генерации тестов
    :return: значение поле: если None, добавляем с __change_me__, иначе
    переданное значение поля
    """
    if str(field).strip().lower() == 'none':
        if test:
            return '__change_me__'
        else:
            return 'None(__change_me__)'
    return field


def generate_field_for_django() -> dict:
    """
    Создает словарь с полями для сериализаторов и тестов.

    :return: словарь с полями.
    """
    fields_django = {
        'AutoField': ('IntegerField()', 'fake.pyint()'),
        'BigIntegerField': ('IntegerField()', 'fake.pyint()'),
        'BooleanField': ('BooleanField()', 'fake.pybool()'),
        'CharField': ('CharField()', 'fake.paragraph()'),
        'CommaSeparatedIntegerField': ('CharField()', 'fake.paragraph()'),
        'DateField': ('DateField()', 'fake.date_between()'),
        'DateTimeField': ('DateTimeField()', 'fake.date_time_this_month()'),
        'DecimalField': ('DecimalField()', 'fake.pydecimal()'),
        'DurationField': ('DurationField()', 'fake.time_delta()'),
        'EmailField': ('EmailField()', 'fake.ascii_free_email()'),
        'Field': ('ModelField()', 'fake.__change_me__()'),
        'FileField': ('FileField()', 'fake.file_name()'),
        'FloatField': ('FloatField()', 'fake.pyfloat()'),
        'ImageField': ('ImageField()', 'fake.file_name()'),
        'IntegerField': ('IntegerField()', 'fake.pyint()'),
        'NullBooleanField': ('BooleanField()', 'fake.pybool()'),
        'PositiveIntegerField': ('IntegerField()', 'fake.pyint()'),
        'PositiveSmallIntegerField': ('IntegerField()', 'fake.pyint()'),
        'SlugField': ('SlugField()', 'fake.slug()'),
        'SmallIntegerField': ('IntegerField()', 'fake.pyint()'),
        'TextField': ('CharField()', 'fake.paragraph()'),
        'TimeField': ('TimeField()', 'fake.time()'),
        'URLField': ('URLField()', 'fake.url()'),
        'UUIDField': ('UUIDField()', 'fake.uuid4()'),
        'GenericIPAddressField': ('IPAddressField()', 'fake.ipv4()'),
        'FilePathField': ('FilePathField()', 'fake.file_path(depth=3)'),
        'BigAutoField': ('None(__change_me__)', 'fake.pyint()'),
        'BinaryField': ('None(__change_me__)', 'fake.binary(length=16)'),
        'ForeignKey': ('None(__change_me__)', '__change_me__'),
        'ManyToManyField': ('None(__change_me__)', '__change_me__'),
        'OneToOneField': ('None(__change_me__)', '__change_me__'),
        'FieldFile': ('None(__change_me__)', 'fake.file_name()'),
    }
    # Если добавлены поля из сторонних библиотек, то добавляем их в наш словарь
    custom_fields = config('FIELD_CLASS_MODEL', default=None)
    if custom_fields:
        if custom_fields.endswith(';'):
            custom_fields = custom_fields[:-1]

        list_fields = custom_fields.split(';')
        for element in list_fields:
            list_elements = element.strip().split(',')
            fields_django.update(
                {
                    list_elements[0]:
                        (
                            add_change_me(list_elements[1]),
                            add_change_me(list_elements[2], test=True)
                        ),
                },
            )
    return fields_django


class Helper(object):
    """Класс содержит функции, которые используются несколько раз."""

    # Ключ данной переменной это тип поля для моделей.
    # Первый элемент кортежа - тип поля в сериализаторе
    # Второй элемент кортежа - тип поля для тестов в библиотеке faker
    fields_django = generate_field_for_django()


    @classmethod
    def remove_import(cls, text: str) -> str:
        """Удаляем импорты.

        :param text: текст кода для админки(взят из example_admin) с импортами.
        :return: текст кода для админки без импортов, то есть только класс.
        """
        list_imports = text.split('\n')[0:3]
        str_imports = '\n'.join(list_imports)
        return text.replace(str_imports, '')

    @classmethod
    def cleaning_directory_done(cls):
        """Очищаем все в папке done от старых файлов."""
        directory_before_done = Path(__file__).parent.parent.joinpath('done')
        directories = (
            f'{directory_before_done}/rules/*',
            f'{directory_before_done}/api/serializers/*',
            f'{directory_before_done}/tests/test_app/*',
            f'{directory_before_done}/api/views/*',
        )
        for directory in directories:
            files = glob.glob(directory)
            for f in files:
                os.remove(f)
        with open(
                f'{directory_before_done}/admin.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write('')
        with open(
                f'{directory_before_done}/tests/conftest.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write('')
        with open(
                f'{directory_before_done}/api/routers.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write('')

    @classmethod
    def str_hump_underline(cls, str_camel) -> str:
        """Строка регистра Camel преобразуется в подчеркивание.

        :param str_camel: строка в верблюжьем стиле.
        :return: строка с подчеркиванием.
        """
        # Соответствие позиции разграничения строчных и прописных букв
        pattern = re.compile(r'([a-z]|\d)([A-Z])')
        # Второй параметр здесь использует обратную ссылку на обычную группу
        return re.sub(pattern, r'\1_\2', str_camel).lower()

    @classmethod
    def str_camel(cls, str_underline) -> str:
        """Строка с подчеркиваниями преобразуется в верблюжий стиль.

        :param str_underline: строка с подчеркиваниями.
        :return: строка в верблюжьем стиле.
        """
        str_camel = ''
        list_elements = str_underline.split('_')
        for element in list_elements:
            str_camel += element.title()
        return str_camel

    def field_for_serializers(self, name_field: str, type_field: str) -> dict:
        """Преобразование полей модели для сериализатора.

        :param name_field: название поля.
        :param type_field: тип поля для сериализтора.
        :return: словарь {название поля: тип поля}.
        """
        return {
            name_field: self.fields_django.get(type_field)[0]
        }

    def field_for_fake(self, name_field: str, type_field: str) -> dict:
        """Преобразование полей модели для тестов и библиотеки faker.

        :param name_field: название поля.
        :param type_field: тип поля для тестов из библиотеки faker.
        :return: словарь {название поля: тип поля}.
        """
        return {
            name_field: self.fields_django.get(type_field)[1]
        }

    def generate_context(self, path: str, params: dict) -> str:
        """Генерируем из шаблона нужный документ.

        :param path: путь до шаблона файла.
        :param params: словарь параметров откуда берется информация для вставки.
        :return: сформированный файл с данными.
        """
        with open(path, 'r', encoding='utf-8') as f:
            initial_file = f.read()
            for key, value in params.items():
                # В словаре много ключей, ищем нужные по совпадению.
                if initial_file.find(key) > 0:
                    initial_file = initial_file.replace(
                        key,
                        str(value),
                    )
                if params.get('{{docs}}') is None:
                    initial_file = initial_file.replace(
                        '{{docs}}',
                        '',
                    )
        return initial_file


class AbstractGenerate(object):
    """Абстрактный класс, для классов генерирующих файлы"""

    @abstractmethod
    def start_generate(self) -> None:
        """Генерирует файл с нужными данными или содержит порядок действия."""

