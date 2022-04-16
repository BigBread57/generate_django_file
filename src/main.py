import ast
import os
import typer

from generate_sample import GenerateSample
from helpers import ModelAnalysis
from settings import BASE_DIR

# app = typer.Typer()


def main(path_to_model: str, rules=False, path_to_api: str = '', app_name: str = ''):
    for filename in os.listdir(BASE_DIR.joinpath(f'{path_to_model}')):

        with open(os.path.join(BASE_DIR.joinpath(f'{path_to_model}'), filename), 'r') as f:
            tree = ast.parse(f.read())
            visitor = ModelAnalysis()
            visitor.visit(tree)

            if visitor.result.get('{{MainClass}}'):
                if path_to_api and app_name:
                    generate_sample = GenerateSample(
                        visitor.result,
                        typer_start={
                            'path_to_api': f'{path_to_api}',
                            'app_name': f'{app_name}',
                        },
                    )
                else:
                    generate_sample = GenerateSample(visitor.result)
                generate_sample.start()
            else:
                continue


if __name__ == "__main__":
    typer.run(main)
