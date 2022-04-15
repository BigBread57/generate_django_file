from utils.utils import AbstractGenerate, Utils


class GenerateViews(AbstractGenerate, Utils):
    """Генерация представления"""

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params
        self.name_file = dict_params.get('{{hump_main_class}}').lower()

    def start_generate(self):
        """Генерация файла."""
        # Вызываем функцию, где открываем пример файла для представлений и
        # считываем его, в заданные поля вставляем нужную информацию.
        initial_views_file = self.generate_context(
            'src/sample/example_views.py',
            self.params,
        )

        # Открываем конечный файл для записи. Записываем то, что сформировали.
        with open(
                f'src/done/views/{self.name_file}.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write(initial_views_file)
