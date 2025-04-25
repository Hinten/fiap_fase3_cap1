import logging
from time import sleep

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.database.base.database import Database

#https://docs.sqlalchemy.org/en/20/orm/quickstart.html
class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @staticmethod
    def create_all():
        """
        Cria no banco de dados tabelas das classes que herdam o Model.
        Se a tabela já existir, ela não será criada novamente e nem substituída.
        """
        Model.metadata.create_all(bind=Database.engine)

        logging.info("Tabelas criadas com sucesso!")

    @staticmethod
    def _drop_all():
        """
        Remove todas as tabelas do banco de dados.
        """

        continuar = input("Você tem certeza que deseja remover todas as tabelas? (s/n): ")

        if continuar.lower() != "s":
            logging.info("Operação cancelada.")
            return

        c = 3
        while c > 0:
            print(f"Removendo tabelas em {c} segundos...")
            sleep(1)
            c -= 1

        Model.metadata.drop_all(bind=Database.engine)
        logging.info("Tabelas removidas com sucesso!")