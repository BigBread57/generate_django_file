from utils.utils import Utils, AbstractGenerate


class GenerateRules(AbstractGenerate, Utils):

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params
        self.name_file = dict_params.get('{{hump_main_class}}').lower()

    def start_generate(self):
        """Генерация файла."""
        # Вызываем функцию, где открываем пример файла для прав доступа и
        # считываем его, в заданные поля вставляем нужную информацию.
        initial_rules_file = self.generate_context(
            'src/sample/example_rules.py',
            self.params,
        )

        # Открываем конечный файл для записи и вносим в него
        # сформированные данные.
        with open(
                f'src/done/rules/{self.name_file}.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write(initial_rules_file)