from src.python.database.base.model import Model
import streamlit as st



class EditView:
    """
    EditView is a class that provides functionality to edit a dashboard.
    It includes methods to load the dashboard, edit its properties, and save changes.
    """

    def __init__(self, model: type[Model], model_id: int|None=None, instance: Model|None=None):
        self.model = model
        self.model_id = model_id
        self.instance = instance

        if model_id is not None and instance is None:
            self.instance = model.get_from_id(model_id)
        elif instance is not None:
            self.instance = instance
            self.id = instance.id

    def get_cadastro_view(self):
        """
        Função para exibir o formulário de cadastro.
        :return:
        """
        st.title(self.model.display_name())

        # criar colunas
        col1, col2 = st.columns([3, 1])

        with col2:
            # Criar um novo registro
            if st.button("Salvar"):
                self.save()

        with col1:
            self.get_fields()

    def save(self):
        raise NotImplementedError("Método save não implementado.")

    def get_fields(self):
        """
        Função para exibir os campos do formulário.
        :return:
        """
        for field in self.model.field_names():
            if field == 'id':
                continue

            value = None if self.instance is None else getattr(self.instance, field)
            new_value = st.text_input(field, value)

            if new_value != value:
                setattr(self.instance, field, new_value)