from helpers.helper import Helper, AbstractGenerate


class GenerateRules(AbstractGenerate, Helper):
    """Генерация файлов для прав доступа пакета django-rules."""

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params
        self.name_file = dict_params.get('{{main_class}}').lower()

    def start_generate(self):
        """Генерация файла."""
        # Вызываем функцию, где открываем пример файла для прав доступа и
        # считываем его, в заданные поля вставляем нужную информацию.
        initial_file = self.generate_context(
            'sample/example_rules.py',
            self.params,
        )

        # Открываем конечный файл для записи и вносим в него
        # сформированные данные.
        with open(
            f'done/rules/{self.name_file}.py', 'w', encoding='utf-8',
        ) as f:
            f.write(initial_file)
