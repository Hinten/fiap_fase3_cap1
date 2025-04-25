import logging
from time import sleep
import json
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.database.base.database import Database

#https://docs.sqlalchemy.org/en/20/orm/quickstart.html
class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @staticmethod
    def _create_all_tables():
        """
        Cria no banco de dados tabelas das classes que herdam o Model.
        Se a tabela já existir, ela não será criada novamente e nem substituída.
        """
        Model.metadata.create_all(bind=Database.engine)

        logging.info("Tabelas criadas com sucesso!")

    @staticmethod
    def _drop_all_tables():
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

    @classmethod
    def fields(cls) -> list[str]:
        """
        Retorna os campos da classe.
        :return: List[str] - Lista com os nomes dos campos.
        """
        return [column.name for column in inspect(cls).c]

    def to_dict(self):
        """
        Converte a instância do modelo em um dicionário.
        :return: dict - Dicionário com os atributos da instância.
        """
        return {column.name: getattr(self, column.name) for column in inspect(self).mapper.column_attrs}

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria uma instância do modelo a partir de um dicionário.
        :param data: dict - Dicionário com os dados para criar a instância.
        :return: Model - Instância do modelo.
        """
        return cls(**data)

    def to_json(self, indent = 4):
        return  json.dumps(self.to_dict(), indent=indent)

    def copy_with(self, **kwargs):
        """
        Cria uma cópia da instância atual com os atributos modificados.
        :param kwargs: Atributos a serem alterados na cópia.
        :return: Nova instância com os atributos atualizados.
        """
        cls = type(self)
        new_instance = cls(**{**self.__dict__, **kwargs})
        new_instance.id = None  # Evita duplicar a chave primária
        return new_instance
