import logging

from src.database.base.database import Database
from src.database.base.utils import create_all_tables
import streamlit as st

def setup():

    Database.init_from_session(st.session_state.get('engine'), st.session_state.get('sessionLocal'))

    if not st.session_state.get('init_tables', False):
        logging.info("Criando tabelas...")
        st.info("Criando tabelas...")
        create_all_tables()
        st.session_state['init_tables'] = True
        logging.info("Tabelas criadas com sucesso.")
        st.success("Tabelas criadas com sucesso.")
