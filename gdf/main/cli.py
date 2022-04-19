"""Реализация gdf из командной строки."""
import sys
from typing import List
from typing import Optional

from gdf.main import application


def main(argv: Optional[List[str]] = None) -> None:
    """Выполнить основное приложение.

    Это обрабатывает создание экземпляра :class:`Application`, запускает его,
    а затем выходит из приложения.

    :param list argv: Аргументы, которые необходимо передать для разбора.
    """
    if argv is None:
        argv = sys.argv[1:]

    app = application.Application()
    app.run(argv)
    app.exit()
