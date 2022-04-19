import argparse

from main import options


class Application:
    """Абстрагируем приложение в класс."""

    def __init__(self, program="gdf"):
        """Инициализировать наше приложение.

        :param str program:
             Имя программы/приложения, которое мы выполняем.
        """

        self.program = program
        # Предварительный синтаксический анализатор аргументов для обработки
        # параметров, необходимых для получения и анализа
        # конфигурационного файла.
        self.prelim_arg_parser = argparse.ArgumentParser(add_help=False)
        options.register_preliminary_options(self.prelim_arg_parser)
        # Экземпляр :class:`flake8.options.manager.OptionManager`, используемый
        # для разбора и обработки параметров и аргументов, переданных
        # пользователем

    def exit(self) -> None:
        """Handle finalization and exiting the program.

        This should be the last thing called on the application instance. It
        will check certain options and exit appropriately.
        """
        print('Успех')
