import logging

from src.python.database.base.oracle import DB
from src.python.database.setup import create_all_tables
import streamlit as st

def setup():

    print(f'Engine {st.session_state.get('engine')}')
    print(f'Session {st.session_state.get('session')}')

    DB.init_from_session(st.session_state.get('engine'), st.session_state.get('session'))

    if not st.session_state.get('init_tables', False):
        logging.info("Criando tabelas...")
        st.info("Criando tabelas...")
        create_all_tables()
        st.session_state['init_tables'] = True
        logging.info("Tabelas criadas com sucesso.")
        st.success("Tabelas criadas com sucesso.")
