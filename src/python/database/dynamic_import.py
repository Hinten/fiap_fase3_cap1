import importlib
import inspect
import os
from src.python.database.base.model import Model

def import_models() -> dict[str, type[Model]]:
    """
    Importa dinamicamente todas as classes que herdam de Model
    na pasta src/python/database/models.
    :return: dict - Um dicionário com o nome das classes como chave e as classes como valor.
    """
    models = {}
    models_path = os.path.join(os.path.dirname(__file__), "models")

    for file in os.listdir(models_path):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"src.python.database.models.{file[:-3]}"
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Model) and obj is not Model:
                    models[name] = obj

    return models

def get_model_by_name(name:str) -> type[Model]:
    """
    Retorna uma instância do modelo baseado no nome.
    :param name: Nome do modelo.
    :return: Model - Instância do modelo.
    """
    models = import_models()
    model_class = models.get(name)
    if model_class:
        return model_class
    else:
        raise ValueError(f"Model '{name}' não encontrado.")

if __name__ == "__main__":
    models = import_models()
    for name, model in models.items():
        print(f"Modelo: {name}, Classe: {model}")