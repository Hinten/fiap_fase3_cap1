import json
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
from abc import abstractmethod
from src.database.base.database import Database
import pandas as pd


#https://docs.sqlalchemy.org/en/20/orm/quickstart.html
class Model(DeclarativeBase):

    #Não funciona na oracledb, infelizmente
    # id: Mapped[int] = mapped_column(
    #     Sequence(f"{__tablename__}_seq_id"),
    #     primary_key=True,
    #     autoincrement=True,
    #     nullable=False
    # )

    @property
    @abstractmethod
    def id(self):
        """
        Este atributo deve ser definido na classe herdeira.

        exemplo:
        id: Mapped[int] = mapped_column(
             Sequence(f"{__tablename__}_seq_id"),
             primary_key=True,
             autoincrement=True,
             nullable=False
         )
        """
        raise NotImplementedError("O atributo 'id' deve ser definido na classe herdeira.")

    def field_names(cls) -> list[str]:
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

    def save(self) -> 'Model':
        """
        Cria ou atualiza a instância no banco de dados.
        :return: Model - Instância salva.
        """
        with Database.get_session() as session:
            session.add(self)
            session.commit()
            print(self.id)

        return self

    def update(self, **kwargs) -> 'Model':
        """
        Atualiza os atributos da instância com os valores fornecidos.
        :param kwargs: Atributos a serem atualizados.
        :return: Model - Instância atualizada.
        """
        for key, value in kwargs.items():
            if key in self.field_names():
                setattr(self, key, value)

        with Database.get_session() as session:
            session.commit()

        return self

    def delete(self) -> 'Model':
        """
        Remove a instância do banco de dados.
        :return: Model - Instância removida.
        """
        with Database.get_session() as session:
            session.delete(self)
            session.commit()

        return self

    @classmethod
    def get_from_id(cls, id:int) -> 'Model':
        """
        Busca uma instância pelo ID.
        :param id: int - ID da instância a ser buscada.
        :return: Model - Instância encontrada ou None.
        """
        with Database.get_session() as session:
            return session.query(cls).filter(cls.id == id).one()

    @classmethod
    def as_dataframe(cls):
        """
        Retorna os dados da tabela como um DataFrame.
        :return: DataFrame - Dados da tabela.
        """
        with Database.get_session() as session:
            return pd.read_sql(session.query(cls).statement, session.bind)



