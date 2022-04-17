from helpers.helper import AbstractGenerate, Helper


class GenerateInitSerializers(AbstractGenerate, Helper):
    """Генерация init файла для serializers."""

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params

    def start_generate(self):
        """Проверяем существует ли файл.

        Если нет - создаем. Если да - актуализируем.
        """
        # Открываем конечный файл и проверяем пуст он или нет.
        f = open('done/api/serializers/__init__.py', 'a+', encoding='utf-8')
        f.seek(0)
        initial_file = f.read()
        f.close()
        if initial_file:
            self.actual_init()
        else:
            self.initial_init()

    def actual_init(self):
        """Актуализация __init__ файла для сериализиторов.

        Если анализируются несколько моделей, то в файл необходимо дозаписывать
        следующие данные:
        1) В from/import дозаписать клас сериализатора.
        2) В __all__ добавить название класса сериализатора.
        """
        with open(
            'done/api/serializers/__init__.py', 'a+', encoding='utf-8',
        ) as f:
            f.seek(0)
            initial_ser_file = f.read()
            start_position = initial_ser_file.find('__all__ = [')
            # 1) Вставляем новый импорт на модель сериализатора +
            # 2) Дописываем все что было в первоначальном файле с начала и до
            # __all__
            # 3) initial_ser_file[start_position_register:-2]
            # удаляем пустую строку и ']' в init файле
            # 4) Дописываем новый класс сериализатора.
            if start_position > 0:
                new_initial_ser_file = (
                    'from {path_to_app}.api.serializer.{main_class} import {main_class_camel}Serializer\n'.format(  # noqa: E501
                        path_to_app=self.params.get('{{path_to_app}}'),
                        main_class=self.params.get('{{main_class}}'),
                        main_class_camel=self.params.get('{{MainClass}}'),
                    ) +
                    initial_ser_file[:start_position] +
                    initial_ser_file[start_position:-2] +
                    "    '{main_class}Serializer',\n]\n".format(
                        main_class=self.params.get('{{MainClass}}'),
                    )
                )

        with open(
            'done/api/serializers/__init__.py', 'w', encoding='utf-8',
        ) as f:
            f.write(new_initial_ser_file)

    def initial_init(self):
        """Первичное добавление информации в __init__."""
        initial_file = self.generate_context(
            'sample/example_init_serializer.py',
            self.params,
        )
        with open(
            'done/api/serializers/__init__.py', 'w', encoding='utf-8',
        ) as f:
            f.write(initial_file)
