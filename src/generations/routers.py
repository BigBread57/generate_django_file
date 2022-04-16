from helpers.helper import Helper, AbstractGenerate


class GenerateRouters(AbstractGenerate, Helper):

    def __init__(self, dict_params: dict, *args, **kwargs) -> None:
        """Инициализируем переменные (параметры для вставки, название файла)."""
        self.params = dict_params

    def start_generate(self):
        # Открываем конечный файл и проверяем пуст он или нет.
        f = open('done/api/routers.py', 'r', encoding='utf-8')
        initial_router_file = f.read()
        f.close()
        if initial_router_file:
            self.actual_router()
        else:
            self.initial_router()

    def actual_router(self):
        with open(
                'done/api/routers.py',
                'a+',
                encoding='utf-8',
        ) as f:
            f.seek(0)
            routers = f.read()
            str_start_find = 'from {path_to_app}.api.views import ('.format(
                path_to_app=self.params.get('{{path_to_app}}'),
            )
            str_end_find = 'class {app_name}APIRootView(APIRootView):'.format(
                app_name=self.params.get('{{AppName}}'),
            )
            start_position_register = routers.find(str_start_find)
            end_position_register = routers.find(str_end_find)
            if start_position_register > 0:
                from_import = routers[start_position_register:end_position_register]
                # self.conftest_factory()[:-3] - удаляем ненужные отступы и
                # закрывающуюся скобку в импорте
                routers = (
                        routers[:start_position_register] +
                        from_import[:-4] +
                        '    {main_class}ViewSet,'.format(main_class=self.params.get('{{MainClass}}')) + '\n)\n\n\n' +
                        routers[end_position_register:-1] + '\n' +
                        "router.register('{app_name}', {main_class}ViewSet, '{app_name}')".format(
                            app_name=self.params.get('{{app-name}}'),
                            main_class=self.params.get('{{MainClass}}'),
                        ) + '\n'
                )

            with open(
                    'done/api/routers.py',
                    'w',
                    encoding='utf-8',
            ) as f:
                f.write(routers)

    def initial_router(self):
        """Первичное добавление информации в routers"""
        initial_routers_file = self.generate_context(
            'sample/example_routers.py',
            self.params,
        )
        with open(
                'done/api/routers.py',
                'w',
                encoding='utf-8',
        ) as f:
            f.write(initial_routers_file)

