from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.python.database.base.model import Model


class Teste(Model):
    __tablename__ = "TESTE"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)