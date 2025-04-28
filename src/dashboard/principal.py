import streamlit as st
from src.database.base.database import Database
from src.database.teste import Teste

@st.cache_data
def get_exemple_data():

    return Teste.get_from_id(2).as_dataframe()


def principal_view():
    """
    Função para exibir a página principal do aplicativo.
    :return:
    """
    Database.init_from_session(st.session_state.get('engine'), st.session_state.get('sessionLocal'))

    #todo antes de continuar aqui, criar as tables automaticamente na database

    menu_lateral = st.sidebar.selectbox(
        "Selecione uma opção",
        ("Dashboard", "Relatórios", "Configurações"),
    )

    print(menu_lateral)


    st.title("Farm Tech Solutions")
    st.subheader("Dashboard Principal")

    # Exibe informações sobre o aplicativo
    st.write(
        "Este é um aplicativo de exemplo para demonstrar a integração com o banco de dados Oracle."
    )

    # Exibe o DataFrame
    st.write("DataFrame:")
    st.dataframe(get_exemple_data())
