import argparse


def register_preliminary_options(parser: argparse.ArgumentParser) -> None:
    """"""
    add_argument = parser.add_argument

    add_argument(
        '-g',
        '--rulles',
        default=False,
        action='store_true',
        help='Установите параметр в True, если хотите сгенерировать файлы ' +
             'с правами доступа',
    )

    # add_argument(
    #     '-r',
    #     '--rulles',
    #     action='store_true',
    #     help='Установите параметр в True, если хотите сгенерировать файлы ' +
    #          'с правами доступа',
    # )
    #
    # add_argument(
    #     '-p',
    #     '--path-to-api',
    #     default=None,
    #     help='Путь до приложения в проекте, например gdf.my_app',
    # )
    # add_argument(
    #     '-a',
    #     '--app-name',
    #     default=None,
    #     help='Название приложения в проекте, например my_app',
    # )

