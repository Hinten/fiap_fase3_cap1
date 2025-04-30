import streamlit as st

from src.dashboard.principal import principal
from src.dashboard.table_view import TableView
from src.python.database.dynamic_import import import_models

def get_rotas() -> dict:
    """
    Função para importar dinamicamente os módulos e retornar um dicionário de rotas.
    :return: dict - Um dicionário com o nome das rotas como chave e as funções como valor.
    """
    rotas = {
        "Principal": principal,
    }

    # Importa todos os modelos
    models = import_models()

    # Adiciona cada modelo ao dicionário de rotas
    items = list(models.items())
    items.sort(key=lambda x: x[1].display_name())
    for model_name, model in items:
        rotas[model.display_name()] = TableView(model).get_view

    return rotas

rotas = get_rotas()

#todo arrumar isso daqui
def nav():
    """
    Função para exibir a página principal do aplicativo.
    :return:
    """
    menu_lateral = st.sidebar.selectbox(
        "Selecione uma opção",
        rotas.keys(),
    )

    print(menu_lateral)

    if menu_lateral in rotas:
        rotas[menu_lateral]()