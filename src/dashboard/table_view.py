from enum import Enum

import streamlit as st

from src.dashboard.edit_view import EditView
from src.python.database.base.model import Model


#view que pega os dados do banco de dados e mostra em uma tabela, com a opção de criar um novo ou editar

class TableState(Enum):
    """
    Enum para gerenciar o estado da tabela.
    """
    VIEW = 1
    EDIT = 2

class TableView:

    def __init__(self, model: type[Model]):
        self.model = model

    def get_view(self):
        """
        Função para exibir uma tabela com os dados do banco de dados.
        :return:
        """
        if st.session_state.get(Model.display_name(), TableState.VIEW).value == TableState.VIEW.value:
            self.table_view()
        elif st.session_state.get(Model.display_name(), TableState.VIEW).value == TableState.EDIT.value:
            self.edit_view()
        else:
            raise ValueError(f"Estado inválido para a tabela {st.session_state.get(Model.display_name())}.")

    def table_view(self):

        st.title(self.model.display_name_plural())

        # criar colunas
        col1, col2 = st.columns([3, 1])  # Tabela (col1) maior, botão "Novo" (col2) menor

        with col2:
            # Criar um novo registro
            if st.button("Novo"):
                st.session_state[Model.display_name()] = TableState.EDIT
                st.rerun()

        with col1:
            # Mostrar tabela
            data = self.model.all()
            if len(data) > 0:
                for index, row in data.iterrows():
                    if st.button(f"Editar {row['id']}"):  # Botão para cada item
                        st.session_state['edit_id'] = row['id']
                        print(row['id'])  # Redirecionar para edição
            else:
                st.write("Nenhum dado disponível.")

    def edit_view(self, model_id: int|None = None):
        """
        Função para exibir o formulário de edição.
        :param model_id:
        :return:
        """
        edit_instance = EditView(self.model, model_id, )
        return edit_instance.get_cadastro_view()