from utils.utils import Utils, AbstractGenerate


class GenerateTests(AbstractGenerate, Utils):

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params
        self.name_file = dict_params.get('{{hump_main_class}}').lower()

    def start_generate(self):
        """Генерация файла."""
        # Вызываем функцию, где открываем пример файла для теста и
        # считываем его, в заданные поля вставляем нужную информацию.
        initial_tests_file = self.generate_context(
            'src/sample/example_tests.py',
            self.params,
        )

        # Открываем конечный файл для записи. Записываем то, что сформировали.
        with open(
                f'src/done/tests/test_api_{self.name_file}.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write(initial_tests_file)