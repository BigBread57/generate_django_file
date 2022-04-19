from helpers.helper import AbstractGenerate, Helper


class GenerateViewsThisRules(AbstractGenerate, Helper):
    """Генерация представления с правилами доступа."""

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params
        self.name_file = dict_params.get('{{main_class}}').lower()

    def start_generate(self):
        """Генерация файла."""
        # Вызываем функцию, где открываем пример файла для представлений и
        # считываем его, в заданные поля вставляем нужную информацию.
        initial_file = self.generate_context(
            'sample/example_views_this_rules.py',
            self.params,
        )

        # Открываем конечный файл для записи. Записываем то, что сформировали.
        with open(
            f'done/api/views/{self.name_file}.py', 'w', encoding='utf-8',
        ) as f:
            f.write(initial_file)
