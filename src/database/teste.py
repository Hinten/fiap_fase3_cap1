from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base.model import Model


class Teste(Model):
    __tablename__ = "TESTE"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)


class Teste2(Model):
    __tablename__ = "TESTE2"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    teste_id: Mapped[int] = mapped_column(ForeignKey("TESTE.id"), nullable=False)

    # Relacionamento opcional
    teste: Mapped["Teste"] = relationship("Teste", back_populates="testes")

