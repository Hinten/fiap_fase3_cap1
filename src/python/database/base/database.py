from sqlalchemy import create_engine, MetaData, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from contextlib import contextmanager
import json

from src.settings import DEBUG
DEFAULT_DSN = "oracle.fiap.com.br:1521/ORCL"

# https://www.sqlalchemy.org/
class Database:

    engine:Engine
    sessionLocal:sessionmaker

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
        Database.engine = engine
        Database.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def init_from_session(engine:Engine, sessionLocal:sessionmaker):
        """
        Inicializa a conexão com o banco de dados a partir de um engine e sessionLocal já existentes.
        :param engine: Engine do banco de dados.
        :param sessionLocal: SessionLocal do banco de dados.
        :return:
        """
        Database.engine = engine
        Database.sessionLocal = sessionLocal

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

        Database.init_oracledb(user, password)


    @staticmethod
    @contextmanager
    def get_session() -> Generator[Session, None, None]:
        db = Database.sessionLocal()
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
        engine = Database.engine
        metadata = MetaData()
        metadata.reflect(bind=engine)
        tables = metadata.tables.keys()
        return list(tables)