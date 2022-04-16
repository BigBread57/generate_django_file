from helpers.helper import Helper, AbstractGenerate


class GenerateSerializers(AbstractGenerate, Helper):

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params
        self.name_file = dict_params.get('{{main_class}}').lower()

    def start_generate(self):
        """Генерация файла."""
        # Вызываем функцию, где открываем пример файла для сериализатора и
        # считываем его, в заданные поля вставляем нужную информацию.
        initial_serializers_file = self.generate_context(
            'sample/example_serializers.py',
            self.params,
        )

        # Открываем конечный файл для записи. Записываем то, что сформировали.
        with open(
                f'done/api/serializers/{self.name_file}.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write(initial_serializers_file)

        # Открываем конечный файл для записи в конец файла.
        # Формируем поля для serializers.Serializers и вставляем их в файл.
        with open(
                f'done/api/serializers/{self.name_file}.py',
                'a+',
                encoding='utf-8',
        ) as f:
            fields = self.params.get('fields_for_serializers')
            f.write('\n')
            for key, value in fields.items():
                f.write(f'        {key} = serializers.{value}\n')
