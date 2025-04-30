from contextlib import contextmanager
from sqlalchemy import create_engine, Engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from dotenv import load_dotenv
import os
from typing import Generator
import json

from src.python.settings import DEBUG

DEFAULT_DSN = "oracle.fiap.com.br:1521/ORCL"


class DB:
    engine:Engine
    session:sessionmaker

    @staticmethod
    def init_from_env():
        '''
        Inicializa a conexão com o banco de dados Oracle a partir de variáveis de ambiente.
        Não esquecer de criar o arquivo .env com as variáveis de ambiente.
        '''

        load_dotenv()

        DB_USER = os.getenv("ORACLE_USER")
        DB_PASSWORD = os.getenv("ORACLE_PASSWORD")
        DB_HOST = os.getenv("ORACLE_HOST")
        DB_PORT = os.getenv("ORACLE_PORT")
        DB_SERVICE = os.getenv("ORACLE_SERVICE")

        DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SERVICE}"

        DB.engine = create_engine(DATABASE_URL, echo=False)

        DB.session = sessionmaker(autocommit=False, autoflush=False, bind=DB.engine)


    @staticmethod
    def init_oracledb(user:str, password:str, dsn:str=DEFAULT_DSN):
        '''
        Inicializa a conexão com o banco de dados Oracle.
        :param user: Nome do usuário do banco de dados.
        :param password: Senha do usuário do banco de dados.
        :param dsn: DSN do banco de dados.
        :return:
        '''

        # Cria o engine de conexão
        engine = create_engine(f"oracle+oracledb://{user}:{password}@{dsn}", echo=DEBUG)

        # Testa a conexão
        with engine.connect() as _:
            print("Conexão bem-sucedida ao banco de dados Oracle!")
        DB.engine = engine
        DB.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def init_from_session(engine:Engine, session:sessionmaker):
        """
        Inicializa a conexão com o banco de dados a partir de um engine e sessionLocal já existentes.
        :param engine: Engine do banco de dados.
        :param session: SessionLocal do banco de dados.
        :return:
        """
        DB.engine = engine
        DB.session = session

    @staticmethod
    def init_oracledb_from_file(path:str = r"E:\PythonProject\fiap_fase3_cap1\login.json"):

        """
        Inicializa a conexão com o banco de dados Oracle a partir de um arquivo JSON.
        :param path: Caminho do arquivo JSON com as credenciais do banco de dados.
        :return:
        """
        with open(path, "r") as file:
            data = json.load(file)
            user = data["user"]
            password = data["password"]

        DB.init_oracledb(user, password)


    @staticmethod
    @contextmanager
    def get_session() -> Generator[Session, None, None]:
        db = DB.session()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def list_tables() -> list[str]:
        """
        Lista as tabelas do banco de dados.
        :return: List[str] - Lista com os nomes das tabelas.
        """
        engine = DB.engine
        metadata = MetaData()
        metadata.reflect(bind=engine)
        tables = metadata.tables.keys()
        return list(tables)



if __name__ == "__main__":

    db = DB()

