from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.database.database import Database

class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @staticmethod
    def create_all():
        """
        Cria no banco de dados tabelas das classes que herdam o Model.
        Se a tabela já existir, ela não será criada novamente e nem substituída.
        """
        Model.metadata.create_all(bind=Database.engine)

        print("Tabelas criadas com sucesso!")

