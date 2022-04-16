from helpers.helper import AbstractGenerate, Helper


class GenerateInitSerializers(AbstractGenerate, Helper):
    """Генерация init файла для serializers."""

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params

    def start_generate(self):
        # Открываем конечный файл и проверяем пуст он или нет.
        f = open('done/api/serializers/__init__.py', 'a+', encoding='utf-8')
        f.seek(0)
        init_file_for_serializer = f.read()
        f.close()
        if init_file_for_serializer:
            self.actual_init()
        else:
            self.initial_init()

    def actual_init(self):
        with open(
                'done/api/serializers/__init__.py',
                'a+',
                encoding='utf-8',
        ) as f:
            f.seek(0)
            init = f.read()
            start_position_register = init.find('__all__ = [')
            if start_position_register > 0:
                # self.conftest_factory()[:-3] - удаляем ненужные отступы и
                # закрывающуюся скобку в импорте
                init = (
                    'from {path_to_app}.api.serializer.{main_class} import {main_class_camel}Serializer'.format(
                        path_to_app=self.params.get('{{path_to_app}}'),
                        main_class=self.params.get('{{main_class}}'),
                        main_class_camel=self.params.get('{{MainClass}}'),
                    ) + '\n' +
                    init[:start_position_register] +
                    init[start_position_register:-2] +
                    "    '{main_class}Serializer',".format(
                        main_class=self.params.get('{{MainClass}}'),
                    ) + '\n]\n'
                )

            with open(
                    'done/api/serializers/__init__.py',
                    'w',
                    encoding='utf-8',
            ) as f:
                f.write(init)

    def initial_init(self):
        """Первичное добавление информации в __init__."""
        init_file_for_serializer = self.generate_context(
            'sample/example_init_serializer.py',
            self.params,
        )
        with open(
                'done/api/serializers/__init__.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write(init_file_for_serializer)
