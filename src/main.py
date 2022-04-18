import os
import typer

from typing import Optional

from generate_sample import GenerateSample
from helpers.preparation import Preparation


app = typer.Typer()
preparation = Preparation()


os.environ['APP_NAME'] = 'bizone_bug_bounty'
os.environ['PATH_TO_API'] = 'server.apps.bizone_bug_bounty.'


@app.command()
def generate(
        path_to_models: str = typer.Argument(
            ...,
            help='Путь до моделей в проекте, например src/models',
        ),
        rules: Optional[bool] = typer.Option(
            False,
            help='Установите параметр в True, если хотите ' +
                 'сгенерировать файлы с правами доступа',
        ),
        path_to_api: Optional[str] = typer.Option(
            None,
            help='Путь до приложения в проекте, например src.my_app',
        ),
        app_name: Optional[str] = typer.Option(
            None,
            help='Название приложения в проекте, например my_app',
        ),
):
    """Команда для запуска генерации файлов для django проектов.

    При запуске генерации файлов пользователю необходимо указать путь до
    приложения внутри django проекта и название приложения для корректной
    генерации файлов.
    Указать можно как через параметры команды, та ки через переменные окружения.
    Для указания данных через параметры команды сначала проверяется, что
    введены оба параметра или не введено ни одного.

    Если условие соблюдено, то анализируются файлы каталога, данные на который
    передал пользователь, а также формируется общий словарь параметров для
    успешной работы

    В случае, если в файле нет информации о django модели, то анализируется
    следующий файл. На основе сформированного общего словаря параметров
    создаются django файлы.

    :param path_to_models: путь до папки models внутри проекта.
    :param rules: флаг для указания нужно ли создавать файлы и представления с
    учетом прав доступа (используется пакет rules).
    :param path_to_api: путь до приложения внутри django проекта.
    :param app_name: название приложения.
    """
    if all([path_to_api is None, app_name is None]) and not all([path_to_api, app_name]):  # noqa: E501
        path_to_models = os.path.join(os.getcwd(), f'{path_to_models}')
        general_params = preparation.formation_general_params(
            path_to_api, app_name,
        )
        # Считываем все файлы из папки models.
        for filename in os.listdir(path_to_models):
            with open(os.path.join(path_to_models, filename), 'r') as f:
                all_params = preparation.start_analysis(
                    f.read(), general_params, rules,
                )
                # Если удалось получить параметры запускаем генерацию.
                # Если не удалось, ищем дальше в папке файлы с django моделями
                if all_params:
                    generate_sample = GenerateSample(all_params)
                    if rules:
                        generate_sample.start_with_rules()
                    generate_sample.start_without_rules()
                continue
    else:
        typer.echo(
            'Параметр path_to_api и параметр app_name должны быть либо ' +
            'заполнены, либо нет',
        )
        raise typer.Abort()


@app.command()
def clear_file():
    """Команда для очистки всех сгенерированных файлов внутри каталога done."""
    preparation.cleaning_file_directory_done()


@app.command()
def clear_folder():
    """Команда для полного удаления папки done."""
    preparation.remove_directory_done()


if __name__ == "__main__":
    app()
