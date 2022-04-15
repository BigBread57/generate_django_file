from utils.utils import Utils, AbstractGenerate


class GenerateConftest(AbstractGenerate, Utils):

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params

    def start_generate(self):
        # Открываем конечный файл и проверяем пусто он или нет.
        f = open('src/done/conftest.py', 'r', encoding='utf-8')
        initial_conftest_file = f.read()
        f.close()
        if initial_conftest_file:
            self.actual_conftest()
        else:
            self.initial_conftest()

    def formatted_file(self, text_file: str) -> str:
        """Подстановка в шаблон необходимых данных."""
        for key, value in self.params.items():
            # В словаре много ключей, ищем нужные по совпадению.
            if text_file.find(key) > 0:
                text_file = text_file.replace(
                    key,
                    str(value),
                )
        return text_file

    def actual_conftest(self):
        with open(
                f'src/done/conftest.py',
                'a+',
                encoding='utf-8',
        ) as f:
            f.seek(0)
            conftest = f.read()
            start_position_register = conftest.find('register(')
            end_position_register = conftest.find('@pytest.fixture')
            if start_position_register > 0:
                register = conftest[start_position_register:end_position_register]

            # self.conftest_factory()[:-2] - удаляем ненужные отступы
            conftest = (
                conftest[:start_position_register] +
                self.conftest_factory()[:-2] +
                register +
                conftest[end_position_register:] + '\n\n' +
                self.conftest_fixture()
            )

            with open(
                    f'src/done/conftest.py',
                    'w',
                    encoding='utf-8',
            ) as f:
                f.write(conftest)

    def initial_conftest(self):
        """Первичное добавление импортов в файл, фабрики и фикстур."""
        with open(
                f'src/done/conftest.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write(
                self.conftest_import() +
                self.conftest_factory() +
                self.conftest_fixture(),
            )

    def conftest_factory(self):
        """Возвращает часть conftest файла, отвечающего за фабрики."""
        with open(
                f'src/sample/conftest/conftest_factory.py',
                'r',
                encoding='utf-8',
        ) as f:
            conftest_factory = f.read()
            hump_main_class = self.params.get('{{hump_main_class}}')
            main_class = self.params.get('{{main_class}}')
            factory_fields = ''
            fields_for_conftest = self.params.get('fields_for_conftest')

            for key, value in fields_for_conftest.items():
                if value == '__change_me__':
                    factory_field = f'    {key} = factory.SubFactory({value})\n'
                else:
                    factory_field = (
                            f'    {key} = factory.LazyAttribute(' +
                            f'lambda {hump_main_class}: {value})\n'
                    )
                factory_fields += factory_field
            factory_fields += '\n\n' + f'register({main_class})\n' + '\n\n'

            return self.formatted_file(conftest_factory) + factory_fields
        
    def conftest_fixture(self):
        """Возвращает часть conftest файла, отвечающего за фикстуры."""
        with open(
                f'src/sample/conftest/conftest_fixture.py',
                'r',
                encoding='utf-8',
        ) as f:
            conftest_fixture = f.read()
            # Получаем из словаря название класса.
            hump_main_class = self.params.get('{{hump_main_class}}')
            # формируем первую строку для format: return {'id': main.id,
            fixture_fields = (
                    '        return {\n' +
                    "            'id': {main_class}.pk,\n".format(
                        main_class=hump_main_class,
                    )
            )
            # Получаем из словаря поля и тип для faker.
            fields_for_conftest = self.params.get('fields_for_conftest')
            # Формирует каждую строку по виду 'id': main.id
            for key, value in fields_for_conftest.items():
                fixture_field = (
                    f"            '{key}': {hump_main_class}.{key},\n"
                )
                fixture_fields += fixture_field

            fixture_fields += (
                    '        }' +
                    '\n    return _{main_class}_format\n'.format(
                        main_class=hump_main_class
                    )
            )

            return self.formatted_file(conftest_fixture) + fixture_fields
            
    def conftest_import(self):
        """Возвращает часть conftest файла, отвечающего за импорты."""
        with open(
                f'src/sample/conftest/conftest_import.py',
                'r',
                encoding='utf-8',
        ) as f:
            
            conftest_import = f.read()
            return self.formatted_file(conftest_import)
