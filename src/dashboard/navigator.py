import streamlit as st

from src.dashboard.principal import principal
from src.dashboard.table_view import TableView
from src.database.fazenda import Fazenda

rotas = {
    "Principal": principal,
    "Fazenda": TableView(Fazenda).get_view,
}

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